import json
import asyncio
import threading
import websockets

from requests import Session
from websockets.sync.client import connect

from typing import Dict,Any, List

class InvalidEndPoint(Exception):
    def __init__(self,endpoint : str) -> None:
        self.endpoint = endpoint
        self.message = "Invalid EndPoint: {}".format(self.endpoint)
        super().__init__(self.message)

class MissingSkeleton(Exception):
    def __init__(self, *args: object) -> None:
        self.message = "Missing Skeleton"
        super().__init__(self.message)

class TokenRequired(Exception):
    def __init__(self, *args: object) -> None:
        self.message = "Token Required"
        super().__init__(self.message)

class Function:
    end_point : str
    method    : str
    session   : Session

    ws        : bool = False
    ws_output : List[Any] = []

    def __init__(self,session : Session,config : Dict) -> None:
        # Set the session
        self.session = session
        # Set the Function Config
        self.end_point = config["end_point"]
        self.method = config["method"]
        # 
        self.queue_input = asyncio.Queue()
        self.queue_output = asyncio.Queue()
        # Prepare the Function
        self.prepare()
    

    def prepare(self):
        # Check if WebSocket is enabled
        if self.method.lower() == "ws":
            # Set WebSocket to True
            self.ws = True
            # Check if the end_point is valid
            if self.end_point.startswith("https://"):
                # Convert https with wss
                self.end_point = self.end_point.replace("https","wss")
            elif self.end_point.startswith("http://"):
                # Convert http with ws
                self.end_point = self.end_point.replace("http","ws")
            elif not self.end_point.startswith("ws://") and not self.end_point.startswith("wss://"):
                # Raise an error if the end_point is not valid
                raise "Invalid EndPoint: {}".format(self.end_point)
            # Set the header
            self.header = {"Authorization" : self.session.headers["Authorization"]}
        # Check if the method is valid
        elif self.method.lower() not in ["get","post","put","delete","ws"]:
            raise "Invalid Method: {}".format(self.method)

    # This function is used to set the params of the websocket connection
    def set_params_ws(self,params : Dict = {}):
        # Check if WebSocket is enabled
        if self.ws:
            # Check if the end_point has params
            if params != {}:
                # Set URI params
                self.end_point += "?"
                self.end_point += "&".join([f"{key}={params[key]}" for key in params.keys()])
    # Start the WebSocket Client
    async def ws_start(self,params : Dict = {}):
        self.queue_input = asyncio.Queue()
        self.queue_output = asyncio.Queue()
        # Check if WebSocket is enabled
        if self.ws:
            # Set URI params
            self.set_params_ws(params)
            try:
                # WebSocket connection Variables
                uri = self.end_point
                headers = self.header
                # Connect to the WebSocket
                async with websockets.connect(uri, extra_headers=headers) as ws:
                    # Define the receiver and sender functions
                    async def receiver(ws):
                        data = []
                        # Receive data from the WebSocket
                        async for msg in ws:
                            await self.queue_output.put(json.loads(msg))
                    # Define the sender function
                    async def sender(ws):
                        try:
                            # Send data to the WebSocket
                            while True:
                                # Get data from the queue
                                data = await self.queue_input.get()
                                # Send data to the WebSocket
                                await ws.send(data)                        
                        except websockets.exceptions.ConnectionClosedOK:
                            await ws.send(json.dumps({"type": "CloseStream"}))
                        except Exception as e:
                            print(e)
                            pass
                    # Start the receiver and sender functions
                    functions = [
                        asyncio.ensure_future(sender(ws)),
                        asyncio.ensure_future(receiver(ws)),
                    ]
                    # Wait for the functions to finish
                    await asyncio.gather(*functions)          
            except websockets.exceptions.ConnectionClosedError as e:
                print(f"WebSocket connection closed unexpectedly: {e}")
        else:
            raise Exception("Not a WebSocket\n Please use start(params) to start the connection")

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if not self.ws:
            if "url_params" in kwds.keys():
                return self.session.request(self.method,self.end_point.format(kwds["url_params"]),**kwds)
            return self.session.request(self.method,self.end_point,**kwds)
        else:
            if args != {}:
                self.queue_input.put_nowait(args)
                output = self.queue_output.get_nowait()
                if output is not None:
                    return output
                return None
            
            
class RestAPI:

    paper : Dict
    # session Data
    url     : str
    headers : Dict
    session : Session
    skeleton: Dict

    def __init__(self,paper : Dict,token=None) -> None:
        self.paper = paper
        self.key = token
        self.start()

    def start(self):
        if "end_point" not in self.paper.keys():
            raise InvalidEndPoint("")
        if "skeleton" not in self.paper.keys():
            raise MissingSkeleton()
        if "header" not in self.paper.keys():
            self.paper["header"] = {}
        self.url = self.paper["end_point"]
        self.headers = self.paper["header"]
        for key in self.headers:
            if key.startswith("*"):
                new_key = key.replace("*","")
                if self.key is None:
                    raise TokenRequired("")
                self.headers[new_key] = self.headers[key].format(self.key)
                del self.headers[key]
                break
        self.session = Session()
        self.session.headers.update(self.headers)
        self.skeleton = self.paper["skeleton"]
        self.load_functions()

    def load_functions(self):
        for key in self.skeleton:
            if self.url.endswith("/"):
                self.url = self.url[:-1]
            end_point = self.skeleton[key]["suffix"]
            _ = {
                "end_point" : f"{self.url}/{self.skeleton[key]['suffix']}",
                "method"    : self.skeleton[key]["method"],
            }
            setattr(self,key,Function(self.session,_))
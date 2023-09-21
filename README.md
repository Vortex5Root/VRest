# VRest Documentation

## Introduction

VRest is a Python library for making HTTP and WebSocket requests to RESTful and WebSocket-based APIs. It provides a flexible and easy-to-use interface for interacting with various APIs, allowing you to send requests and receive responses.

## Installation

You can install VRest using pip:

```bash
poetry add git+https://github.com/Vortex5Root/VRest.git
```

## Quick Start

To get started with VRest, you need to create a `RestAPI` instance and define your API configuration, including the API endpoint, headers, and available functions. Here's a basic example using the Deepgram API:

```python
from VRest.vrest.new_version import RestAPI

# Define the API configuration
deepgram_config = {
    "end_point": "https://api.deepgram.com/v1/",
    "header": {
        "accept": "application/json",
        "content-type": "application/json",
        "*Authorization": "Token {}"
    },
    "skeloton": {
        "pre_recode": {
            "suffix": "listen",
            "method": "POST"
        },
        "stream": {
            "suffix": "listen",
            "method": "ws"
        }
    }
}

# Create a RestAPI instance
deepgram_api = RestAPI(deepgram_config, api_key="YOUR_API_KEY")

# Example API request
response = deepgram_api.pre_recode(params={"filler_words": "false", "summarize": "v2"}, json={"url": "https://static.deepgram.com/examples/interview_speech-analytics.wav"})

# Print the response status code and data
print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    print(response.json()["results"]["channels"][0]["alternatives"][0]["transcript"])
else:
    print(response.text)
```

## Usage

### Creating a RestAPI Instance

To interact with an API, you need to create a `RestAPI` instance by providing the API configuration in a dictionary format. The configuration should include the API endpoint, headers, and skeloton (available API functions).

```python
api_config = {
    "end_point": "https://api.example.com/v1/",
    "header": {
        "accept": "application/json",
        "content-type": "application/json",
        "*Authorization": "Token {}"
    },
    "skeloton": {
        "function_name": {
            "suffix": "endpoint_suffix",
            "method": "GET"
        }
        # Add more functions as needed
    }
}

# Create a RestAPI instance
api = RestAPI(api_config, api_key="YOUR_API_KEY")
```

### Making API Requests

Once you have created a `RestAPI` instance, you can make API requests using the defined functions. For example, to make a GET request to the `function_name` endpoint:

```python
response = api.function_name(params={"param_name": "param_value"})
```

Replace `function_name` with the name of the function you want to call, and provide any necessary parameters as a dictionary in the `params` argument.

### WebSocket Support

VRest also supports WebSocket connections. If a function is configured to use WebSocket (method="ws"), you can start a WebSocket connection and send and receive data. Here's an example of starting a WebSocket connection:

```python
async def start_websocket():
    # Start the WebSocket connection
    await api.function_name.ws_start(params={"param_name": "param_value"})

# Create an asyncio event loop and run the WebSocket function
import asyncio
loop = asyncio.get_event_loop()
loop.run_until_complete(start_websocket())
```

### Audio Streaming Example

The provided code includes an audio streaming example using PyAudio and WebSocket. It captures audio from a microphone, sends it to the Deepgram API for speech recognition, and receives the transcribed text. You can adapt this example for your specific use case.

## Error Handling

VRest includes custom exceptions for handling common errors:

- `InvalidEndPoint`: Raised when the API endpoint is invalid.
- `MissingSkeloton`: Raised when the API configuration lacks a skeloton (function definitions).
- `TokenRequired`: Raised when an API request requires an authentication token.

You can handle these exceptions in your code to gracefully manage errors.

## Conclusion

VRest simplifies API interaction by providing a clean and flexible interface for making HTTP and WebSocket requests. You can use it to communicate with various APIs and easily handle responses and errors. Explore the library further and customize it to meet your specific needs.
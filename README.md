# Welcome to VRest

VRest is a powerful Python library designed for simplifying the process of making RESTful API calls. It provides an intuitive and user-friendly interface, enabling developers to effortlessly create and execute API requests.

## Installation

To get started with VRest, you can easily install it using Poetry, a dependency management tool. Follow the instructions below to add VRest to your project:

```bash
poetry add git+https://github.com/Vortex5Root/VRest.git
```

By running this command, Poetry will fetch the latest version of VRest from the specified Git repository and add it as a dependency to your project.

## Usage

### Creating a Dictionary

VRest requires a configuration dictionary that defines the API endpoints and their associated request details. This dictionary is structured in JSON format. Here's an example of how it should be organized:

```json
{
    "end_point": "<url>",
    "header":{
        "<row>","value"
    },
    "<function_name>": {
        "method": "<GET, POST, PUT, DELETE>",
        "<json, parms>": {
            "<var_name>": {},
            ...
        },
        ...
    },
    ...
}
```

To customize the dictionary for your specific API, replace `<url>` with the base URL of your API and `<function_name>`, `<method>`, `<json, parms>`, and `<var_name>` with appropriate values that correspond to your API's structure.
Use Header to set Auth Tokens
### Example

Here's a practical example to demonstrate how VRest can be utilized within your Python code:

```python
# Import VRest
from vrest import RestAPI
# Import required modules
import json

# Load the configuration dictionary from a file
config = {}
with open("<Dictionary_File>.json", "r") as config_file:
    config = json.loads(config_file.read())

# Create a RestAPI object
api = RestAPI(config)

# Set the API endpoint path
api.path = "<Path>"

# Set the command
api.sub_dir = "<Command>"

# Execute the API call
api.exec({})
```

Ensure that you replace `"<Dictionary_File>.json"` with the actual path to your configuration file. Customize `<Path>` and `<Command>` based on your specific API requirements.

## Contributing

If you would like to contribute to the development of VRest, we welcome your contributions! Feel free to submit pull requests or open issues on the GitHub repository at [https://github.com/Vortex5Root/VRest](https://github.com/Vortex5Root/VRest).

## License

VRest is released under the [MIT License](https://opensource.org/licenses/MIT), granting you the freedom to utilize and modify the library according to your needs.

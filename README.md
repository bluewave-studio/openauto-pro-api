## **Description**
OpenAuto Pro API is defined in [Protocol Buffers](https://developers.google.com/protocol-buffers/docs/overview) language. Protocol Buffers has ability to generate code for various programming languages (e. g. C++, Python, JavaScript, Java and many others). Communication with OpenAuto Pro application using the API is done via TCP/IP protocol.


More details regarding protocol format can be found directly in [Api.proto](Api.proto) file. This file contains definition of all payloads in the API. We also provide examples written in Python 3 that cover all functionalities of the API.
<br />
In case of support, suggestions or any other queries, please visit our [community](https://www.bluewavestudio.io/community/).
<br />
## **Generating [Api_pb2.py](api_examples/python/common/Api_pb2.py) from [Api.proto](Api.proto)**
[Api_pb2.py](api_examples/python/common/Api_pb2.py) is automatically generated file by protoc (part of [Protocol Buffers](https://developers.google.com/protocol-buffers/docs/overview)). In order to generate it from [Api.proto](Api.proto) use following command:

```console
protoc --python_out=api_examples/python/common/ Api.proto
```

**protoc** command can also be used to generate code of the Api for different languages (C++, JavaScript, etc.).
<br />
## **Supported features**
* Audio Focus
* Controlling Day/Night theme
* Injecting key strokes
* Fetching media metadata
* Fetching navigation data
* Displaying notifications
* Injecting OBD-II data
* Reading OBD-II data
* Fetching phone status
* Fetching projection status
* Controlling reverse gear status
* Displaying status icons
* Injecting temperature
* Reading temperature

## **Message format**
| | Field 1 | Field 2 | Field 3 | Field 4 |
| --- | --- | --- | --- | --- |
| **Description** | Size of the Protocol Buffers byte stream | Message Id | Flags | Protocol Buffers byte stream |
| **Size** | 32-bit unsigned integer (little endian) | 32-bit unsigned integer (little endian) | 32-bit unsigned integer (little endian) | n |

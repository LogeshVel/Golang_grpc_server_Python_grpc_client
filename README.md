## Golang_grpc_server_Python_grpc_client

Simple CRUD gRPC API. Golang Server and Python Client.

Package or Lib Requirements:

- To compile proto file to Golang pb file we need _protoc-gen-go_ plugin along with the **protoc**. Same to compile the proto file to Golang grpc pb filr we need _protoc-gen-go-grpc_ plugin. For Installation of these plugins,

        $ go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.28

        $ go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.2

- To compile the proto file to Python pb and grpc file we can use **_grpcio-tools_**. For installation

        pip install grpcio-tools

- We need to install protobuf and grpc for both the Languanbge (Golang and Python). For Python it will be installed by the **grpcio-tools** so Python is good to go. For Golang we should use go get to get this packages.

        $ go get -u google.golang.org/grpc
        $ go get -u google.golang.org/protobuf

### Usage:

Add the Project's root dir path to the GOPATH and PYTHONPATH and for PYTHONAPTH need to add one more path for pb files. /path/to/Golang_grpc_server_Python_grpc_client/python_client/python_pb_files

Run the Golang Server and then run the Python Client.

### GOPATH and PYTHONPATH

Placed all the compiled Go pb file under src directory and then added the Projects root directory in the GOPATH and turned off the GO111MODULE.

For PYTHONPATH add the Project's root dir path and the _/path/to/Golang\_grpc\_server\_Python\_grpc\_client/python\_client/python\_pb\_files_


Checkout my Medium Article on gRPC - Golang Server and Python Client (will publish soon)

### Extension of this project

In this project we have Golang gRPC Server and the Python gRPC Client. 

This repo ([gRPC Server - gRPC client and REST client](https://github.com/LogeshVel/grpc_server_grpc_and_REST_client)) has the gRPC server that serves the gRPC and REST Clients.

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

Usage:

Run the Golang Server and then run the Python Client.
#!/bin/bash
set -x
python -m grpc.tools.protoc -I . --python_out=. --grpc_python_out=. scalica.proto

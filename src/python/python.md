# Pythonでの利用

https://www.grpc.io/docs/languages/python/quickstart/

## インストール

### gRPC

本体

~~~
python -m pip install grpcio
~~~

### gRPC tools

ツール類

~~~
python -m pip install grpcio-tools
~~~

## 開発

### サンプル

sample.proto

~~~
syntax = "proto3";

// リクエスト
message SampleRequest {
    string message = 1;
}

// レスポンス
message SampleResponse {
    string reply = 1;
}

// サンプルサービス
service SampleService {
    // サービス側メソッドの呼び出し
    rpc Call (SampleRequest) returns (SampleResponse) {}
}
~~~


### protoファイルのコンパイル

以下をpyファイルに起こして実行する。

~~~python
from grpc.tools import protoc
protoc.main(
    (
        '',
        '-I.',
        '--python_out=.',
        '--grpc_python_out=.',
        'XXX.proto',
    )
)
~~~

実行すると、XXX_pb2.py と XXX_pb2_grpc.py が生成される。

* XXX_pb2.py
  * シリアライズのインターフェース
* XXX_pb2_grpc.py
  * gRPCのインターフェース


### 実装：サーバ側

grpc、生成された2ファイルをimportする。

#### Servicerクラスの継承

XXX_pb2_grpc.py に定義されている、XXXServicerを継承したクラスを作成する。

Servicerクラスには、.protoで定義したserviceがインターフェースとして実装されている。
これを継承し、.protoで定義した引数、戻り値に則ってabstractメソッドを実装していく。

~~~python
import grpc
from sample_pb2 import SampleRequest, SampleResponse  
from sample_pb2_grpc import SampleServiceServicer

class SampleService(SampleServiceServicer):
    def __init__(self):
        pass
    def Call(self, request:SampleRequest, context):
        print(f"request : {request.message}")
        return SampleResponse(reply=f"reply for {request.message}")
~~~

### サーバの開始

1. grpc.server()メソッドを用いて、serverを作成
   * 同時実行数などを引数で指定（スレッドプールとして）
1. XXX_pb2_grpc.add_XXXServicer_to_server()メソッドで、Servicerとserverを紐づけ
1. アドレス、ポートを指定して、サーバを開始 

~~~python
server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
add_SampleServiceServicer_to_server(SampleService(), server)
server.add_insecure_port('[::]:9999')
server.start()
~~~

まとめると

~~~python
import grpc
from sample_pb2 import SampleRequest, SampleResponse  
from sample_pb2_grpc import SampleServiceServicer, add_SampleServiceServicer_to_server


class SampleService(SampleServiceServicer):
    def __init__(self):
        super().__init__()
    def Call(self, request, context):
        print(f"request : {request.message}")
        return SampleResponse(reply=f"reply for {request.message}")

from concurrent import futures
from sample_pb2_grpc import add_SampleServiceServicer_to_server

def StartServer():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    add_SampleServiceServicer_to_server(SampleService(), server)
    server.add_insecure_port('[::]:9999')
    server.start()
    print('server started')
    return server

def Main():
    StartServer().wait_for_termination()

if __name__ == '__main__':
    Main()
~~~


### 実装：クライアント側

grpc、生成された2ファイルをimportする。

#### サーバへの接続

1. アドレス、ポートを指定してサーバへ接続する
   * insecure_channel()/secure_channel()
1. XXX_pb2_grpc.XXXStubクラスのインスタンスを生成
   * Stubには、.protoで定義したserviceのメソッドが定義されており、サーバへの通信がラップされている

~~~python
import grpc
from sample_pb2 import SampleRequest, SampleResponse 
from sample_pb2_grpc import SampleServiceStub

def Request():
    with grpc.insecure_channel('localhost:9999') as channel:
        stub = SampleServiceStub(channel)
        request = SampleRequest(message = 'test message')
        print(f"request : {request.message}")
        response = stub.Call(request)
        print(f"response : {response.reply}")

if __name__ == '__main__':
    Request()
~~~

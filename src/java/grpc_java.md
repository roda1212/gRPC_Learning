# javaでの利用

https://www.grpc.io/docs/languages/java/quickstart/

## インストール

Maven、Gradleなどの例が書かれている
試しにGradleを使う

## 開発

### サンプル

sample.proto

~~~groovy
syntax = "proto3";

package sample;

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

### protoファイルのコンパイル：Gragle

必要なもの

* [grpc-java](https://github.com/grpc/grpc-java)
  * java用のgRPCライブラリ、フレームワーク
* [protobuf-gradle-plugin](https://github.com/google/protobuf-gradle-plugin)
  * protocol buffer生成用のgradleプラグイン

* javaパッケージ名なども指定できる
  * option java_package = "パッケージ名";

#### build.gradle

以下の設定で、必要なプラグインの取得、.protoのコンパイルをまとめてできる。

設定の詳細に関しては以下を参照

https://github.com/grpc/grpc-java
https://github.com/google/protobuf-gradle-plugin

~~~groovy

~~~


gradlew generateProtoを実行すると、以下のファイルが生成される。

* XXX.java
  * シリアライズのインターフェース
* XXXServiceGrpc.java
  * gRPCのインターフェース

### 実装：サーバ側

#### ServiceImplBaseクラスの継承

XXXServiceGrpc.java に定義されている、ベースクラスを継承する

~~~java
package server;

import io.grpc.stub.StreamObserver;
import sample.Sample.SampleRequest;
import sample.Sample.SampleResponse;;

public class SampleService extends sample.SampleServiceGrpc.SampleServiceImplBase {
    @Override
    public void call(SampleRequest request,
        StreamObserver<SampleResponse> responseObserver) {
        SampleResponse.Builder builder = SampleResponse.newBuilder();
        System.out.println("request : " + request.getMessage());
        builder.setReply("reply for \"" + request.getMessage() + "\" (java)");
        SampleResponse response = builder.build();
        responseObserver.onNext(response);
        responseObserver.onCompleted();
    }
}
~~~

### サーバの開始

1. ポートを指定してio.grpc.ServerBuilderを作成し、サービスを紐づけ、build()
2. サーバを開始

~~~java
/*
 * This Java source file was generated by the Gradle 'init' task.
 */
package server;

import java.io.IOException;

import io.grpc.Server;
import io.grpc.ServerBuilder;

public class SampleServer {
    public static void main(String[] args) throws IOException, InterruptedException {
        final int portNumber = 9999;
        Server server = ServerBuilder.forPort(portNumber)
                                .addService(new SampleService())
                                .build();
        server.start();
        System.out.println("server started");
        server.awaitTermination();
    }
}
~~~

### 実装：クライアント側

1. アドレス、ポートを指定してchannelを作成
   1. usePlaintext() or notで平文か暗号文か切り替わる？
2. channelを紐づけStubを作成
   * サービス種別によって使えるものが異なる？
     * Stub : async stub
     * BlockingStub : blocking-style stub
     * FutureStub : ListenableFuture-style stub
3. Stubに実装されたIFメソッドを呼び出す

~~~java
/*
 * This Java source file was generated by the Gradle 'init' task.
 */
package client;

import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;

import sample.Sample.SampleRequest;
import sample.Sample.SampleResponse;
import sample.SampleServiceGrpc;

public class SampleClient {
    public static void main(String[] args) {
        final int portNumber = 9999;
        ManagedChannel channel = ManagedChannelBuilder.forAddress("localhost", portNumber)
                                .usePlaintext().build();
        SampleServiceGrpc.SampleServiceBlockingStub stub
                 = SampleServiceGrpc.newBlockingStub(channel);

        SampleRequest request = SampleRequest.newBuilder()
                                .setMessage("test message (java)").build();
        
        System.out.println("request : " + request.getMessage());
        SampleResponse response = stub.call(request);
        System.out.println("response : " + response.getReply());
    }
}
~~~

## 参考

* https://qiita.com/disc99/items/3fdfe5c1c1170871221a

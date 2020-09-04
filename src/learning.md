# gRPC

https://grpc.io/

* Googleが開発したRPC（Remote Procedure Call）
  * 高速かつ低用量、数多くの開発言語に対応
* シリアライズにProtocol Bufferを使用する

## Protocol Buffer

https://developers.google.com/protocol-buffers/

シリアライズフォーマットの一つ。
XMLより小さく、高速に扱える？

IDLで構造を定義


[wikipedia](https://ja.wikipedia.org/wiki/Protocol_Buffers)


### protoファイル

データの定義を行うファイル。

#### 定義

以下のように定義する。

~~~
syntax = "proto3";

message XXX {
    型 変数名 = フィールド番号;
}
~~~

* 記述形式がproto2とproto3の二種類ある。
  * 上の定義はproto3形式。これから作るならこれに準拠していたほうが良いか。
  * 違いは[ここ](https://qiita.com/ksato9700/items/0eb025b1e2521c1cab79)参照

#### コンパイル

protocでコンパイルしてコードを生成。
protocは、前述のリンクからたどってDownloadページへいくと、バイナリが手に入る。

記述形式はデフォルトではproto2が選択されるらしい。
protoファイルに明示していないと、指定したほうがいいよ、と警告が出る。

コンパイル後の出力フォーマットは言語に依存し、コンパイル時に指定する。

**protoc引数**

~~~
Usage: protoc [OPTION] PROTO_FILES
Parse PROTO_FILES and generate output based on the options given:
  -IPATH, --proto_path=PATH   Specify the directory in which to search for
                              imports.  May be specified multiple times;
                              directories will be searched in order.  If not
                              given, the current working directory is used.
                              If not found in any of the these directories,
                              the --descriptor_set_in descriptors will be
                              checked for required proto file.
  --version                   Show version info and exit.
  -h, --help                  Show this text and exit.
  --encode=MESSAGE_TYPE       Read a text-format message of the given type
                              from standard input and write it in binary
                              to standard output.  The message type must
                              be defined in PROTO_FILES or their imports.
  --decode=MESSAGE_TYPE       Read a binary message of the given type from
                              standard input and write it in text format
                              to standard output.  The message type must
                              be defined in PROTO_FILES or their imports.
  --decode_raw                Read an arbitrary protocol message from
                              standard input and write the raw tag/value
                              pairs in text format to standard output.  No
                              PROTO_FILES should be given when using this
                              flag.
  --descriptor_set_in=FILES   Specifies a delimited list of FILES
                              each containing a FileDescriptorSet (a
                              protocol buffer defined in descriptor.proto).
                              The FileDescriptor for each of the PROTO_FILES
                              provided will be loaded from these
                              FileDescriptorSets. If a FileDescriptor
                              appears multiple times, the first occurrence
                              will be used.
  -oFILE,                     Writes a FileDescriptorSet (a protocol buffer,
    --descriptor_set_out=FILE defined in descriptor.proto) containing all of
                              the input files to FILE.
  --include_imports           When using --descriptor_set_out, also include
                              all dependencies of the input files in the
                              set, so that the set is self-contained.
  --include_source_info       When using --descriptor_set_out, do not strip
                              SourceCodeInfo from the FileDescriptorProto.
                              This results in vastly larger descriptors that
                              include information about the original
                              location of each decl in the source file as
                              well as surrounding comments.
  --dependency_out=FILE       Write a dependency output file in the format
                              expected by make. This writes the transitive
                              set of input file paths to FILE
  --error_format=FORMAT       Set the format in which to print errors.
                              FORMAT may be 'gcc' (the default) or 'msvs'
                              (Microsoft Visual Studio format).
  --print_free_field_numbers  Print the free field numbers of the messages
                              defined in the given proto files. Groups share
                              the same field number space with the parent 
                              message. Extension ranges are counted as 
                              occupied fields numbers.

  --plugin=EXECUTABLE         Specifies a plugin executable to use.
                              Normally, protoc searches the PATH for
                              plugins, but you may specify additional
                              executables not in the path using this flag.
                              Additionally, EXECUTABLE may be of the form
                              NAME=PATH, in which case the given plugin name
                              is mapped to the given executable even if
                              the executable's own name differs.
  --cpp_out=OUT_DIR           Generate C++ header and source.
  --csharp_out=OUT_DIR        Generate C# source file.
  --java_out=OUT_DIR          Generate Java source file.
  --js_out=OUT_DIR            Generate JavaScript source.
  --objc_out=OUT_DIR          Generate Objective-C header and source.
  --php_out=OUT_DIR           Generate PHP source file.
  --python_out=OUT_DIR        Generate Python source file.
  --ruby_out=OUT_DIR          Generate Ruby source file.
  @<filename>                 Read options and filenames from file. If a
                              relative file path is specified, the file
                              will be searched in the working directory.
                              The --proto_path option will not affect how
                              this argument file is searched. Content of
                              the file will be expanded in the position of
                              @<filename> as in the argument list. Note
                              that shell expansion is not applied to the
                              content of the file (i.e., you cannot use
                              quotes, wildcards, escapes, commands, etc.).
                              Each line corresponds to a single argument,
                              even if it contains spaces.
~~~


## gRPCを使ってみる

### protoファイル

gRPCで使用する場合には、messageに加え、service（インターフェース）を定義する必要がある。

~~~
syntax = "proto3";

message SampleRequest {
    string message = 1;
}

message SampleResponse {
    string reply = 1;
}

service SampleService {
    rpc Call (SampleRequest) returns (SampleResponse) {}
}
~~~

また、コンパイルは、protocだけでなく、各言語用のプラグインが必要。

### 実際の使用

各開発言語を参照

## その他

## 通信方式

4種類ある
* Unary
  * 1 req, 1 res
* Server streaming
  * 1 req, n res
* Client streaming
  * n req, 1 res
* Bidirectional streaming
  * x req, y res

説明は以下がわかりやすい
[goでgRPCの4つの通信方式やってみた(Dockerのサンプルあり)](https://qiita.com/tomo0/items/310d8ffe82749719e029)

## protoファイルの管理

実際に触ってみて、大きな課題はIDLの管理（共有方法）のように感じた。

Java-Gradleはデフォルトで自プロジェクト配下の.protoをコンパイルするようになっている。
それだとServer-Clientでモジュールが分かれる場合にはどーすんの？
ましてや、開発言語が変わったらどうすりゃいいのか。

[Qiita - Protocol buffers の proto ファイルの管理と配布](https://qiita.com/RyotaNakaya/items/d71d2cb5f5cd44b052ee)
のように、同じ課題意識を持っている人はいる。

個人的には方針2か3かな。。。
いずれにしても、どうやって参照するかが悩みどころな気がする。
リポジトリに.protoもpublishする感じ？

## Link

* [いまさらだけどgRPCに入門したので分かりやすくまとめてみた](https://qiita.com/gold-kou/items/a1cc2be6045723e242eb)
  * 比較的わかりやすい
* [gRPCのシリアライゼーション形式をJSONにする](https://qiita.com/yugui/items/238dcdb75cd40d0f1ece)
  * できるらしいが、かなり手間はかかりそう

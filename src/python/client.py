import grpc
from sample_pb2 import SampleRequest, SampleResponse 
from sample_pb2_grpc import SampleServiceStub

def Request():
    with grpc.insecure_channel('localhost:9999') as channel:
        stub = SampleServiceStub(channel)
        request = SampleRequest(message = 'test message (python)')
        print(f"request : {request.message}")
        response = stub.Call(request)
        print(f"response : {response.reply}")

if __name__ == '__main__':
    Request()


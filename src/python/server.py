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
import time
import grpc
from concurrent import futures
import threading
from protos.protopb import rpc_pb2, rpc_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Listener(rpc_pb2_grpc.GreetServiceServicer):

    def Greet(self, request, context):
        print("Invoked unary unary")
        return rpc_pb2.GreetResponse(result="Hello, %s!" % request.greeting.first_name)

    def GreetManyTimes(self, request, context):
        print("Invoked unary stream")
        name = request.greeting.first_name
        for i in range(0, 10):
            result = f"Hello {name} ! - {i + 1}"
            yield rpc_pb2.GreetManyTimesResponse(result=result)
            time.sleep(5)

    def LGreet(self, request_iterator, context):
        print("Invoked stream unary")
        result = ""
        for item in request_iterator:
            result += f"Hello {item.greeting.first_name} !\n"
        return rpc_pb2.LongGreetResponse(result=result)

    def GreetEveryone(self, request_iterator, context):
        print("Invoked bidirectional streaming")
        for new_note in request_iterator:
            result = f"Hello {new_note.greeting.first_name} !"
            yield rpc_pb2.GreetEveryoneResponse(result=result)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
    rpc_pb2_grpc.add_GreetServiceServicer_to_server(Listener(), server)
    server.add_insecure_port("[::]:500511")
    server.start()
    try:
        while True:
            print("Started...")
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        server.stop(0)


if __name__ == "__main__":
    serve()

import grpc
from protos.protopb import rpc_pb2, rpc_pb2_grpc
import time
import random


def generate_request(feature_list):
    for item in feature_list:
        yield item
        time.sleep(5)


def make_request(name):
    return rpc_pb2.GreetEveryoneRequest(greeting=rpc_pb2.Greeting(first_name=name))


def get_names():
    name_array = [make_request("Theesh"), make_request("Sandaru"), make_request("Thilakarathne")]
    for name in name_array:
        yield name
        time.sleep(5)


def unary():
    chanel = grpc.insecure_channel('localhost:500511')
    stub = rpc_pb2_grpc.GreetServiceStub(chanel)
    greet = rpc_pb2.Greeting(first_name="Theesh")
    greetRequest = rpc_pb2.GreetRequest(greeting=greet)
    greetResp = stub.Greet(greetRequest)
    print(greetResp.result)


def unary_stream():
    chanel = grpc.insecure_channel('localhost:500511')
    stub = rpc_pb2_grpc.GreetServiceStub(chanel)
    greet = rpc_pb2.Greeting(first_name="Theesh")
    greetRequest = rpc_pb2.GreetManyTimesRequest(greeting=greet)
    greetResp = stub.GreetManyTimes(greetRequest)
    for i in greetResp:
        print(i.result)
    # print(greetResp.result)


def stream_unary():
    chanel = grpc.insecure_channel('localhost:500511')
    stub = rpc_pb2_grpc.GreetServiceStub(chanel)
    requests = [
        rpc_pb2.GreetManyTimesRequest(greeting=rpc_pb2.Greeting(first_name="Theesh")),
        rpc_pb2.GreetManyTimesRequest(greeting=rpc_pb2.Greeting(first_name="Saja")),
        rpc_pb2.GreetManyTimesRequest(greeting=rpc_pb2.Greeting(first_name="Thilake"))
    ]
    route_iterator = generate_request(requests)
    route_summary_future = stub.LGreet.future(route_iterator)
    data = route_summary_future.result()
    print(data.result)


def bidirectional():
    chanel = grpc.insecure_channel('localhost:500511')
    stub = rpc_pb2_grpc.GreetServiceStub(chanel)
    responses = stub.GreetEveryone(get_names())
    for item in responses:
        print(item.result)


if __name__ == "__main__":
    bidirectional()

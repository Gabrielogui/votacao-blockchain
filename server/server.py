from concurrent import futures
import grpc
import voting_pb2_grpc
from node import VotingNode

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    voting_pb2_grpc.add_VotingServiceServicer_to_server(VotingNode(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
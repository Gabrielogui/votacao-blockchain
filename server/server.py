from concurrent import futures
import grpc

import voting_pb2_grpc
import node_pb2_grpc
from node import VotingNode, NodeService


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    voting_pb2_grpc.add_VotingServiceServicer_to_server(VotingNode(), server)
    node_pb2_grpc.add_NodeServiceServicer_to_server(NodeService(node_id="Node-1"), server)

    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor rodando na porta 50051...")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
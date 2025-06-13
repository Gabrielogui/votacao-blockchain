from concurrent import futures
import grpc
import time

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'proto')))

import voting_pb2_grpc
import node_pb2_grpc
from node import VotingNode, NodeService


def serve(port=50051, node_id="Node-1"):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Instanciar os serviços
    voting_service = VotingNode()
    node_service = NodeService(node_id=node_id)

    # Registrar os serviços no servidor gRPC
    voting_pb2_grpc.add_VotingServiceServicer_to_server(voting_service, server)
    node_pb2_grpc.add_NodeServiceServicer_to_server(node_service, server)

    server.add_insecure_port(f'[::]:{port}')
    server.start()

    print(f"| Servidor {node_id} rodando na porta {port}...")
    try:
        while True:
            time.sleep(86400)  # Mantém o servidor vivo (1 dia)
    except KeyboardInterrupt:
        print("\n□ Servidor interrompido.")
        server.stop(0)


if __name__ == '__main__':
    serve()
from concurrent import futures
import grpc
import time
import sys
import os

# Ajusta path para encontrar proto e node.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'proto')))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import voting_pb2_grpc
import node_pb2_grpc
from node import VotingNode, NodeService


def serve(port, node_id):
    # Criação do servidor gRPC com 10 threads
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Instanciando os serviços
    voting_service = VotingNode(node_id=node_id, port=port)
    node_service = NodeService(node_id=node_id)

    # Registrando serviços no servidor
    voting_pb2_grpc.add_VotingServiceServicer_to_server(voting_service, server)
    node_pb2_grpc.add_NodeServiceServicer_to_server(node_service, server)

    server.add_insecure_port(f'[::]:{port}')
    server.start()

    print(f"\n✅ Servidor {node_id} rodando na porta {port}...")
    print("ℹ️ Pressione Ctrl+C para encerrar.\n")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        print(f"\n□ Servidor {node_id} interrompido.")
        server.stop(0)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Servidor de Votação Blockchain")
    parser.add_argument('--port', type=int, default=50051, help='Porta do servidor')
    parser.add_argument('--id', type=str, default='Node-1', help='ID do nó')

    args = parser.parse_args()
    serve(args.port, args.id)

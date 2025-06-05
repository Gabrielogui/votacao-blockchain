import grpc

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'proto')))

import voting_pb2
import voting_pb2_grpc
from google.protobuf import empty_pb2
import argparse


def submit_vote(stub, voter_id, candidate):
    try:
        request = voting_pb2.VoteRequest(voter_id=voter_id, candidate=candidate)
        stub.CastVote(request)
        print(f"✅ Voto para '{candidate}' registrado com sucesso pelo eleitor '{voter_id}'.")
    except grpc.RpcError as e:
        print(f"❌ Erro ao enviar voto: {e.details()}")


def get_results(stub):
    try:
        response = stub.GetResults(empty_pb2.Empty())
        print("🗳️ Resultados da votação:")
        for candidate, votes in response.results.items():
            print(f"➡️ {candidate}: {votes} votos")
    except grpc.RpcError as e:
        print(f"❌ Erro ao buscar resultados: {e.details()}")


def main():
    parser = argparse.ArgumentParser(description="Cliente para o sistema de votação")
    subparsers = parser.add_subparsers(dest='command')

    # Comando para votar
    vote_parser = subparsers.add_parser('vote', help='Enviar um voto')
    vote_parser.add_argument('--voter_id', type=str, required=True, help='ID do eleitor')
    vote_parser.add_argument('--candidate', type=str, required=True, help='Nome do candidato')

    # Comando para consultar resultados
    result_parser = subparsers.add_parser('results', help='Consultar resultados da votação')

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    # Abre conexão com o servidor
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = voting_pb2_grpc.VotingServiceStub(channel)

        if args.command == 'vote':
            submit_vote(stub, args.voter_id, args.candidate)
        elif args.command == 'results':
            get_results(stub)


if __name__ == '__main__':
    main()

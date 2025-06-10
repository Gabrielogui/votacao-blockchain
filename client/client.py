import sys
import os
import grpc
from google.protobuf import empty_pb2

# Garante que o Python ache os arquivos .py gerados a partir dos .proto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'proto')))

import voting_pb2
import voting_pb2_grpc


def submit_vote(stub):
    voter_id = input("🆔 Digite seu ID de eleitor: ").strip()
    print("👤 Escolha um candidato:")
    candidates = {
        1: "Alice",
        2: "Bruno",
        3: "Carlos",
        4: "Daniela"
    }
    for cid, name in candidates.items():
        print(f"{cid}. {name}")

    try:
        choice = int(input("Digite o número do candidato: "))
        if choice not in candidates:
            print("❌ Opção inválida!")
            return
        candidate_id = candidates[choice]  # string conforme o seu proto
    except ValueError:
        print("❌ Entrada inválida!")
        return

    try:
        req = voting_pb2.VoteRequest(voter_id=voter_id, candidate_id=candidate_id)
        resp = stub.SubmitVote(req)
        print(f"✅ {resp.message}")
    except grpc.RpcError as e:
        print(f"❌ Erro ao enviar voto: {e.details()}")


def get_results(stub):
    try:
        resp = stub.QueryResults(empty_pb2.Empty())
        print("\n📊 Resultados da votação:")
        for candidate, votes in resp.results.items():
            print(f"➡️ {candidate}: {votes} voto(s)")
    except grpc.RpcError as e:
        print(f"❌ Erro ao buscar resultados: {e.details()}")


def main():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = voting_pb2_grpc.VotingServiceStub(channel)

        while True:
            print("\n========= MENU =========")
            print("1. Votar")
            print("2. Ver resultados")
            print("3. Sair")
            print("========================")
            opc = input("Escolha uma opção: ").strip()

            if opc == '1':
                submit_vote(stub)
            elif opc == '2':
                get_results(stub)
            elif opc == '3':
                print("👋 Encerrando cliente...")
                break
            else:
                print("❌ Opção inválida! Tente novamente.")


if __name__ == '__main__':
    main()

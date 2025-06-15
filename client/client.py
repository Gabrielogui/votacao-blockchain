import sys
import os
import json
import grpc
from google.protobuf import empty_pb2

# Ajusta o path para importar os módulos gerados a partir dos .proto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'proto')))

import voting_pb2
import voting_pb2_grpc

PEERS_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'server', 'peers.json'))

def load_peers():
    """Carrega a lista de nós (peers) de peers.json."""
    try:
        with open(PEERS_FILE, 'r') as f:
            data = json.load(f)
        return data.get('peers', [])
    except Exception as e:
        print(f"🚨 Não foi possível carregar peers.json: {e}")
        return []

def pick_node(peers):
    """Exibe e permite escolher qual nó usar."""
    print("\n🌐 Selecione o nó para conectar:")
    for i, p in enumerate(peers, start=1):
        print(f"{i}. {p}")
    try:
        idx = int(input("Número do nó: ").strip())
        if 1 <= idx <= len(peers):
            return peers[idx - 1]
    except ValueError:
        pass
    print("❌ Opção inválida! Voltando ao menu principal.")
    return None

def get_stub(node_address):
    """Cria canal e stub gRPC para o nó especificado."""
    channel = grpc.insecure_channel(node_address)
    return voting_pb2_grpc.VotingServiceStub(channel)

def submit_vote(stub):
    voter_id = input("> Digite seu ID de eleitor: ").strip()
    print("👤 Escolha um candidato:")
    candidates = {
        1: "Caio",
        2: "Gabriel",
        3: "Luiz",
        4: "Luiza"
    }
    for cid, name in candidates.items():
        print(f"{cid}. {name}")

    try:
        choice = int(input("Digite o número do candidato: ").strip())
        if choice not in candidates:
            print("❌ Opção inválida!")
            return
        candidate_id = candidates[choice]
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
            print(f"=>  {candidate}: {votes} voto(s)")
    except grpc.RpcError as e:
        print(f"❌ Erro ao buscar resultados: {e.details()}")

def main():
    peers = load_peers()
    if not peers:
        print("🚨 Lista de nós vazia. Verifique peers.json.")
        return

    while True:
        print("\n========= MENU =========")
        print("1. Votar")
        print("2. Ver resultados")
        print("3. Sair")
        print("========================")
        opc = input("Escolha uma opção: ").strip()

        if opc == '3':
            print("👋 Encerrando cliente...")
            break

        node = pick_node(peers)
        if not node:
            continue

        stub = get_stub(node)
        if opc == '1':
            submit_vote(stub)
        elif opc == '2':
            get_results(stub)
        else:
            print("❌ Opção inválida! Tente novamente.")

if __name__ == '__main__':
    main()

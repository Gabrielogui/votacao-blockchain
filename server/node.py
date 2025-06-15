import json
import grpc
from concurrent import futures
from blockchain.blockchain import Blockchain
from cryptography.fernet import Fernet
import os

import voting_pb2
import voting_pb2_grpc
import node_pb2
import node_pb2_grpc

class VotingNode(voting_pb2_grpc.VotingServiceServicer):
    def __init__(self, node_id="Node-1", port=50051):
        self.node_id = node_id
        self.port = port
        self.votes = {}
        self.blockchain = Blockchain()

        # Carrega chave de criptografia
        with open("key.key", "rb") as f:
            key = f.read()
        self.cipher = Fernet(key)

        # Carrega lista de peers, excluindo o próprio
        base_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(base_dir, "peers.json")) as f:
            cfg = json.load(f)
        self.peers = [p for p in cfg["peers"] if p != f"localhost:{port}"]

    def broadcast_block(self, block_data):
        """Envia bloco para todos os peers via gRPC"""
        for peer in self.peers:
            try:
                channel = grpc.insecure_channel(peer)
                stub = voting_pb2_grpc.VotingServiceStub(channel)
                stub.PropagateBlock(voting_pb2.BlockMessage(data=block_data))
            except Exception as e:
                print(f"⚠️ Falha ao enviar bloco para {peer}: {e}")

    def SubmitVote(self, request, context):
        raw = f"{request.voter_id}:{request.candidate_id}".encode()
        enc = self.cipher.encrypt(raw).decode()

        self.blockchain.add_block({"vote": enc})
        self.votes[request.candidate_id] = self.votes.get(request.candidate_id, 0) + 1

        self.broadcast_block({"vote": enc})

        return voting_pb2.VoteResponse(success=True, message="Voto registrado na rede")

    def PropagateBlock(self, request, context):
        block_data = dict(request.data)
        self.blockchain.add_block(block_data)
        return voting_pb2.VoteResponse(success=True, message="Bloco adicionado")

    def QueryResults(self, request, context):
        counts = {}
        for block in self.blockchain.chain[1:]:
            enc = block.data.get("vote", "").encode()
            try:
                dec = self.cipher.decrypt(enc).decode()
                _, candidate = dec.split(":")
                counts[candidate] = counts.get(candidate, 0) + 1
            except Exception as e:
                print(f"⚠️ Erro ao descriptografar voto: {e}")
        return voting_pb2.VoteResults(results=counts)


class NodeService(node_pb2_grpc.NodeServiceServicer):
    def __init__(self, node_id="Node-1"):
        self.node_id = node_id
        self.total_votes = 0
        self.status = "Online"

    def Ping(self, request, context):
        return node_pb2.PingResponse(reply=f"Pong de {self.node_id}")

    def GetNodeStatus(self, request, context):
        return node_pb2.StatusResponse(
            node_id=self.node_id,
            total_votes=self.total_votes,
            status=self.status
        )

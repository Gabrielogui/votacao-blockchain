import node_pb2
import node_pb2_grpc
import voting_pb2
import voting_pb2_grpc

from blockchain.blockchain import Blockchain

from cryptography.fernet import Fernet



class NodeService(node_pb2_grpc.NodeServiceServicer):
    def __init__(self, node_id):
        self.node_id = node_id
        self.total_votes = 0
        self.status = "Online"

    def Ping(self, request, context):
        print(f"Ping recebido: {request.message}")
        return node_pb2.PingResponse(reply=f"Pong de {self.node_id}")

    def GetNodeStatus(self, request, context):
        return node_pb2.StatusResponse(
            node_id=self.node_id,
            total_votes=self.total_votes,
            status=self.status
        )


class VotingNode(voting_pb2_grpc.VotingServiceServicer):
    def __init__(self):
        self.votes = {}
        self.blockchain = Blockchain()

        # Carrega a chave de criptografia ao iniciar o servidor
        with open("key.key", "rb") as key_file:
            key = key_file.read()
        self.cipher = Fernet(key)  

    def SubmitVote(self, request, context):
        candidate = request.candidate_id
        voter = request.voter_id

        # Criptografa o voto
        vote_data = f"{voter}:{candidate}".encode()
        encrypted_vote = self.cipher.encrypt(vote_data)

        # Armazena o voto criptografado no blockchain
        self.blockchain.add_block({'vote': encrypted_vote.decode()})

        # Atualiza contagem local (não criptografada, apenas para resultados)
        self.votes[candidate] = self.votes.get(candidate, 0) + 1

        print(f"V Voto criptografado registrado no blockchain")
        return voting_pb2.VoteResponse(success=True, message="Voto registrado com segurança")

    def QueryResults(self, request, context):
        decrypted_votes = {}

        # Lê a chave para descriptografar os votos
        with open("key.key", "rb") as key_file:
            key = key_file.read()
        cipher = Fernet(key)

        for block in self.blockchain.chain[1:]:  # Ignora o bloco gênese
            data = block.data  # Acessa o atributo .data corretamente

            if isinstance(data, dict) and 'vote' in data:
                try:
                    encrypted_vote = data['vote'].encode()
                    decrypted = cipher.decrypt(encrypted_vote).decode()
                    voter_id, candidate_id = decrypted.split(":")
                    decrypted_votes[candidate_id] = decrypted_votes.get(candidate_id, 0) + 1
                except Exception as e:
                    print(f"X Erro ao descriptografar voto: {e}")

        return voting_pb2.VoteResults(results=decrypted_votes)

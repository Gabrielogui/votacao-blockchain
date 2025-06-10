import node_pb2
import node_pb2_grpc
import voting_pb2
import voting_pb2_grpc

from blockchain.blockchain import Blockchain


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

    def SubmitVote(self, request, context):
        candidate = request.candidate_id
        voter = request.voter_id

        # Armazena o voto no blockchain
        vote_data = {'voter_id': voter, 'candidate_id': candidate}
        self.blockchain.add_block(vote_data)

        # Atualiza contagem
        self.votes[candidate] = self.votes.get(candidate, 0) + 1

        print(f"✅ Voto registrado e salvo no blockchain: {vote_data}")
        return voting_pb2.VoteResponse(success=True, message="Voto com segurança")

    def QueryResults(self, request, context):
        return voting_pb2.VoteResults(results=self.votes)

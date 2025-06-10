import node_pb2
import node_pb2_grpc
import voting_pb2
import voting_pb2_grpc


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

    def SubmitVote(self, request, context):  # Nome certo
        candidate = request.candidate_id      # Provavelmente é candidate_id, veja seu .proto
        if candidate in self.votes:
            self.votes[candidate] += 1
        else:
            self.votes[candidate] = 1
        print(f"📥 Voto recebido: Eleitor {request.voter_id} votou em {candidate}")
        return voting_pb2.VoteResponse(message="Voto registrado com sucesso")

    def QueryResults(self, request, context):  # Nome certo
        results = [
            voting_pb2.Result(candidate_id=k, votes=v) for k, v in self.votes.items()
        ]
        return voting_pb2.VoteResults(results=results)

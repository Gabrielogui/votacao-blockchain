import grpc
import voting_pb2, voting_pb2_grpc

def submit_vote(voter_id, candidate_id):
    channel = grpc.insecure_channel('localhost:50051')
    stub = voting_pb2_grpc.VotingServiceStub(channel)
    response = stub.SubmitVote(voting_pb2.VoteRequest(voter_id=voter_id, candidate_id=candidate_id))
    print(response.message)

if __name__ == '__main__':
    # parsing de argumentos e chamada submit_vote
    pass
# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: voting.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'voting.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cvoting.proto\x12\x06voting\x1a\x1bgoogle/protobuf/empty.proto\"5\n\x0bVoteRequest\x12\x10\n\x08voter_id\x18\x01 \x01(\t\x12\x14\n\x0c\x63\x61ndidate_id\x18\x02 \x01(\t\"0\n\x0cVoteResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"p\n\x0bVoteResults\x12\x31\n\x07results\x18\x01 \x03(\x0b\x32 .voting.VoteResults.ResultsEntry\x1a.\n\x0cResultsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\"i\n\x0c\x42lockMessage\x12,\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32\x1e.voting.BlockMessage.DataEntry\x1a+\n\tDataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x32\xc3\x01\n\rVotingService\x12\x37\n\nSubmitVote\x12\x13.voting.VoteRequest\x1a\x14.voting.VoteResponse\x12;\n\x0cQueryResults\x12\x16.google.protobuf.Empty\x1a\x13.voting.VoteResults\x12<\n\x0ePropagateBlock\x12\x14.voting.BlockMessage\x1a\x14.voting.VoteResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'voting_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_VOTERESULTS_RESULTSENTRY']._loaded_options = None
  _globals['_VOTERESULTS_RESULTSENTRY']._serialized_options = b'8\001'
  _globals['_BLOCKMESSAGE_DATAENTRY']._loaded_options = None
  _globals['_BLOCKMESSAGE_DATAENTRY']._serialized_options = b'8\001'
  _globals['_VOTEREQUEST']._serialized_start=53
  _globals['_VOTEREQUEST']._serialized_end=106
  _globals['_VOTERESPONSE']._serialized_start=108
  _globals['_VOTERESPONSE']._serialized_end=156
  _globals['_VOTERESULTS']._serialized_start=158
  _globals['_VOTERESULTS']._serialized_end=270
  _globals['_VOTERESULTS_RESULTSENTRY']._serialized_start=224
  _globals['_VOTERESULTS_RESULTSENTRY']._serialized_end=270
  _globals['_BLOCKMESSAGE']._serialized_start=272
  _globals['_BLOCKMESSAGE']._serialized_end=377
  _globals['_BLOCKMESSAGE_DATAENTRY']._serialized_start=334
  _globals['_BLOCKMESSAGE_DATAENTRY']._serialized_end=377
  _globals['_VOTINGSERVICE']._serialized_start=380
  _globals['_VOTINGSERVICE']._serialized_end=575
# @@protoc_insertion_point(module_scope)

# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from google.protobuf.descriptor import (
    Descriptor as google___protobuf___descriptor___Descriptor,
    FileDescriptor as google___protobuf___descriptor___FileDescriptor,
)

from google.protobuf.message import (
    Message as google___protobuf___message___Message,
)

from google.protobuf.timestamp_pb2 import (
    Timestamp as google___protobuf___timestamp_pb2___Timestamp,
)

from typing import (
    Optional as typing___Optional,
    Text as typing___Text,
)

from typing_extensions import (
    Literal as typing_extensions___Literal,
)


builtin___bool = bool
builtin___bytes = bytes
builtin___float = float
builtin___int = int


DESCRIPTOR: google___protobuf___descriptor___FileDescriptor = ...

class SegmentEvent(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    id: typing___Text = ...
    organizationId: typing___Text = ...
    instance_id: typing___Text = ...
    accountId: typing___Text = ...
    accountUserId: typing___Text = ...
    raw: typing___Text = ...
    type: typing___Text = ...
    event: typing___Text = ...
    anonymous_id: typing___Text = ...

    @property
    def received_at(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    def __init__(self,
        *,
        id : typing___Optional[typing___Text] = None,
        organizationId : typing___Optional[typing___Text] = None,
        instance_id : typing___Optional[typing___Text] = None,
        accountId : typing___Optional[typing___Text] = None,
        accountUserId : typing___Optional[typing___Text] = None,
        raw : typing___Optional[typing___Text] = None,
        received_at : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        type : typing___Optional[typing___Text] = None,
        event : typing___Optional[typing___Text] = None,
        anonymous_id : typing___Optional[typing___Text] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"received_at",b"received_at"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"accountId",b"accountId",u"accountUserId",b"accountUserId",u"anonymous_id",b"anonymous_id",u"event",b"event",u"id",b"id",u"instance_id",b"instance_id",u"organizationId",b"organizationId",u"raw",b"raw",u"received_at",b"received_at",u"type",b"type"]) -> None: ...
type___SegmentEvent = SegmentEvent

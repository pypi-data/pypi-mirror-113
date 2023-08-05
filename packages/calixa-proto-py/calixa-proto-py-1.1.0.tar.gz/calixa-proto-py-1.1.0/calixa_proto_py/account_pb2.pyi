# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from common_pb2 import (
    Address as common_pb2___Address,
    Amount as common_pb2___Amount,
)

from google.protobuf.descriptor import (
    Descriptor as google___protobuf___descriptor___Descriptor,
    EnumDescriptor as google___protobuf___descriptor___EnumDescriptor,
    FileDescriptor as google___protobuf___descriptor___FileDescriptor,
)

from google.protobuf.internal.enum_type_wrapper import (
    _EnumTypeWrapper as google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper,
)

from google.protobuf.message import (
    Message as google___protobuf___message___Message,
)

from google.protobuf.struct_pb2 import (
    Struct as google___protobuf___struct_pb2___Struct,
)

from google.protobuf.timestamp_pb2 import (
    Timestamp as google___protobuf___timestamp_pb2___Timestamp,
)

from typing import (
    NewType as typing___NewType,
    Optional as typing___Optional,
    Text as typing___Text,
    cast as typing___cast,
)

from typing_extensions import (
    Literal as typing_extensions___Literal,
)


builtin___bool = bool
builtin___bytes = bytes
builtin___float = float
builtin___int = int


DESCRIPTOR: google___protobuf___descriptor___FileDescriptor = ...

AccountStatusValue = typing___NewType('AccountStatusValue', builtin___int)
type___AccountStatusValue = AccountStatusValue
AccountStatus: _AccountStatus
class _AccountStatus(google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper[AccountStatusValue]):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    ACCOUNT_STATUS_UNSPECIFIED = typing___cast(AccountStatusValue, 0)
    ACCOUNT_ACTIVE = typing___cast(AccountStatusValue, 1)
    ACCOUNT_SUSPENDED = typing___cast(AccountStatusValue, 2)
    ACCOUNT_DELETED = typing___cast(AccountStatusValue, 3)
ACCOUNT_STATUS_UNSPECIFIED = typing___cast(AccountStatusValue, 0)
ACCOUNT_ACTIVE = typing___cast(AccountStatusValue, 1)
ACCOUNT_SUSPENDED = typing___cast(AccountStatusValue, 2)
ACCOUNT_DELETED = typing___cast(AccountStatusValue, 3)
type___AccountStatus = AccountStatus

OpportunityStatusValue = typing___NewType('OpportunityStatusValue', builtin___int)
type___OpportunityStatusValue = OpportunityStatusValue
OpportunityStatus: _OpportunityStatus
class _OpportunityStatus(google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper[OpportunityStatusValue]):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    OPPORTUNITY_STATUS_UNSPECIFIED = typing___cast(OpportunityStatusValue, 0)
    OPPORTUNITY_STATUS_OPEN = typing___cast(OpportunityStatusValue, 1)
    OPPORTUNITY_STATUS_CLOSED = typing___cast(OpportunityStatusValue, 2)
    OPPORTUNITY_STATUS_WON = typing___cast(OpportunityStatusValue, 3)
    OPPORTUNITY_STATUS_LOST = typing___cast(OpportunityStatusValue, 4)
    OPPORTUNITY_STATUS_CLOSED_WON = typing___cast(OpportunityStatusValue, 5)
OPPORTUNITY_STATUS_UNSPECIFIED = typing___cast(OpportunityStatusValue, 0)
OPPORTUNITY_STATUS_OPEN = typing___cast(OpportunityStatusValue, 1)
OPPORTUNITY_STATUS_CLOSED = typing___cast(OpportunityStatusValue, 2)
OPPORTUNITY_STATUS_WON = typing___cast(OpportunityStatusValue, 3)
OPPORTUNITY_STATUS_LOST = typing___cast(OpportunityStatusValue, 4)
OPPORTUNITY_STATUS_CLOSED_WON = typing___cast(OpportunityStatusValue, 5)
type___OpportunityStatus = OpportunityStatus

AccountUserStatusValue = typing___NewType('AccountUserStatusValue', builtin___int)
type___AccountUserStatusValue = AccountUserStatusValue
AccountUserStatus: _AccountUserStatus
class _AccountUserStatus(google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper[AccountUserStatusValue]):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    ACCOUNT_USER_STATUS_UNSPECIFIED = typing___cast(AccountUserStatusValue, 0)
    ACCOUNT_USER_ACTIVE = typing___cast(AccountUserStatusValue, 1)
    ACCOUNT_USER_SUSPENDED = typing___cast(AccountUserStatusValue, 2)
    ACCOUNT_USER_DELETED = typing___cast(AccountUserStatusValue, 3)
    ACCOUNT_USER_INVITED = typing___cast(AccountUserStatusValue, 4)
ACCOUNT_USER_STATUS_UNSPECIFIED = typing___cast(AccountUserStatusValue, 0)
ACCOUNT_USER_ACTIVE = typing___cast(AccountUserStatusValue, 1)
ACCOUNT_USER_SUSPENDED = typing___cast(AccountUserStatusValue, 2)
ACCOUNT_USER_DELETED = typing___cast(AccountUserStatusValue, 3)
ACCOUNT_USER_INVITED = typing___cast(AccountUserStatusValue, 4)
type___AccountUserStatus = AccountUserStatus

class Opportunity(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    name: typing___Text = ...
    description: typing___Text = ...
    stage: typing___Text = ...
    type: typing___Text = ...
    next_step: typing___Text = ...
    owner: typing___Text = ...
    created_by_user_id: typing___Text = ...
    last_modified_by_user_id: typing___Text = ...
    probability: builtin___float = ...
    opportunity_status: type___OpportunityStatusValue = ...
    line_item_quantity: builtin___float = ...

    @property
    def amount(self) -> common_pb2___Amount: ...

    @property
    def closed_at(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    @property
    def last_activity_at(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    def __init__(self,
        *,
        name : typing___Optional[typing___Text] = None,
        description : typing___Optional[typing___Text] = None,
        stage : typing___Optional[typing___Text] = None,
        type : typing___Optional[typing___Text] = None,
        next_step : typing___Optional[typing___Text] = None,
        owner : typing___Optional[typing___Text] = None,
        created_by_user_id : typing___Optional[typing___Text] = None,
        last_modified_by_user_id : typing___Optional[typing___Text] = None,
        probability : typing___Optional[builtin___float] = None,
        opportunity_status : typing___Optional[type___OpportunityStatusValue] = None,
        amount : typing___Optional[common_pb2___Amount] = None,
        closed_at : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        last_activity_at : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        line_item_quantity : typing___Optional[builtin___float] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"amount",b"amount",u"closed_at",b"closed_at",u"last_activity_at",b"last_activity_at"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"amount",b"amount",u"closed_at",b"closed_at",u"created_by_user_id",b"created_by_user_id",u"description",b"description",u"last_activity_at",b"last_activity_at",u"last_modified_by_user_id",b"last_modified_by_user_id",u"line_item_quantity",b"line_item_quantity",u"name",b"name",u"next_step",b"next_step",u"opportunity_status",b"opportunity_status",u"owner",b"owner",u"probability",b"probability",u"stage",b"stage",u"type",b"type"]) -> None: ...
type___Opportunity = Opportunity

class Account(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    account_id: typing___Text = ...
    organization_id: typing___Text = ...
    canonical_id: typing___Text = ...
    name: typing___Text = ...
    status: type___AccountStatusValue = ...
    domain_name: typing___Text = ...
    created_by_user_id: typing___Text = ...

    @property
    def properties(self) -> google___protobuf___struct_pb2___Struct: ...

    @property
    def address(self) -> common_pb2___Address: ...

    @property
    def signed_up_at(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    @property
    def first_seen_at(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    @property
    def last_seen_at(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    @property
    def created_at(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    @property
    def updated_at(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    def __init__(self,
        *,
        account_id : typing___Optional[typing___Text] = None,
        organization_id : typing___Optional[typing___Text] = None,
        canonical_id : typing___Optional[typing___Text] = None,
        name : typing___Optional[typing___Text] = None,
        status : typing___Optional[type___AccountStatusValue] = None,
        domain_name : typing___Optional[typing___Text] = None,
        created_by_user_id : typing___Optional[typing___Text] = None,
        properties : typing___Optional[google___protobuf___struct_pb2___Struct] = None,
        address : typing___Optional[common_pb2___Address] = None,
        signed_up_at : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        first_seen_at : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        last_seen_at : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        created_at : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        updated_at : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"address",b"address",u"created_at",b"created_at",u"first_seen_at",b"first_seen_at",u"last_seen_at",b"last_seen_at",u"properties",b"properties",u"signed_up_at",b"signed_up_at",u"updated_at",b"updated_at"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"account_id",b"account_id",u"address",b"address",u"canonical_id",b"canonical_id",u"created_at",b"created_at",u"created_by_user_id",b"created_by_user_id",u"domain_name",b"domain_name",u"first_seen_at",b"first_seen_at",u"last_seen_at",b"last_seen_at",u"name",b"name",u"organization_id",b"organization_id",u"properties",b"properties",u"signed_up_at",b"signed_up_at",u"status",b"status",u"updated_at",b"updated_at"]) -> None: ...
type___Account = Account

class AccountAssociation(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    account_id: typing___Text = ...
    role_id: typing___Text = ...
    account_user_id: typing___Text = ...
    canonical_account_id: typing___Text = ...
    canonical_account_user_id: typing___Text = ...

    @property
    def created_at(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    @property
    def updated_at(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    def __init__(self,
        *,
        account_id : typing___Optional[typing___Text] = None,
        role_id : typing___Optional[typing___Text] = None,
        account_user_id : typing___Optional[typing___Text] = None,
        canonical_account_id : typing___Optional[typing___Text] = None,
        canonical_account_user_id : typing___Optional[typing___Text] = None,
        created_at : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        updated_at : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"created_at",b"created_at",u"updated_at",b"updated_at"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"account_id",b"account_id",u"account_user_id",b"account_user_id",u"canonical_account_id",b"canonical_account_id",u"canonical_account_user_id",b"canonical_account_user_id",u"created_at",b"created_at",u"role_id",b"role_id",u"updated_at",b"updated_at"]) -> None: ...
type___AccountAssociation = AccountAssociation

class AccountAssociationWithOrg(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    organization_id: typing___Text = ...
    account_id: typing___Text = ...
    role_id: typing___Text = ...
    account_user_id: typing___Text = ...
    canonical_account_id: typing___Text = ...
    canonical_account_user_id: typing___Text = ...

    @property
    def created_at(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    @property
    def updated_at(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    def __init__(self,
        *,
        organization_id : typing___Optional[typing___Text] = None,
        account_id : typing___Optional[typing___Text] = None,
        role_id : typing___Optional[typing___Text] = None,
        account_user_id : typing___Optional[typing___Text] = None,
        canonical_account_id : typing___Optional[typing___Text] = None,
        canonical_account_user_id : typing___Optional[typing___Text] = None,
        created_at : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        updated_at : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"created_at",b"created_at",u"updated_at",b"updated_at"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"account_id",b"account_id",u"account_user_id",b"account_user_id",u"canonical_account_id",b"canonical_account_id",u"canonical_account_user_id",b"canonical_account_user_id",u"created_at",b"created_at",u"organization_id",b"organization_id",u"role_id",b"role_id",u"updated_at",b"updated_at"]) -> None: ...
type___AccountAssociationWithOrg = AccountAssociationWithOrg

class AccountUserAssociation(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    account_user_id: typing___Text = ...
    role_id: typing___Text = ...
    canonical_account_user_id: typing___Text = ...

    def __init__(self,
        *,
        account_user_id : typing___Optional[typing___Text] = None,
        role_id : typing___Optional[typing___Text] = None,
        canonical_account_user_id : typing___Optional[typing___Text] = None,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"account_user_id",b"account_user_id",u"canonical_account_user_id",b"canonical_account_user_id",u"role_id",b"role_id"]) -> None: ...
type___AccountUserAssociation = AccountUserAssociation

class AccountUser(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    account_user_id: typing___Text = ...
    organization_id: typing___Text = ...
    email: typing___Text = ...
    status: type___AccountUserStatusValue = ...
    first_name: typing___Text = ...
    last_name: typing___Text = ...
    canonical_id: typing___Text = ...

    @property
    def last_seen_at(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    @property
    def properties(self) -> google___protobuf___struct_pb2___Struct: ...

    @property
    def signed_up_at(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    @property
    def first_seen_at(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    @property
    def created_at(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    @property
    def updated_at(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    def __init__(self,
        *,
        account_user_id : typing___Optional[typing___Text] = None,
        organization_id : typing___Optional[typing___Text] = None,
        email : typing___Optional[typing___Text] = None,
        status : typing___Optional[type___AccountUserStatusValue] = None,
        last_seen_at : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        first_name : typing___Optional[typing___Text] = None,
        last_name : typing___Optional[typing___Text] = None,
        properties : typing___Optional[google___protobuf___struct_pb2___Struct] = None,
        canonical_id : typing___Optional[typing___Text] = None,
        signed_up_at : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        first_seen_at : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        created_at : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        updated_at : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"created_at",b"created_at",u"first_seen_at",b"first_seen_at",u"last_seen_at",b"last_seen_at",u"properties",b"properties",u"signed_up_at",b"signed_up_at",u"updated_at",b"updated_at"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"account_user_id",b"account_user_id",u"canonical_id",b"canonical_id",u"created_at",b"created_at",u"email",b"email",u"first_name",b"first_name",u"first_seen_at",b"first_seen_at",u"last_name",b"last_name",u"last_seen_at",b"last_seen_at",u"organization_id",b"organization_id",u"properties",b"properties",u"signed_up_at",b"signed_up_at",u"status",b"status",u"updated_at",b"updated_at"]) -> None: ...
type___AccountUser = AccountUser

class AccountUserRole(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    organization_id: typing___Text = ...
    account_user_role_id: typing___Text = ...
    name: typing___Text = ...

    @property
    def created_at(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    @property
    def updated_at(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    def __init__(self,
        *,
        organization_id : typing___Optional[typing___Text] = None,
        account_user_role_id : typing___Optional[typing___Text] = None,
        name : typing___Optional[typing___Text] = None,
        created_at : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        updated_at : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"created_at",b"created_at",u"updated_at",b"updated_at"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"account_user_role_id",b"account_user_role_id",u"created_at",b"created_at",u"name",b"name",u"organization_id",b"organization_id",u"updated_at",b"updated_at"]) -> None: ...
type___AccountUserRole = AccountUserRole

class Teammate(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    first_name: typing___Text = ...
    last_name: typing___Text = ...
    email: typing___Text = ...

    def __init__(self,
        *,
        first_name : typing___Optional[typing___Text] = None,
        last_name : typing___Optional[typing___Text] = None,
        email : typing___Optional[typing___Text] = None,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"email",b"email",u"first_name",b"first_name",u"last_name",b"last_name"]) -> None: ...
type___Teammate = Teammate

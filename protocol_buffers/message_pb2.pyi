from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Side(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BUY: _ClassVar[Side]
    SELL: _ClassVar[Side]

class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NEW: _ClassVar[Status]
    PENDING: _ClassVar[Status]
    FILL: _ClassVar[Status]

class OrderType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LIMIT: _ClassVar[OrderType]
    MARKET: _ClassVar[OrderType]
BUY: Side
SELL: Side
NEW: Status
PENDING: Status
FILL: Status
LIMIT: OrderType
MARKET: OrderType

class OrderMessage(_message.Message):
    __slots__ = ("orderId", "externalId", "side", "rawText", "price", "amount", "status", "orderType")
    ORDERID_FIELD_NUMBER: _ClassVar[int]
    EXTERNALID_FIELD_NUMBER: _ClassVar[int]
    SIDE_FIELD_NUMBER: _ClassVar[int]
    RAWTEXT_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ORDERTYPE_FIELD_NUMBER: _ClassVar[int]
    orderId: str
    externalId: str
    side: Side
    rawText: str
    price: str
    amount: int
    status: Status
    orderType: OrderType
    def __init__(self, orderId: _Optional[str] = ..., externalId: _Optional[str] = ..., side: _Optional[_Union[Side, str]] = ..., rawText: _Optional[str] = ..., price: _Optional[str] = ..., amount: _Optional[int] = ..., status: _Optional[_Union[Status, str]] = ..., orderType: _Optional[_Union[OrderType, str]] = ...) -> None: ...

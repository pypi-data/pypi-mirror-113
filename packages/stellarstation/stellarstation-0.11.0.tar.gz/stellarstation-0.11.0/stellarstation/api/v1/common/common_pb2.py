# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: stellarstation/api/v1/common/common.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='stellarstation/api/v1/common/common.proto',
  package='stellarstation.api.v1.common',
  syntax='proto3',
  serialized_options=b'\n com.stellarstation.api.v1.commonB\013CommonProtoP\001Z9github.com/infostellarinc/go-stellarstation/api/v1/common',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n)stellarstation/api/v1/common/common.proto\x12\x1cstellarstation.api.v1.common\"\'\n\x04\x42its\x12\x0e\n\x06length\x18\x01 \x01(\r\x12\x0f\n\x07payload\x18\x02 \x01(\x0c\"+\n\x05\x41ngle\x12\x0f\n\x07\x61zimuth\x18\x01 \x01(\x01\x12\x11\n\televation\x18\x02 \x01(\x01\x42l\n com.stellarstation.api.v1.commonB\x0b\x43ommonProtoP\x01Z9github.com/infostellarinc/go-stellarstation/api/v1/commonb\x06proto3'
)




_BITS = _descriptor.Descriptor(
  name='Bits',
  full_name='stellarstation.api.v1.common.Bits',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='length', full_name='stellarstation.api.v1.common.Bits.length', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='payload', full_name='stellarstation.api.v1.common.Bits.payload', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=75,
  serialized_end=114,
)


_ANGLE = _descriptor.Descriptor(
  name='Angle',
  full_name='stellarstation.api.v1.common.Angle',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='azimuth', full_name='stellarstation.api.v1.common.Angle.azimuth', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='elevation', full_name='stellarstation.api.v1.common.Angle.elevation', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=116,
  serialized_end=159,
)

DESCRIPTOR.message_types_by_name['Bits'] = _BITS
DESCRIPTOR.message_types_by_name['Angle'] = _ANGLE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Bits = _reflection.GeneratedProtocolMessageType('Bits', (_message.Message,), {
  'DESCRIPTOR' : _BITS,
  '__module__' : 'stellarstation.api.v1.common.common_pb2'
  # @@protoc_insertion_point(class_scope:stellarstation.api.v1.common.Bits)
  })
_sym_db.RegisterMessage(Bits)

Angle = _reflection.GeneratedProtocolMessageType('Angle', (_message.Message,), {
  'DESCRIPTOR' : _ANGLE,
  '__module__' : 'stellarstation.api.v1.common.common_pb2'
  # @@protoc_insertion_point(class_scope:stellarstation.api.v1.common.Angle)
  })
_sym_db.RegisterMessage(Angle)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)

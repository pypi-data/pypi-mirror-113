# Builtin modules
from __future__ import annotations
from io import BytesIO
from math import ceil
from typing import Dict, Any, List, Tuple, IO
# Third party modules
# Local modules
# Program
VAR_ENDIANNESS   = "little"
VAR_VERSION      = b"\x01"
OP_NONE          = b"\xED"
OP_BOOL_FALSE    = b"\xEE"
OP_BOOL_TRUE     = b"\xEF"
OP_INTERGER      = b"\xF0"
OP_NEG_INTERGER  = b"\xF1"
OP_ZERO_INTERGER = b"\xF2"
OP_FLOAT         = b"\xF3"
OP_NEG_FLOAT     = b"\xF4"
OP_ZERO_FLOAT    = b"\xF5"
OP_STRING        = b"\xF6"
OP_ZERO_STRING   = b"\xF7"
OP_BYTES         = b"\xF8"
OP_ZERO_BYTES    = b"\xF9"
OP_LIST          = b"\xFA"
OP_ZERO_LIST     = b"\xFB"
OP_DICT          = b"\xFC"
OP_ZERO_DICT     = b"\xFD"
OP_SET           = b"\xFE"
OP_ZERO_SET      = b"\xFF"

class FSPackerError(Exception): pass

class UnsupportedType(FSPackerError): pass

class UnsupportedVersion(FSPackerError): pass

class InvalidOP(FSPackerError): pass

class MaxDictProtection(FSPackerError): pass

class MaxOPProtection(FSPackerError): pass

class OutOfData(FSPackerError): pass

def packMessage(message:bytes) -> bytes:
	d = len(message)
	if d < 0xFD:
		return d.to_bytes(1, VAR_ENDIANNESS) + message
	elif d <= 0xFFFF:
		return b"\xFD" + d.to_bytes(2, VAR_ENDIANNESS) + message
	elif d <= 0xFFFFFF:
		return b"\xFE" + d.to_bytes(3, VAR_ENDIANNESS) + message
	elif d <= 0xFFFFFFFF:
		return b"\xFF" + d.to_bytes(4, VAR_ENDIANNESS) + message
	raise RuntimeError("Too big data to pack")

def unpackMessage(buffer:bytes) -> Tuple[int, int]:
	d = buffer[0]
	if d < 0xFD:
		return 1, d
	elif d == 0xFD:
		return 3, int.from_bytes(buffer[1:3], VAR_ENDIANNESS)
	elif d == 0xFE:
		return 4, int.from_bytes(buffer[1:4], VAR_ENDIANNESS)
	elif d == 0xFF:
		return 5, int.from_bytes(buffer[1:5], VAR_ENDIANNESS)
	return 0, 0

def _create_vint(d:int) -> bytes:
	if d < 0xEA:
		return d.to_bytes(1, VAR_ENDIANNESS)
	elif d <= 0xFFFF:
		return b"\xEA" + d.to_bytes(2, VAR_ENDIANNESS)
	elif d <= 0xFFFFFF:
		return b"\xEB" + d.to_bytes(3, VAR_ENDIANNESS)
	elif d <= 0xFFFFFFFF:
		return b"\xEC" + d.to_bytes(4, VAR_ENDIANNESS)
	else:
		raise FSPackerError("Too big number")

class FSPacker:
	dictCounter:int
	dictByKey:Dict[Any, int]
	dictBuffer:BytesIO
	opBuffer:BytesIO
	def __init__(self) -> None:
		self.dictCounter = 0
		self.dictByKey   = {}
		self.dictBuffer  = BytesIO()
		self.opBuffer    = BytesIO()
	@classmethod
	def dump(cls, data:Any, fp:IO[bytes]) -> None:
		fp.write( cls()._parse(data) )
		return
	@classmethod
	def dumps(cls, data:Any) -> bytes:
		return cls()._parse(data)
	def _parse(self, data:Any) -> bytes:
		self._dump(data)
		return VAR_VERSION + _create_vint(len(self.dictByKey)) + self.dictBuffer.getbuffer() + self.opBuffer.getbuffer()
	def _dump(self, d:Any) -> None:
		dt = type(d)
		if d is None:
			self.opBuffer.write(OP_NONE)
			return
		if d is False:
			self.opBuffer.write(OP_BOOL_FALSE)
			return
		if d is True:
			self.opBuffer.write(OP_BOOL_TRUE)
			return
		if dt is int:
			if d == 0:
				self.opBuffer.write(OP_ZERO_INTERGER)
			else:
				self.opBuffer.write( _create_vint( self._register(d) ) )
			return
		if dt is float:
			if d == 0.0:
				self.opBuffer.write(OP_ZERO_FLOAT)
			else:
				self.opBuffer.write( _create_vint( self._register(d) ) )
			return
		if dt is str:
			if d == "":
				self.opBuffer.write(OP_ZERO_STRING)
			else:
				self.opBuffer.write( _create_vint( self._register(d) ) )
			return
		if dt in (bytes, bytearray):
			if d == b"":
				self.opBuffer.write(OP_ZERO_BYTES)
			else:
				self.opBuffer.write( _create_vint( self._register(d) ) )
			return
		if dt in (tuple, list):
			if len(d):
				self.opBuffer.write(OP_LIST + _create_vint(len(d)))
				for sd in d:
					self._dump(sd)
			else:
				self.opBuffer.write(OP_ZERO_LIST)
			return
		if dt is dict:
			if len(d):
				self.opBuffer.write(OP_DICT + _create_vint(len(d)))
				for k, v in d.items():
					self._dump(k)
					self._dump(v)
			else:
				self.opBuffer.write(OP_ZERO_DICT)
			return
		if dt is set:
			if len(d):
				self.opBuffer.write(OP_SET + _create_vint(len(d)))
				for sd in d:
					self._dump(sd)
			else:
				self.opBuffer.write(OP_ZERO_SET)
			return
		raise UnsupportedType(dt)
	def _register(self, k:Any) -> int:
		if k not in self.dictByKey:
			kt = type(k)
			s:bytes
			if kt is int:
				nl = ceil(k.bit_length() / 8)
				self.dictBuffer.write(
					(OP_INTERGER if k > 0 else OP_NEG_INTERGER) + \
					_create_vint(nl) + \
					abs(k).to_bytes(nl, VAR_ENDIANNESS)
				)
			elif kt is float:
				if k > 0:
					s = k.hex()[2:].encode()
					self.dictBuffer.write(OP_FLOAT + _create_vint(len(s)) + s)
				else:
					s = k.hex()[3:].encode()
					self.dictBuffer.write(OP_NEG_FLOAT + _create_vint(len(s)) + s)
			elif kt is str:
				s = k.encode("raw_unicode_escape")
				self.dictBuffer.write(OP_STRING + _create_vint(len(s)) + s)
			elif kt in (bytes, bytearray):
				self.dictBuffer.write(OP_BYTES + _create_vint(len(k)) + k)
			else:
				raise UnsupportedType(kt)
			self.dictByKey[k] = self.dictCounter
			self.dictCounter += 1
		return self.dictByKey[k]

class FSUnpacker:
	dict:List[Any]
	buffer:BytesIO
	maxDictSize:int
	maxOPSize:int
	OPs:Dict[bytes, Any]
	@classmethod
	def load(cls, data:IO[bytes], maxDictSize:int=0, maxOPSize:int=0) -> Any:
		return cls(BytesIO(data.read()), maxDictSize, maxOPSize)._parse()
	@classmethod
	def loads(cls, data:bytes, maxDictSize:int=0, maxOPSize:int=0) -> Any:
		return cls(BytesIO(data), maxDictSize, maxOPSize)._parse()
	def __init__(self, buffer:BytesIO, maxDictSize:int=0, maxOPSize:int=0):
		self.dict        = []
		self.buffer      = buffer
		self.maxDictSize = maxDictSize
		self.maxOPSize   = maxOPSize
		self.OPs = {
			OP_NONE:         None,
			OP_BOOL_FALSE:   False,
			OP_BOOL_TRUE:    True,
			OP_ZERO_INTERGER:0,
			OP_ZERO_FLOAT:   0.0,
			OP_ZERO_STRING:  "",
			OP_ZERO_BYTES:   b"",
		}
	def _parse(self) -> Any:
		bver = self.buffer.read(1)
		if bver != VAR_VERSION:
			raise UnsupportedVersion(bver[0])
		self._parse_dicts()
		return self._parse_ops()
	def _parse_dicts(self) -> None:
		dictLen = self._read_vint()
		if self.maxDictSize > 0 and dictLen > self.maxDictSize:
			raise MaxDictProtection()
		for i in range(dictLen):
			t = self.buffer.read(1)
			if t == b"":
				raise OutOfData()
			dl = self._read_vint()
			if t == OP_INTERGER:
				self.dict.append(int.from_bytes(self.buffer.read(dl), VAR_ENDIANNESS))
				continue
			if t == OP_NEG_INTERGER:
				self.dict.append(-int.from_bytes(self.buffer.read(dl), VAR_ENDIANNESS))
				continue
			if t == OP_FLOAT:
				self.dict.append(float.fromhex(self.buffer.read(dl).decode()))
				continue
			if t == OP_NEG_FLOAT:
				self.dict.append(-float.fromhex(self.buffer.read(dl).decode()))
				continue
			if t == OP_STRING:
				self.dict.append(self.buffer.read(dl).decode("raw_unicode_escape"))
				continue
			if t == OP_BYTES:
				self.dict.append(self.buffer.read(dl))
				continue
			raise InvalidOP(t)
	def _parse_ops(self) -> Any:
		if self.maxOPSize > 0 and self.buffer.getbuffer().nbytes-self.buffer.tell() > self.maxOPSize:
			raise MaxOPProtection()
		return self._loads()
	def _read_vint(self) -> int:
		d = self.buffer.read(1)
		if d[0] < 0xEA:
			return d[0]
		if d[0] == 0xEA:
			return int.from_bytes(self.buffer.read(2), VAR_ENDIANNESS)
		if d[0] == 0xEB:
			return int.from_bytes(self.buffer.read(3), VAR_ENDIANNESS)
		return int.from_bytes(self.buffer.read(4), VAR_ENDIANNESS)
	def _loads(self) -> Any:
		op = self.buffer.read(1)
		if op == b"":
			raise OutOfData()
		if op[0] < 0xED:
			if op[0] < 0xEA:
				return self.dict[ op[0] ]
			if op[0] == 0xEA:
				return self.dict[ int.from_bytes(self.buffer.read(2), VAR_ENDIANNESS) ]
			if op[0] == 0xEB:
				return self.dict[ int.from_bytes(self.buffer.read(3), VAR_ENDIANNESS) ]
			return self.dict[ int.from_bytes(self.buffer.read(4), VAR_ENDIANNESS) ]
		if op in self.OPs:
			return self.OPs[op]
		if op == OP_ZERO_LIST:
			return tuple()
		if op == OP_ZERO_DICT:
			return dict()
		if op == OP_ZERO_SET:
			return set()
		if op == OP_LIST:
			return tuple(( self._loads() for i in range(self._read_vint()) ))
		if op == OP_DICT:
			return dict(( (self._loads(), self._loads())  for i in range(self._read_vint()) ))
		if op == OP_SET:
			return set(( self._loads() for i in range(self._read_vint()) ))
		raise InvalidOP(op)

dump = FSPacker.dump
dumps = FSPacker.dumps
load = FSUnpacker.load
loads = FSUnpacker.loads

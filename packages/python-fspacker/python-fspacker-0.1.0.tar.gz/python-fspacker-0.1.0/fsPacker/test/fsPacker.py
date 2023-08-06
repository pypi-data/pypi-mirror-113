# Builtin modules
import unittest
from typing import Any
from tempfile import TemporaryFile
# Third party modules
# Local modules
from .. import (dump, dumps, load, loads, UnsupportedVersion, MaxDictProtection, MaxOPProtection, OutOfData, packMessage,
unpackMessage)
# Program
class FSPackerTest(unittest.TestCase):
	data:Any
	@classmethod
	def setUpClass(self) -> None:
		self.data = (
			None,
			True,
			False,
			0,
			-1,
			1,
			1<<256,
			0.0,
			0.1,
			-0.1,
			1.234e+16,
			1.234e-16,
			"",
			"test",
			"Ő",
			b'\xf0\xa4\xad\xa2'.decode(),
			b"",
			b"\x00",
			b"\x00FF00",
			tuple(),
			dict(),
			{"data":"ok"},
			{1:1},
			{(1,2,3):1},
			{1, "a", b"b"},
		)
		return None
	def test_dumpsAndLoads(self) -> None:
		d:Any
		for d in self.data:
			self.assertEqual(loads(dumps( d )), d)
		self.assertTupleEqual(loads(dumps( self.data )), self.data)
		self.assertTupleEqual(loads(dumps( (self.data, self.data)) ), (self.data, self.data))
		self.assertTupleEqual(loads(dumps( [self.data, self.data] )), (self.data, self.data))
		self.assertDictEqual(loads(dumps( {"data":self.data} )), {"data":self.data})
		return None
	def test_dumpAndLoad(self) -> None:
		with TemporaryFile() as fi:
			dump(self.data, fi)
			fi.seek(0)
			self.assertEqual(load(fi), self.data)
		return None
	def test_raises(self) -> None:
		d:bytes = dumps(self.data)
		with self.assertRaises(OutOfData):
			loads(d[:-1])
		with self.assertRaises(UnsupportedVersion):
			loads(b"\xff" + d[1:])
		d = dumps([0]*1024)
		with self.assertRaises(MaxOPProtection):
			loads(d, maxOPSize=512)
		d = dumps(list(range(1024)))
		with self.assertRaises(MaxDictProtection):
			loads(d, maxDictSize=512)
		return None
	def test_messagePackUnPack(self) -> None:
		indicatorLength:int
		messageLength:int
		d:bytes = dumps(self.data)
		packedMessage:bytes = packMessage(d)
		indicatorLength, messageLength = unpackMessage(packedMessage)
		self.assertEqual(indicatorLength, 1)
		self.assertEqual(messageLength, len(d))
		self.assertEqual(packedMessage[indicatorLength:], d)
		#
		packedMessage = packMessage(b"\x00"*0xFC)
		indicatorLength, messageLength = unpackMessage(packedMessage)
		self.assertEqual(indicatorLength, 1)
		self.assertEqual(messageLength, 0xFC)
		#
		packedMessage = packMessage(b"\x00"*0xFD)
		indicatorLength, messageLength = unpackMessage(packedMessage)
		self.assertEqual(indicatorLength, 3)
		self.assertEqual(messageLength, 0xFD)
		#
		packedMessage = packMessage(b"\x00"*0xFFFF)
		indicatorLength, messageLength = unpackMessage(packedMessage)
		self.assertEqual(indicatorLength, 3)
		self.assertEqual(messageLength, 0xFFFF)
		#
		packedMessage = packMessage(b"\x00"*0xFFFFFF)
		indicatorLength, messageLength = unpackMessage(packedMessage)
		self.assertEqual(indicatorLength, 4)
		self.assertEqual(messageLength, 0xFFFFFF)
		#
		return None

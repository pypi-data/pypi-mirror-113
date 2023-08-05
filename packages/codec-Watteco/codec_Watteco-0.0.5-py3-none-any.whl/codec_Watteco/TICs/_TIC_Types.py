# -*- coding: utf-8 -*-
from ._TIC_Tools import *
from datetime import datetime
from datetime import timedelta

_E_CONTRAT = Enum(BitsInteger(7),
	_Err          = 0,
	_AnyChange    = 1,
	_Empty        = 2,
	BT_4_SUP36    = 3,
	BT_5_SUP36    = 4,
	HTA_5         = 5,
	HTA_8         = 6,
	TJ_EJP        = 7,
	TJ_EJP_HH     = 8,
	TJ_EJP_PM     = 9,
	TJ_EJP_SD     = 10,
	TJ_LU         = 11,
	TJ_LU_CH      = 12,
	TJ_LU_P       = 13,
	TJ_LU_PH      = 14,
	TJ_LU_SD      = 15,
	TJ_MU         = 16,
	TV_A5_BASE    = 17,
	TV_A8_BASE    = 18,
	default       = Pass
)

_E_PT = Enum(BitsInteger(7),
	_Err       = 0,
	_AnyChange = 1,
	_Empty     = 2,
	___ = 3,
	ZZZ = 4,
	HC  = 5,
	HCD = 6,
	HCE = 7,
	HCH = 8,
	HH  = 9,
	HH_ = 10,
	HP  = 11,
	HP_ = 12,
	HPD = 13,
	HPE = 14,
	HPH = 15,
	JA  = 16,
	JA_ = 17,
	P__ = 18,
	PM  = 19,
	PM_ = 20,
	XXX = 21,
	default = Pass
)

_E_DIV = Enum(BitsInteger(7),
	_Err       = 0,
	_AnyChange = 1,
	_Empty     = 2,
	__ACTIF = 3,
	ACTIF = 4,
	CONSO  = 5,
	CONTROLE = 6,
	DEP = 7,
	INACTIF = 8,
	PROD  = 9,
	TEST = 10,
	kVA  = 11,
	kW = 12,
)

TYPE_E_CONTRAT = Struct(
	Embedded(
		BitStruct(
			"IsString" / Flag,
			Embedded(IfThenElse (this.IsString, 
				Struct("Size"  / BitsInteger(7)),
				Struct("Value" / _E_CONTRAT)
			))
		)
	),
	Embedded( If (this.IsString, Struct("Value" / BytesToUTF8Class(String(this._.Size))))),
)

TYPE_E_PT = Struct(
	Embedded(
		BitStruct(
			"IsString" / Flag,
			Embedded(IfThenElse (this.IsString, 
				Struct("Size"  / BitsInteger(7)),
				Struct("Value" / _E_PT)
			))
		)
	),
	Embedded( If (this.IsString, Struct("Value" / BytesToUTF8Class(String(this._.Size))))),
)


TYPE_E_DIV = Struct(
	Embedded(
		BitStruct(
			"IsString" / Flag,
			Embedded(IfThenElse (this.IsString, 
				Struct("Size"  / BitsInteger(7)),
				Struct("Value" / _E_DIV)
			))
		)
	),
	Embedded( If (this.IsString, Struct("Value" / BytesToUTF8Class(String(this._.Size))))),
)

# ADAPTER: "SYYMMDDHHMMSS" ==> 7 bytes
class SDMYhmsToUTF8Class(Adapter):
	def _encode(self, obj, context):
		res = obj[0] + ''.join([chr(int(obj[i:i+2])) for i in range(1, len(obj), 2)])	
		return res.encode()
		
	def _decode(self, obj, context):
		res="%c%02d%02d%02d%02d%02d%02d" % (obj[0],obj[1],obj[2],obj[3],obj[4],obj[5],obj[6])
		return res

TYPE_SDMYhms = SDMYhmsToUTF8Class(Bytes(7)) 


# ADAPTER: "JJ/MM/AA HH:MM:SS" ==> 6 bytes
class DMYhmsToUTF8Class(Adapter):
	def _encode(self, obj, context):
		res = ''.join([chr(int(obj[i:i+2])) for i in range(0, len(obj), 3)])	
		return res.encode()
		
	def _decode(self, obj, context):
		res="%02d/%02d/%02d %02d:%02d:%02d" % (obj[0],obj[1],obj[2],obj[3],obj[4],obj[5])
		return res
		
TYPE_DMYhms = DMYhmsToUTF8Class(Bytes(6))


TYPE_SDMYhmsU24 = Struct(
	"Date" / TYPE_SDMYhms,
	"Value" / Int24ub
)
TYPE_SDMYhmsU16 = Struct(
	"Date" / TYPE_SDMYhms,
	"Value" / Int16ub
)
TYPE_SDMYhmsU8 = Struct(
	"Date" / TYPE_SDMYhms,
	"Value" / Int8ub
) 


# Timestamp date conversions: 
#   "JJ/MM/AA hh:mm:ss" ==> nb seconds since 01/01/2000
def _StrDateToTimestamp(strDate):
	myDateRef = datetime.strptime('01/01/00 00:00:00', '%d/%m/%y %H:%M:%S')
	myDate = datetime.strptime(strDate, '%d/%m/%y %H:%M:%S')
	return int((myDate - myDateRef).total_seconds())	
#   nb seconds since 01/01/2000 ==> "JJ/MM/AA hh:mm:ss"
def _TimestampToStrDate(u32Seconds):
	myDate = datetime.strptime('01/01/00 00:00:00', '%d/%m/%y %H:%M:%S')
	myDate += timedelta(seconds=u32Seconds)
	return myDate.strftime('%d/%m/%y %H:%M:%S')


# ADAPTER: "JJ/MM/AA HH:MM:SS" <==> Timestamp (U32)
class DMYhmsToTimeStampClass(Adapter):
	def _encode(self, obj, context):
		return _StrDateToTimestamp(obj)
		
	def _decode(self, obj, context):
		return _TimestampToStrDate(obj)
		
TYPE_tsDMYhms = DMYhmsToTimeStampClass(Int32ub)

TYPE_tsDMYhms_E_PT = Struct (
	"Date" / TYPE_tsDMYhms,
	"PT" / TYPE_E_PT,
)


TYPE_U32xbe = BytesTostrHexClass(Bytes(4))

TYPE_bf8d = Int8ub


class hhmmSSSSClass(Adapter):
	#   hhmmSSSS <=> b'xxxx'
	def _encode(self, obj, context):
		res = bytearray(b'')
		if (obj[0:1] == 'N'):
			res.append(255)
		else: 
			res.append(int(obj[0:2]))
			res.append(int(obj[2:4]))
			res = res + bytearray.fromhex(obj[4:8])
		return res
				
	def _decode(self, obj, context):
		res = ""
		if (obj[0] == 0xFF):
			res += "NONUTILE"
		else:
			res += "%02d%02d%02x%02x" % (obj[0],obj[1],obj[2],obj[3])
		return res

TYPE_hhmmSSSS = Struct (
	"FirstByte" / Peek(Int8ub),
	"Value" / IfThenElse (this.FirstByte == 255,
		hhmmSSSSClass(Bytes(1)),
		hhmmSSSSClass(Bytes(4))
	)
)

TYPE_11hhmmSSSS = TYPE_hhmmSSSS[11]

'''

# Below solution DOES NOT WORK TWICE. ONLY ONCE IF end of stream !!! (cause of GreedyByte)

class _11hhmmSSSSClass_(Adapter):
	# 11 fois 
	#   hhmmSSSS <=> b'xxxx'
	#   ou
	#   NONUTILE <=> b'\xFF'
	
	def _encode(self, obj, context):
		i = 0
		res = bytearray(b'')
		for j in range(0,11):
			if (obj[i:i+1] == 'N'):
				res.append(255)
			else: 
				res.append(int(obj[i:i+2]))
				res.append(int(obj[i+2:i+4]))
				res = res + bytearray.fromhex(obj[i+4:i+8])
			i = i + 9
		return res
		
	def _decode(self, obj, context):
		i = 0
		res = ""
		for j in range(0,11):
			if (obj[i] == 0xFF):
				res += "NONUTILE"
				i = i + 1
			else:
				res += "%02d%02d%02x%02x" % (obj[i],obj[i+1],obj[i+2],obj[i+3])
				i = i + 4
			if (j < 10):
				res += ' '
		return res

TYPE_11hhmmSSSS = _11hhmmSSSSClass(GreedyBytes)
'''

TYPE_U24_E_DIV = Struct (
	"Value" / Int24ub,
	"DIV"   / TYPE_E_DIV,
)
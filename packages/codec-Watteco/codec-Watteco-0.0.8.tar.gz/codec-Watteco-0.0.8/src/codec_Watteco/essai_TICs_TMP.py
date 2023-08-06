from codec_Watteco._TestsTools import *

WTCParse("110a005700004114260c2937393c0e01e3d30000480a00163e3851ec")

exit(0)
# WTCParse("11060403150000000000803c0000000001")

# zeDict=json.loads('''
# {"EndPoint": 0, "Report": "Standard", "CommandID": "ConfigureReporting", "ClusterID": "Pressure", "tmpSize": 21, "toto": "hello", "ReportParameters": {"Batch": "Yes", "Size": 10}, "AttributeID": "MeasuredValue", "Batches": [{"FieldIndex": 0, "MinReport": {"Unit": "Seconds", "Value": 0}, "MaxReport": {"Unit": "Minutes", "Value": 60}, "Delta": 0, "Resolution": 0,"TagValue": {"TagLabel": 0, "TagSize": 1}}]}
#  '''
# )
#zeBytes=STDFrame.build(zeDict)
#print(hexlify(zeBytes))

a=Struct(
	"A" / Byte[1],
	"B" / Byte[2]
)

st = Struct(
	"remainBytes" / Peek(GreedyBytes),
	"count" / Rebuild(Byte, len_(this.items)),
	"toto" / Byte,
	"items" / GreedyRange(a),
	"offset" / Tell
)

print(st.build(
	dict(toto=10,
		items=[dict(A=b'\x01',B=b'\x01\x02'),
		dict(A=b'\x01',B=b'\x01\x02'),
		dict(A=b'\x01',B=b'\x01\x02'),
		dict(A=b'\x01',B=b'\x01\x02'),
		dict(A=b'\x0B',B=b'\x0C\x0D')])))
print(st.parse(b'\x03\x0A\x02\x03\x04\xAA'))



class BatchSizeAdapter(Adapter):
	# revert the size in configure batch cause we swapped it
	
	def _encode(self, obj, context):
		return( obj&0x08 |
			(obj&0x01)<<6 | (obj&0x02)<<4 | (obj&0x04)<<2 |
			(obj&0x10)>>2 | (obj&0x20)>>4 | (obj&0x40)>>6 ) 

		
	def _decode(self, obj, context):
		return( obj&0x08 |
			(obj&0x01)<<6 | (obj&0x02)<<4 | (obj&0x04)<<2 |
			(obj&0x10)>>2 | (obj&0x20)>>4 | (obj&0x40)>>6 ) 

BatchSize = BatchSizeAdapter(BitsInteger(7))

ReportParameters = BitsSwapped(BitStruct(
		"Batch" / Enum(Bit, Yes = 1 , No = 0),
		Embedded(
			IfThenElse(this.Batch == "Yes",
				Struct(
					"Size"	/ Rebuild(BatchSize, len_(this._._.items))
				),
				Struct(
					"NoHeaderPort" / Enum(Bit, Yes = 1 , No = 0),
					"Secured" / Enum(Bit, Yes = 1 , No = 0),
					"SecuredIfAlarm" / Enum(Bit, Yes = 1 , No = 0),
					"CauseRequest" / Enum(BitsInteger(2), No = 0, Long = 1, Short = 2),
					"Reserved" / Bit,
					"New" / Enum(Bit, Yes = 1 , No = 0)
				)
			)
		)
	)
)


st2 = Struct(
	"RP" / ReportParameters,
	"items" / GreedyRange(a),
	"offset" / Tell
)

print(st2.parse(b'\x07\x02\x03\x04\xAA'))


print(st2.build(
	dict(
		RP=dict(Batch="Yes",NoHeaderPort=0,Secured=0,SecuredIfAlarm=0,CauseRequest=0,Reserved=0,New=0),
		items=[
			dict(A=b'\x01',B=b'\x01\x02'),
			dict(A=b'\x01',B=b'\x01\x02'),
			dict(A=b'\x01',B=b'\x01\x02'),
			dict(A=b'\x01',B=b'\x01\x02'),
			dict(A=b'\x0B',B=b'\x0C\x0D')])))
			
print(st2.parse(b'\x0b\x01\x01\x02\x01\x01\x02\x01\x01\x02\x01\x01\x02\x0b\x0c\r'))


exit(0)

TICDataCBEFromBitfields = Struct(
	"BitField" / Computed("11101"),
	"Data" / TIC_STDFieldRepeater(20, TIC_STDField(CBEFields,FindFieldBitField))
)
t=TICDataCBEFromBitfields.parse(b'\x00\x01\x00\x02\xFF\xFF\x41\x42\x43\x00\x41\x42\x43\x44\x45\x46\x00')
print(t)
print(TICDataCBEFromBitfields.build(t))


TICDataCBEFromBitfields = Struct(
	"BitField" / Computed("101011"),
	Embedded(TIC_STDFieldRepeater(20, TIC_STDField(CBEFields,FindFieldBitField)))
)
t=TICDataCBEFromBitfields.parse(b'\x00\x01\xFF\xFF\x41\x42\x43\x44\x45\x46\x00\x04')
print(t)
print(TICDataCBEFromBitfields.build(t))


WTCParseBuildTest(STDFrame, "110A005405004119 260706082122 0000000D 0000000E 0000000F 41 414243444500", ERR_SYM_EXP=True)
WTCParseBuildTest(STDFrame, "110A005405004119 260607082122 0000000D 0000000E 0000000F 41 414243444500")

WTCParseBuildTest(STDFrame, "11 06 0054 39 0000 07 0000 800a 00000064 00000001 01 08 0001 800b 00000065 00000002 09")
WTCParseBuildTest(STDFrame, "11 06 0054 39 0000 07 0000 800a 00000064 00000001 01 08 0001 800b 00000065 00000002 09 00",ERR_SYM_EXP=True)
WTCParseBuildTest(STDFrame, "11 06 0054 39 0000 03 0000 800a 00000064 00000001 01 08 0001 800b 00000065 00000002 09",ERR_PARSE_EXP=True)
WTCParseBuildTest(STDFrame, "11 06 0054 39 0000 07 0000 800a 00000064 00000001 01 08 0001 800b 00000065 00000002 ",ERR_PARSE_EXP=True)
WTCParseBuildTest(STDFrame, "11 06 0054 39 0000 02 0000 800a 00000064 00000001 01 08 0001 800b 00000065 00000002 09",ERR_PARSE_EXP=True)

WTCParse("11 06 00 54 55 00 00 06 80 0a 80 78 00 00 00 01 00 00 00 01 02 07 80 0a 80 78 00 00 00 01 00 00 00 01 0a 08 80 0a 80 78 00 00 00 01 00 00 00 01 12")

#TIC PMEPMI, STD, 31 premiers champs + PMAX_s et PMAX_i
WTCParseBuildTest(STDFrame, 
"11 06 0057 00 0000 41 8001 800A"  +                     "78" + #120 (Sum)
"05FFFFFFFF 090C000000FFFFFFFF"                               + # 14
"06 010203040506 04 010220010203 800001 800002 800003 800004" + # 26
"800001 800002 800003 800004 04 05 8441424344 05"             + # 20 
"0000000A05 0000000B06 0000000C07 0000000D08"                 + # 20 
"05 06 010101020202 FFFF"                                     + # 10 
"1000 0000000A 2000 3000 0000000B 4000 5000 0000000C "        + # 22 
"00000E 08 00000F 09"                                         + #  8
"")

#TIC PMEPMI, STD, 31 premiers champs + PMAX_s et PMAX_i
WTCParse( 
"11 06 0057 00 0000 41 8001 800A"  +                     "78" + #120 (Sum)
"05FFFFFFFF 090C000000FFFFFFFF"                               + # 14
"06 010203040506 04 010220010203 800001 800002 800003 800004" + # 26
"800001 800002 800003 800004 04 05 8441424344 05"             + # 20 
"0000000A05 0000000B06 0000000C07 0000000D08"                 + # 20 
"05 06 010101020202 FFFF"                                     + # 10 
"1000 0000000A 2000 3000 0000000B 4000 5000 0000000C "        + # 22 
"00000E 08 00000F 09"                                         + #  8
"")

zeDict=json.loads('''
{
  "EndPoint": 0,
  "Report": "Standard",
  "CommandID": "ConfigureReporting",
  "ClusterID": "TIC_PMEPMI",
  "ReportParameters": {
    "Batch": "No",
    "NoHeaderPort": "No",
    "Secured": "No",
    "SecuredIfAlarm": "No",
    "CauseRequest": "No",
    "Reserved": 0,
    "New": "No"
  },
  "Instance": 0,
  "AttributeID": "General",
  "AttributeType": "ByteString",
  "MinReport": {
    "Unit": "Minutes",
    "Value": 1
  },
  "MaxReport": {
    "Unit": "Minutes",
    "Value": 10
  },
  "Data": {
    "TICReportSelector": {
      "DescHeader": {
        "Obsolete": "No",
        "Report": "Standard",
        "PresentField": "DescVarBitfield",
        "Size": 2
      },
      "BitField": "0011000100011000"
    },
    "TICDataSelector": {
      "DescHeader": {
        "Obsolete": "No",
        "Report": "Standard",
        "PresentField": "DescVarBitfield",
        "Size": 2
      },
      "BitField": "0001000100011000"
    },
    "TICCriteriaFields": {
      "DATE": "01/02/32 01:02:03",
      "EAPP_s": 8388612,
      "EAPP_i": 8388613,
      "PTCOUR1": {
        "IsString": false,
        "Value": "ZZZ"
      }
    }
  }
}
''');


zeDict=json.loads('''
{
  "EndPoint": 0,
  "Report": "Standard",
  "CommandID": "ConfigureReporting",
  "ClusterID": "TIC_PMEPMI",
  "ReportParameters": {
    "Batch": "No",
    "NoHeaderPort": "No",
    "Secured": "No",
    "SecuredIfAlarm": "No",
    "CauseRequest": "No",
    "Reserved": 0,
    "New": "No"
  },
  "Instance": 0,
  "AttributeID": "General",
  "AttributeType": "ByteString",
  "MinReport": {
    "Unit": "Minutes",
    "Value": 1
  },
  "MaxReport": {
    "Unit": "Minutes",
    "Value": 10
  },
  "Data": {
    "TICReportSelector": {
      "DescHeader": {
        "Obsolete": "No",
        "Report": "Standard",
        "PresentField": "DescVarBitfield",
        "Size": 3
      },
      "BitField": "0011000100011"
    },
    "TICDataSelector": {
      "DescHeader": {
        "Obsolete": "No",
        "Report": "Standard",
        "PresentField": "DescVarIndexes",
        "Size": 5
      },
      "BitField": "0001000100011"
    },
    "TICCriteriaFields": {
      "DATE": "01/02/32 01:02:03",
      "EAPP_s": 8388612,
      "EAPP_i": 8388613,
      "PTCOUR1": {
        "IsString": false,
        "Value": "ZZZ"
      }
    }
  }
}
''');

# print(zeDict)
zeBytes=STDFrame.build(zeDict)
print(hexlify(zeBytes))
print(STDFrame.parse(zeBytes))

WTCParse( "11 08 0057 00 0000")
WTCParse( "11 08 0057 01 0000")
WTCParse( "11 08 0057 80 0000")
WTCParseBuildTest(STDFrame,"11 08 0057 80 0000")




zeDict=json.loads('''
	{
		"EndPoint": 0, 
		"Report": "Standard", 
		"CommandID": "ReadReportingConfiguration", 
		"ClusterID": "TIC_PMEPMI",
		"ReportParameters": { 
			"Batch": "No", 
			"NoHeaderPort": "No", 
			"Secured": "No", 
			"SecuredIfAlarm": "No", 
			"CauseRequest": "No", 
			"Reserved": 0, 
			"New": "No"
		}, 
		"Instance": 0, 
		"AttributeID": "General"
	}
'''
)

zeBytes=STDFrame.build(zeDict)
print(hexlify(zeBytes))

'''
OK      11080057010000          {"EndPoint": 0, "Report": "Standard", "CommandID": "ReadReportingConfiguration", "ClusterID": "TI
C_PMEPMI", "ReportParameters": {"Batch": "Yes", "Size": 0}, "Instance": 0, "AttributeID": "General"}
OK      11080057800000          {"EndPoint": 0, "Report": "Standard", "CommandID": "ReadReportingConfiguration", "ClusterID": "TI
C_PMEPMI", "ReportParameters": {"Batch": "No", "NoHeaderPort": "No", "Secured": "No", "SecuredIfAlarm": "No", "CauseRequest": "No
", "Reserved": 0, "New": "Yes"}, "Instance": 0, "AttributeID": "General"}

'''

WTCParse("11060403150000000000803c0000000001")
WTCParse("11060400150000000000803c0000000001")


zeDict=json.loads('''
 {"EndPoint": 0, "Report": "Standard", "CommandID": "ConfigureReporting", "ClusterID": "Pressure", "ReportParameters": {"Batch": "Yes", "Size": 0}, "AttributeID": "MeasuredValue", "Batches": [{"FieldIndex": 0, "MinReport": {"Unit": "Seconds", "Value": 0}, "MaxReport": {"Unit":"Minutes", "Value": 60}, "Delta": 0, "Resolution": 0, "TagValue": {"TagLabel": 0, "TagSize": 1}}]}
 '''
)
zeBytes=STDFrame.build(zeDict)
print(hexlify(zeBytes))
 
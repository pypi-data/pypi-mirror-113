from codec_Watteco._TestsTools import *

from codec_Watteco.ZCL_FRAME import *
from codec_Watteco.ZCL import *
import json 
import sys
from codec_Watteco.WTC_CodecTools import * 
from construct import *
import time

def function(trame):
	var = json.dumps(STDFrame.parse(hexlify(trame) ),indent=1)
	sys.stdout.write(var)

a = { "EndPoint": 0, "Report": "Standard", "CommandID": "ClusterSpecificCommand", "ClusterID": "OnOff", "Data": [ 1 ] }
b = { "EndPoint": 0, "Report": "Standard", "CommandID": "ConfigureReporting", "ClusterID": "PowerQuality", "AttributeID": "CurrentValues", "ReportParameters": { "New": "No", "Reserved": 0, "CauseRequest": "No", "SecuredIfAlarm": "No", "Secured": "No", "NoHeaderPort": "No", "Batch": "No" }, "AttributeType": "ByteString", "MinReport": { "Value": 60, "Unit": "Minutes" }, "MaxReport": { "Value": 60, "Unit": "Minutes" }, "Data": { "Freq": 0, "FreqMin": 0, "FreqMax": 0, "Vrms": 0, "VrmsMin": 0, "VrmsMax": 0, "Vpeak": 0, "VpeakMin": 1, "VpeakMax": 0, "OverVoltageNumber": 1, "SagNumber": 0, "BrownoutNumber": 1 } }
c = { "EndPoint": 0, "Report": "Standard", "CommandID": "ConfigureReporting", "ClusterID": "SimpleMetering", "AttributeID": "CurrentMetering", "ReportParameters": { "New": "No", "Reserved": 0, "CauseRequest": "No", "SecuredIfAlarm": "No", "Secured": "No", "NoHeaderPort": "No", "Batch": "No" }, "AttributeType": "ByteString", "MinReport": { "Value": 60, "Unit": "Minutes" }, "MaxReport": { "Value": 60, "Unit": "Minutes" }, "Data": { "ActiveEnergy": 0, "ReactiveEnergy": 0, "NbMinutes": 0, "ActivePower": 0, "ReactivePower": 0 } }
trame = bytearray(STDFrame.build(b))
print(trame)
if(trame[4] == 1 and trame[2] == 6 ):
	trame[4] = ((len(trame)-7) << 1) + 1
print(hexlify(trame))

# batch config: 3106000c1d0055008001802340a000003f8000000B
#1106800a800000410000803c1610000000000400000005011100000000010000000301
#3106000c1d0055008001802340a000003f8000000B

# Tout pleins de trame batch
#11060050800006410000803c0710020000000001 => OK
# 1106000f1d040200001e8028000000370000000101 => OK
# 1106040215000000801E803C0000000A02
# 1106040515000000801E803C000000640A
# 1106005015000604A760A7600000000112
# 1106005015000604A760A7600000000112 Tension pile
#1106040215000000800A803C0000000A01
 
 
WTCParse(
"11 06 0054 00 0200 41 8001 800A"             "16" + # 22 (Sum)
"260607082122"                                     + #  6
"24060708 0000000D 0000000E 0000000F"              + # 16
"")
# ==> {"EndPoint": 0, "Report": "Standard", "CommandID": "ReportAttributes", "ClusterID": "TIC_CBE", "Instance": 5, "AttributeID": "General", "AttributeType": "ByteString", "Data": {"TICDataSelector": {"DescHeader": {"Obsolete": "No", "Report": "Standard", "PresentField": "DescVarIndexes", "Size": 6}, "BitField": "0000001110000000000000000000000001100000"}, "TICDataFields": {"BASE": 13, "HCHC": 14, "HCHP": 15, "HHPHC": "A", "MOTDETAT": "ABCDE"}}, "Cause": []}

WTCParse("11 06 0054 39 0000 07 0000 800a 00000064 00000001 01 08 0001 800b 00000065 00000002 09")
# ==> {"EndPoint": 0, "Report": "Standard", "CommandID": "ConfigureReporting", "ClusterID": "TIC_CBE", "ReportParameters": {"Batch": "Yes", "Size": 28}, "Instance": 0, "AttributeID": "General", "Batches": [{"FieldIndex": 7, "MinReport": {"Unit": "Seconds", "Value": 0}, "MaxReport": {"Unit": "Minutes", "Value": 10}, "Delta": 100, "Resolution": 1, "TagValue": {"TagLabel": 0, "TagSize": 1}}, {"FieldIndex": 8, "MinReport": {"Unit": "Seconds", "Value": 1}, "MaxReport": {"Unit": "Minutes", "Value": 11}, "Delta": 101, "Resolution": 2, "TagValue": {"TagLabel": 1, "TagSize": 1}}]}


WTCParse("110A005405004119 260607082122 0000000D 0000000E 0000000F 41 414243444500")
# ==> {"EndPoint": 0, "Report": "Standard", "CommandID": "ReportAttributes", "ClusterID": "TIC_CBE", "Instance": 5, "AttributeID": "General","AttributeType": "ByteString", "Data": {"TICDataSelector": {"DescHeader": {"Obsolete": "No", "Report": "Standard", "PresentField": "DescVarIndexes", "Size": 6}, "BitField": "0000001110000000000000000000000001100000"}, "TICDataFields": {"BASE": 13, "HCHC": 14, "HCHP": 15, "HHPHC": "A", "MOTDETAT": "ABCDE"}}, "Cause": []}


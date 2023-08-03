import minimalmodbus
import time
import struct
import sys
import wago
from pathlib import Path

# port name, slave address (in decimal)
meter = minimalmodbus.Instrument('/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AQ01JZVA-if00-port0', 7)
meter.serial.baudrate = 115200
meter.serial.bytesize = 8
meter.serial.parity   = minimalmodbus.serial.PARITY_NONE
meter.serial.stopbits = 1
meter.mode = minimalmodbus.MODE_RTU
meter.serial.timeout  = 1
#meter.close_port_after_each_call = True
#meter.debug = True
#print(meter)
#r = 74
#df = meter.read_float(r, 4, 2, minimalmodbus.BYTEORDER_BIG )
#print( 'big', df )
#df = meter.read_float(r, 4, 2, minimalmodbus.BYTEORDER_LITTLE )
#print( 'little', df )
#df = meter.read_float(r, 4, 2, minimalmodbus.BYTEORDER_BIG_SWAP )
#print( 'bigswap', df )
#df = meter.read_float(r, 4, 2, minimalmodbus.BYTEORDER_LITTLE_SWAP )
#print( 'littleswap', df )
#sys.exit()

skipNext = False
#if ( len(sys.argv) > 1 ):
#	start = int(sys.argv[1])

#date = [ 22 * 256 + 7, 11 * 256 + 5, 17 * 256 + 36 ]
#meter.write_registers(62, date )
data = [
	[ 0x4000,	0x34,	[] ],
	[ 0x5000,	0x38,	[] ],
	[ 0x6000,	0x24,	[] ],
	[ 0x6024,	0x4D,	[] ],
	[ 0x6071,	0x20,	[] ]
]

for d in data:
	# Start register, number, function code
	d[2] = meter.read_registers(d[0], d[1], 3)
	# Register number, number of decimals, function code
	#print( meter.read_register(currentRegister) )
	n = len(d[2])
	for i in range(0,n):
		j = i + d[0]
		if ( skipNext == True ):
			skipNext = False
			continue
		raw = d[2][i]
		val = raw
		hrval = raw
		name = ''
		unit = '  '
		if ( j in wago.ref_registers ):
			r = wago.ref_registers[j]
			name = r[wago.reg_name]
			unit = r[wago.reg_unit]
			if ( r[wago.reg_type] == 's16' ):
				val = raw - ((raw & 0x8000) << 1)
			elif ( r[wago.reg_type] == 'f32' ):
				val = struct.unpack('f', struct.pack('I', (raw << 16) + d[2][i+1] ))[0]
				skipNext = True
			hrval = (val+r[wago.reg_offset]) * r[wago.reg_scale]
		
		if ( True or raw > 0 or j in wago.ref_registers ):
			print( 'x{register:04X} x{hex:04X} {raw:5n} {val:10.2f} {hrval:10.2f} {unit:5} - {name}'.format(register=j,hex=raw,raw=raw,val=val,hrval=hrval,unit=unit,name=name) )

	#sys.exit()
import minimalmodbus
import time
import struct
import sys
import styleboiler
from pathlib import Path

# port name, slave address (in decimal)
meter = minimalmodbus.Instrument('/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A10NBJFH-if00-port0', 1)
meter.serial.baudrate = 9600
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
	[ 0,	7,	[] ],
	[ 100,	20,	[] ]
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
		if ( j in styleboiler.ref_registers ):
			r = styleboiler.ref_registers[j]
			name = r[styleboiler.reg_name]
			unit = r[styleboiler.reg_unit]
			if ( r[styleboiler.reg_type] == 's16' ):
				val = raw - ((raw & 0x8000) << 1)
			elif ( r[styleboiler.reg_type] == 'f32' ):
				val = struct.unpack('f', struct.pack('I', (raw << 16) + d[2][i+1] ))[0]
				skipNext = True
			hrval = (val+r[styleboiler.reg_offset]) * r[styleboiler.reg_scale]
		
		if ( True or raw > 0 or j in styleboiler.ref_registers ):
			print( 'x{register:04X} x{hex:04X} b{bin:016b} {raw:5n} {val:10.2f} {hrval:10.2f} {unit:5} - {name}'.format(register=j,hex=raw,bin=raw,raw=raw,val=val,hrval=hrval,unit=unit,name=name) )

	#sys.exit()
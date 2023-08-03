import minimalmodbus
import time
import struct
import sys
import eastron
from pathlib import Path

# port name, slave address (in decimal)
inverter = minimalmodbus.Instrument('/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A10NBJFH-if00-port0', 6)
inverter.serial.baudrate = 38400
inverter.serial.bytesize = 8
inverter.serial.parity   = minimalmodbus.serial.PARITY_NONE
inverter.serial.stopbits = 1
inverter.mode = minimalmodbus.MODE_RTU
inverter.serial.timeout  = 1
#inverter.close_port_after_each_call = True
#inverter.debug = True
#print(inverter)
#r = 74
#df = inverter.read_float(r, 4, 2, minimalmodbus.BYTEORDER_BIG )
#print( 'big', df )
#df = inverter.read_float(r, 4, 2, minimalmodbus.BYTEORDER_LITTLE )
#print( 'little', df )
#df = inverter.read_float(r, 4, 2, minimalmodbus.BYTEORDER_BIG_SWAP )
#print( 'bigswap', df )
#df = inverter.read_float(r, 4, 2, minimalmodbus.BYTEORDER_LITTLE_SWAP )
#print( 'littleswap', df )
#sys.exit()

currentRegister = 0
d = 80
skipNext = False
#if ( len(sys.argv) > 1 ):
#	start = int(sys.argv[1])

#date = [ 22 * 256 + 7, 11 * 256 + 5, 17 * 256 + 36 ]
#inverter.write_registers(62, date )

while currentRegister <= 500:
	# Register number, number of decimals, function code
	#print( inverter.read_register(currentRegister) )
	data = inverter.read_registers(currentRegister, d, 4)
	n = len(data)
	for i in range(0,n):
		if ( skipNext == True ):
			skipNext = False
			continue
		register = i + currentRegister
		raw = data[i]
		val = raw
		hrval = raw
		if ( i % 2 == 1 ):
			f = data[i] + (data[i-1] << 16 )
			#hrval = struct.unpack('f', struct.pack('I', f))[0]
		name = ''
		unit = '  '
		if ( register in eastron.ref_registers ):
			r = eastron.ref_registers[register]
			name = r[eastron.reg_name]
			unit = r[eastron.reg_unit]
			if ( r[3] == 's16' ):
				val = raw - ((raw & 0x8000) << 1)
			elif ( r[3] == 'f32' ):
				val = struct.unpack('f', struct.pack('I', (raw << 16) + data[i+1] ))[0]
				skipNext = True
			hrval = (val+r[eastron.reg_offset]) * r[eastron.reg_scale]
		
		if ( raw > 0 or register in eastron.ref_registers ):
			print( '{register:3n} x{hex:04X} {raw:5n} {val:10.2f} {hrval:10.2f} {unit:5} - {name}'.format(register=register,hex=raw,raw=raw,val=val,hrval=hrval,unit=unit,name=name) )

	currentRegister += d
	#sys.exit()
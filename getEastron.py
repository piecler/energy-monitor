#!/usr/bin/env python
import minimalmodbus
import time
import decimal
import struct
import sys
import mysql.connector
import eastron
from pathlib import Path

p = Path(__file__).with_name('db.cred')
f = open(p.absolute(), 'r')
cred = f.read().splitlines()

mydb = mysql.connector.connect(
  host=cred[0],
  user=cred[1],
  password=cred[2],
  database=cred[3]
)

mycursor = mydb.cursor()

sql_fields = []
sql_values = []
for register in eastron.registers:
	if ( register[eastron.reg_log] == 1 ):
		sql_fields.append( ' `' + register[eastron.reg_db_field] + '`' )
		sql_values.append( ' %s' )

sqlInsertData = 'INSERT INTO `em` ( `timestamp`,`unix_ts`,{fields} ) VALUES ( NOW(6),FLOOR(UNIX_TIMESTAMP(NOW(6))*1000),{values} )'.format(
		fields=",".join(sql_fields),
		values=",".join(sql_values)
	)

# get last data timestamp
lastLogTimestamp = time.time()
mycursor.execute("SELECT FLOOR(`unix_ts`/1000) FROM `em` ORDER BY `unix_ts` DESC LIMIT 1")
myresult = mycursor.fetchall()
for x in myresult:
	lastLogTimestamp = x[0]

lastLogTimestamp = float(lastLogTimestamp)

#sys.exit()

# port name, slave address (in decimal)
meter = minimalmodbus.Instrument('/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A10NBJFH-if00-port0', 6)
meter.serial.baudrate = 38400
meter.serial.bytesize = 8
meter.serial.parity   = minimalmodbus.serial.PARITY_NONE
meter.serial.stopbits = 1
meter.mode = minimalmodbus.MODE_RTU
meter.serial.timeout  = 1
meter.close_port_after_each_call = True
#meter.debug = True
#print(meter)

startTime = time.time()
# avg over samples
samples = 0
errors = 0
while True:
	data = [
		[ 0,	42,	[] ],
		[ 70,	2,	[] ],
		[ 200,	6,	[] ],
		[ 224,	2,	[] ],
		[ 346,	12,	[] ]
	]
	start = 0
	d = 100
	#if ( len(sys.argv) > 1 ):
	#	start = int(sys.argv[1])

	try:
		#while start < 398:
		for d in data:
			# Start register, number, function code
			d[2] = meter.read_registers(d[0], d[1], 4)
			#print(d[2])
			n = len(d[2])
			for i in range(0,n):
				j = i + d[0]
				if ( j in eastron.ref_registers ):
					r = eastron.ref_registers[j]
					if ( r[eastron.reg_type] == 'f32' ):
						r[eastron.reg_value] = struct.unpack('f', struct.pack('I', (d[2][i] << 16) + d[2][i+1] ))[0]
					else:
						r[eastron.reg_value] = d[2][i]

			#start += d
		samples += 1
		#register = 1000
		#val = eastron.ref_registers[register][eastron.reg_value]
		#print( '{register:3n} {val:8.2f}'.format(register=register,val=val) )

		# log to db
		now = time.time()
		if ( (now - startTime > 9.5) or True ):
			#log null row
			if ( now - lastLogTimestamp > 30 ):
				val = []
				val.append( round( (now + lastLogTimestamp) / 2 ) )
				val.append( round( 1000 * ((now + lastLogTimestamp) / 2) ) )
				mycursor.execute("INSERT INTO `em` ( `timestamp`, `unix_ts` ) VALUES ( FROM_UNIXTIME(%s), %s )", val)
				mydb.commit()

			#insert to db
			val = []
			for r in eastron.registers:
				if ( r[eastron.reg_log] == 1 ):
					if ( samples > 1 ):
						val.append( r[eastron.reg_value] / samples )
					else:
						val.append( r[eastron.reg_value] )
				r[eastron.reg_value] = 0

			#print( val )
			mycursor.execute(sqlInsertData, val)
			mydb.commit()

			lastLogTimestamp = now

			samples = 0
			errors = 0
			startTime = time.time()
	except Exception as error:
		print( "[!] Exception occurred: ", error )
		startTime = time.time()
		samples = 0
		for r in eastron.registers:
			r[eastron.reg_value] = 0
		errors += 1
		if ( errors > 100 ):
			print("getEastron: exit, too many errors")
			sys.exit()
		time.sleep(2)

	#time.sleep(1)
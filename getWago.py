#!/usr/bin/env python
import minimalmodbus
import time
import decimal
import struct
import sys
import mysql.connector
import wago
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
for register in wago.registers:
	if ( register[wago.reg_log] == 1 ):
		sql_fields.append( ' `' + register[wago.reg_db_field] + '`' )
		sql_values.append( ' %s' )

sqlInsertData = 'INSERT INTO `em_wago` ( `timestamp`,`unix_ts`,{fields} ) VALUES ( NOW(6),FLOOR(UNIX_TIMESTAMP(NOW(6))*1000),{values} )'.format(
		fields=",".join(sql_fields),
		values=",".join(sql_values)
	)

# get last data timestamp
lastLogTimestamp = time.time()
mycursor.execute("SELECT FLOOR(`unix_ts`/1000) FROM `em_wago` ORDER BY `unix_ts` DESC LIMIT 1")
myresult = mycursor.fetchall()
for x in myresult:
	lastLogTimestamp = x[0]

lastLogTimestamp = float(lastLogTimestamp)

#print( lastLogTimestamp )
#sys.exit()

# port name, slave address (in decimal)
meter = minimalmodbus.Instrument('/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AQ01JZVA-if00-port0', 7)
meter.serial.baudrate = 115200
meter.serial.bytesize = 8
meter.serial.parity   = minimalmodbus.serial.PARITY_NONE
meter.serial.stopbits = 1
meter.mode = minimalmodbus.MODE_RTU
meter.serial.timeout  = 1
meter.close_port_after_each_call = True
#meter.debug = True
#print(meter)

#print( meter.read_registers(0x4000, 10, 3) )
#sys.exit()

startTime = time.time()
lastPurge = time.time()
# avg over samples
samples = 0
errors = 0
while True:
	data = [
		#[ 0x4000,	0x34,	[] ],
		[ 0x5000,	0x38,	[] ],
		[ 0x6000,	0x24,	[] ],
		#[ 0x6024,	0x4D,	[] ],
		#[ 0x6071,	0x20,	[] ]
	]
	#if ( len(sys.argv) > 1 ):
	#	start = int(sys.argv[1])

	try:
		#while start < 398:
		for d in data:
			# Start register, number, function code
			d[2] = meter.read_registers(d[0], d[1], 3)
			#print(d[2])
			n = len(d[2])
			for i in range(0,n):
				j = i + d[0]
				if ( j in wago.ref_registers ):
					r = wago.ref_registers[j]
					if ( r[wago.reg_type] == 'f32' ):
						r[wago.reg_value] = struct.unpack('f', struct.pack('I', (d[2][i] << 16) + d[2][i+1] ))[0]
					else:
						r[wago.reg_value] = d[2][i]

		samples += 1
		#register = 1000
		#val = wago.ref_registers[register][wago.reg_value]
		#print( '{register:3n} {val:8.2f}'.format(register=register,val=val) )

		# log to db
		now = time.time()
		if ( (now - startTime > 9.5) or True ):
			#log null row
			if ( now - lastLogTimestamp > 30 ):
				val = []
				val.append( round( (now + lastLogTimestamp) / 2 ) )
				val.append( round( 1000 * ((now + lastLogTimestamp) / 2) ) )
				mycursor.execute("INSERT INTO `em_wago` ( `timestamp`, `unix_ts` ) VALUES ( FROM_UNIXTIME(%s), %s )", val)
				mydb.commit()

			#insert to db
			val = []
			for r in wago.registers:
				if ( r[wago.reg_log] == 1 ):
					if ( samples > 1 ):
						val.append( r[wago.reg_value] / samples )
					else:
						val.append( r[wago.reg_value] )
				r[wago.reg_value] = 0

			#print( val )
			mycursor.execute(sqlInsertData, val)
			mydb.commit()

			lastLogTimestamp = now

			samples = 0
			errors = 0
			startTime = time.time()
		if ( (now - lastPurge > 100) ):
			#purge data older than a week
			mycursor.execute("DELETE FROM `em_wago` WHERE unix_ts < UNIX_TIMESTAMP(NOW())*1000-7*24*3600*1000 LIMIT 10000")
			mydb.commit()
			lastPurge = time.time()
	except Exception as error:
		print( "[!] Exception occurred: ", error )
		startTime = time.time()
		samples = 0
		for r in wago.registers:
			r[wago.reg_value] = 0
		errors += 1
		if ( errors > 100 ):
			print("getWago: exit, too many errors")
			sys.exit()
		time.sleep(2)

	time.sleep(0.5)
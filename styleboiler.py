reg_num = 0
reg_db_field = 1
reg_name = 2
reg_type = 3
reg_offset = 4
reg_scale = 5
reg_unit = 6
reg_log = 7
reg_value = 8

registers = (
	[ 0x0000,	'power',				'Power on/off bit 0',											'b16', 0, 1.00,		'',		1, 0 ],
	[ 0x0001,	'mode',					'Mode 1:invalid, 2:hybird, 3:e-heater, 4:vacation',				'u16', 0, 1.00,		'',		1, 0 ],
	[ 0x0002,	'Ts',					'Target temperature',											'tmp', -30, 0.50,	'°C',	1, 0 ],
	[ 0x0003,	'flags',				'Flags',														'b16', 0, 1.00,		'',		1, 0 ],
	[ 0x0004,	'hour',					'Time hour',													'u16', 0, 1.0,		'',		1, 0 ],
	[ 0x0005,	'minute',				'Time minute',													'u16', 0, 1.0,		'',		1, 0 ],
	[ 0x0006,	'',						'Unknown',														'u16', 0, 1.0,		'',		0, 0 ],
	[ 0x0064,	'mode_op',				'Operation mode 1:invalid, 2:hybird, 3:e-heater, 4:vacation',	'b16', 0, 1.00,		'',		1, 0 ],
	[ 0x0065,	'T5U',					'Temperature tank upper',										'tmp', -30, 0.50,	'°C',	1, 0 ],
	[ 0x0066,	'T5L',					'Temperature tank lower',										'tmp', -30, 0.50,	'°C',	1, 0 ],
	[ 0x0067,	'T3',					'Temperature condenser',										'tmp', -30, 0.50,	'°C',	1, 0 ],
	[ 0x0068,	'T4',					'Temperature ambient',											'tmp', -30, 0.50,	'°C',	1, 0 ],
	[ 0x0069,	'Tp',					'Temperature compressor exhaust',								'u16', 0, 1.0,		'°C',	1, 0 ],
	[ 0x006a,	'Th',					'Temperature suction',											'tmp', -30, 0.50,	'°C',	1, 0 ],
	[ 0x006b,	'pmv',					'PMV opening valve',											'u16', 0, 1.0,		'',		1, 0 ],
	[ 0x006c,	'current',				'Current',														'u16', 0, 1.0,		'A',	1, 0 ],
	[ 0x006d,	'status1',				'Status bits on/off',											'b16', 0, 1.0,		'',		1, 0 ],
	[ 0x006e,	'error',				'Error code',													'u16', 0, 1.0,		'',		1, 0 ],
	[ 0x006f,	'Ts_max',				'Target temperature max',										'u16', 0, 1.0,		'°C',	1, 0 ],
	[ 0x0070,	'Ts_min',				'Target temperature min',										'u16', 0, 1.0,		'°C',	1, 0 ],
	[ 0x0071,	'Tx',					'Display temperature',											'tmp', -30, 0.50,	'°C',	1, 0 ],
	[ 0x0072,	'rhw',					'Remaining hot water',											'u16', 0, 1.0,		'',		1, 0 ],
	[ 0x0073,	'status2',				'Status bits on/off',											'b16', 0, 1.0,		'',		1, 0 ],
	[ 0x0074,	'compressor_runtime',	'Compressor running time',										'b16', 0, 1.0,		'sec',	1, 0 ],
	[ 0x0075,	'',						'Model 1=190,2=300',											'u16', 0, 1.0,		'',		0, 0 ],
	[ 0x0076,	'',						'Main PCB firmware version',									'u16', 0, 1.0,		'',		0, 0 ],
	[ 0x0077,	'',						'Wire controller firmware version',								'u16', 0, 1.0,		'',		0, 0 ],
)

ref_registers = {}

for register in registers:
	ref_registers[ register[0] ] = register

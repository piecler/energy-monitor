<?php

$zipfile = 'MOSMIX_S_LATEST_240.kmz';
$url = 'https://opendata.dwd.de/weather/local_forecasts/mos/MOSMIX_S/all_stations/kml/' . $zipfile;
$ts = [];
$rows = [];
$sqlFields = [
	'PPPP', 'TX', 'TTT', 'Td', 'TN', 'T5cm', 'DD', 'FF', 'FX1', 'FX3', 'FXh', 'FXh25', 'FXh40', 'FXh55',
	'N', 'Neff', 'Nh', 'Nm', 'Nl', 'N05', 'VV', 'wwM', 'wwM6', 'wwMh', 'ww', 'W1W2', 'RR1c', 'RRS1c',
	'RR3c', 'RRS3c', 'R602', 'R650', 'Rh00', 'Rh02', 'Rh10', 'Rh50', 'Rd02', 'Rd50', 'Rad1h', 'SunD1' ];

function debug( $str ) {
	#echo "$str\n";
}

$cred = explode( "\n", file_get_contents( realpath(dirname(__FILE__)) . '/../db.cred' ) );
$mysqli = new mysqli( $cred[0], $cred[1], $cred[2], $cred[3] );
if ($mysqli->connect_errno) {
    die( "Failed to connect to MySQL: " . $mysqli->connect_error );
}

$sqlInsert = 'INSERT INTO
	`log`.`weather`
	( `timestamp`, `datetime`, `location`, `' . implode( '`, `', $sqlFields ). '` ) VALUES
	( ?, FROM_UNIXTIME(?), ?, ' . implode(',',array_fill( 0, count($sqlFields), '? ') ) . ')
	ON DUPLICATE KEY UPDATE `' . implode( '` = ?, `', $sqlFields ). '` = ?;';
$insertStmt = $mysqli->prepare( $sqlInsert );

debug( 'fetch zip' );
$zip = file_get_contents( $url );
if ( $zip !== false ) {
	debug( 'store zip' );
	file_put_contents( $zipfile, $zip );
	$zip = new ZipArchive;
	debug( 'open zip' );
	$res = $zip->open( $zipfile );
	if ( $res === true ) {
		debug( 'extract kml' );
		$xml = $zip->getFromName( $zip->getNameIndex(0) );
		debug( 'parse kml' );
		$mosmix = new SimpleXMLElement($xml);
		debug( 'get data' );
		$timesteps = $mosmix->children('kml', true)->Document->ExtendedData->children('dwd',true)->ProductDefinition->ForecastTimeSteps->TimeStep;
		for ( $i = 0, $len = count( $timesteps ); $i < $len; $i++ ) {
			#debug( trim($timesteps[$i]) . ' : ' . strtotime( trim($timesteps[$i]) ) );
			$_ts = strtotime( trim($timesteps[$i]) );
			$ts[] = $_ts;
			$row = [ 'timestamp' => $_ts ];
			for ( $j = 0; $j < count( $sqlFields ); $j++ ) {
				$row[$sqlFields[$j]] = NULL;
			}
			$rows[] = $row;
		}
		$placemarks = $mosmix->children('kml', true)->Document->Placemark;
		$mysqli->begin_transaction();
		for ( $pi = 0, $len = count( $placemarks ); $pi < $len; $pi++ ) {
			$p = $placemarks[$pi];
			$location = trim( $p->name );
			$sqlData = [];
			$forecasts = $p->ExtendedData->children('dwd',true)->Forecast;
			for ( $fi = 0, $flen = count( $forecasts ); $fi < $flen; $fi++ ) {
				$f = $forecasts[$fi];
				$field = trim( $f['elementName'] );
				$values = preg_split( '/\s+/', trim($f->value) );
				for ( $vi = 0, $vlen = count( $values ); $vi < $vlen; $vi++ ) {
					if ( array_key_exists( $field, $rows[$vi] ) ) {
						if ( $values[$vi] !== '-' ) {
							$rows[$vi][$field] = (float)$values[$vi];
						}
					}
				}
			}
			// store in db
			for ( $ri = 0, $rlen = count( $rows ); $ri < $rlen; $ri++ ) {
				$r = $rows[$ri];
				$sqlValues = [ $r['timestamp'] * 1000, $r['timestamp'], $location ];
				// values ...
				for ( $j = 0; $j < count( $sqlFields ); $j++ ) {
					$sqlValues[] = $r[$sqlFields[$j]];
				}
				// on duplicate key ...
				for ( $j = 0; $j < count( $sqlFields ); $j++ ) {
					$sqlValues[] = $r[$sqlFields[$j]];
				}
				#var_dump( $sqlValues );die;
				$insertStmt->bind_param( str_pad( 'iis', 2*count( $sqlFields )+3, 's' ), ...$sqlValues );
				$insertStmt->execute();
			}
			
			if ( $pi % 100 === 99 ) {
				debug ( 'store location forecasts ' . $pi );
				$mysqli->commit();
				$mysqli->begin_transaction();
			}
	

		}
		$mysqli->commit();
		//unlink( $file );
	} else {
		// zip broken
		die;
	}
} else {
	// url broken
	die;
}


<?php
require( 'config.php' );

$values = [];
$storePerInsert = 3000;

function getSunPosition($date, $lat, $lng) {
	//const {sin, cos, asin, atan2, PI} = Math, 
	$r = pi() / 180;
	$t = $date / 315576e7 - 0.3;
	$m = $r * (357.52911 + $t * (35999.05029 - $t * 1537e-7));
	$c = $r * (125.04 - 1934.136 * $t);
	$l = $r * (280.46646 + $t * (36000.76983 + $t * 3032e-7) + (1.914602 - $t * (4817e-6 - $t * 14e-6)) * sin($m) - 
		569e-5 - 478e-5 * sin($c)) + (0.019993 - 101e-6 * $t) * sin(2 * $m) + 289e-6 * sin(3 * $m);
	$e = $r * (84381.448 - $t * (46.815 - $t * (59e-5 + 1813e-6 * $t))) / 3600 + $r * 256e-5 * cos($c);
	$sl = sin($l);
	$cr = cos($r * $lat);
	$sr = sin($r * $lat);
	$d = asin(sin($e) * $sl);
	$h = $r * (280.46061837 + 13184999.8983375 * $t + $lng) - atan2(cos($e) * $sl, cos($l));
	$sd = sin($d);
	$cd = cos($d);
	$ch = cos($h);
	return [
		'azimuth' => pi() + atan2(sin($h), $ch * $sr - $cr * $sd / $cd), 
		'altitude' => asin($sr * $sd + $cr * $cd * $ch)
	];
}

function toDeg( $rad ) {
	return 180 * ( $rad / pi() );
}


/*
$time = 1685809960-18*3600-31*60-40;
for ( $i= 0; $i < 24*60; $i++ ) {
	$ts = $time + $i * 60;
	$datetimeFormat = 'Y-m-d H:i:s';
	$date = new \DateTime('now', new \DateTimeZone('Europe/Berlin'));
	$date->setTimestamp($ts);
	$sun = getSunPosition( $ts * 1000, 52, 13 );
	echo $date->format($datetimeFormat) . " $ts " . toDeg( $sun['azimuth'] ) . '° / ' . toDeg($sun['altitude']) . "\n";
}
*/


$cred = explode( "\n", file_get_contents( realpath(dirname(__FILE__)) . '/db.cred' ) );
$mysqli = new mysqli( $cred[0], $cred[1], $cred[2], $cred[3] );
if ($mysqli->connect_errno) {
    echo "Failed to connect to MySQL: " . $mysqli->connect_error;
} else {
	$ph = [];
	for ( $i = 0; $i < $storePerInsert; $i++ ) {
		$ph[] = '?';
	}
	$sql = "INSERT INTO `sun` (`unix_ts`, `azimuth`, `elevation`) VALUES ( ?, ?, ? );";
	$stmt = $mysqli->prepare( $sql );
	$ts = 946681200000;
	$stopTs = 4102441200000;
	$n = 0;
	$mysqli->begin_transaction();
	while ( $ts < $stopTs ) {
		$sun = getSunPosition( $ts, $lat, $lng );
		$az = toDeg( $sun['azimuth'] );
		$el = toDeg( $sun['altitude'] );
		$values[] = $ts;
		$values[] = $az;
		$values[] = $el;
		$n++;
		$stmt->bind_param( "iss", $ts, $az, $el );
		$stmt->execute();
		if ( $n > 100000 ) {
			echo 'store';
			$mysqli->commit();
			$mysqli->begin_transaction();
			$n = 0;
		}
		$ts += 200000;
		$date = date( 'Y-m-d', (int)($ts / 1000) );
		$n++;
		echo "\r$date               ";
	}
	$mysqli->commit();

}

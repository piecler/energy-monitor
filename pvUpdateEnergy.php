<?php

$cred = explode( "\n", file_get_contents( realpath(dirname(__FILE__)) . '/db.cred' ) );

$mysqli = new mysqli( $cred[0], $cred[1], $cred[2], $cred[3] );
if ($mysqli->connect_errno) {
    echo "Failed to connect to MySQL: " . $mysqli->connect_error;
} else {
	$sql = 
	"INSERT INTO `pv_E` ( `id`, `date`, `pv`, `grid_out`, `grid_in`, `battery_charge`, `battery_discharge`, `load`, `gen`, `em_export`, `em_import`)
		SELECT * FROM (SELECT
			NULL AS `id`,
			DATE(`timestamp`) AS `date`,
			(MAX(`pv_total_E`)-MIN(`pv_total_E`)) AS `pv`,
			(MAX(`grid_out_total_E`)-MIN(`grid_out_total_E`)) AS `grid_out`,
			(MAX(`grid_in_total_E`)-MIN(`grid_in_total_E`)) AS `grid_in`,
			(MAX(`battery_charge_total_E`)-MIN(`battery_charge_total_E`)) AS `battery_charge`,
			(MAX(`battery_discharge_total_E`)-MIN(`battery_discharge_total_E`)) AS `battery_discharge`,
			(MAX(`load_total_E`)-MIN(`load_total_E`)) AS `load`,
			(MAX(`gen_total_E`)-MIN(`gen_total_E`)) AS `gen`,
			(MAX(`em_export_E`)-MIN(`em_export_E`)) AS `em_export`,
			(MAX(`em_import_E`)-MIN(`em_import_E`)) AS `em_import`
		FROM
			`log`.`pv`
		WHERE
			DATE(`timestamp`) >= subdate(CURDATE(),1)
		GROUP BY
			DATE(`timestamp`)) AS `t`
	ON DUPLICATE KEY UPDATE `pv` = `t`.`pv`,`grid_out` = `t`.`grid_out`,`grid_in` = `t`.`grid_in`,`battery_charge` = `t`.`battery_charge`,`battery_discharge` = `t`.`battery_discharge`,`load` = `t`.`load`,`gen` = `t`.`gen`,`em_export` = `t`.`em_export`,`em_import` = `t`.`em_import`";
	$res = $mysqli->query( $sql );
	/*
	$sql = 
	"INSERT INTO `pv_E` ( `id`, `date`, `em_p1_import`, `em_p2_import`, `em_p3_import`, `em_p1_export`, `em_p2_export`, `em_p3_export` )
		SELECT * FROM (SELECT
			NULL AS `id`,
			DATE(`timestamp`) AS `date`,
			(MAX(`em_p1_import_E`)-MIN(`em_p1_import_E`)) AS `em_p1_import`,
			(MAX(`em_p2_import_E`)-MIN(`em_p2_import_E`)) AS `em_p2_import`,
			(MAX(`em_p3_import_E`)-MIN(`em_p3_import_E`)) AS `em_p3_import`,
			(MAX(`em_p1_export_E`)-MIN(`em_p1_export_E`)) AS `em_p1_export`,
			(MAX(`em_p2_export_E`)-MIN(`em_p2_export_E`)) AS `em_p2_export`,
			(MAX(`em_p3_export_E`)-MIN(`em_p3_export_E`)) AS `em_p3_export`
		FROM
			`log`.`em`
		WHERE
			DATE(`timestamp`) >= subdate(CURDATE(),1)
		GROUP BY
			DATE(`timestamp`)) AS `t`
	ON DUPLICATE KEY UPDATE `em_p1_import` = `t`.`em_p1_import`,`em_p2_import` = `t`.`em_p2_import`,`em_p3_import` = `t`.`em_p3_import`,`em_p1_export` = `t`.`em_p1_export`,`em_p2_export` = `t`.`em_p2_export`,`em_p3_export` = `t`.`em_p3_export`";
	$res = $mysqli->query( $sql );
	*/
}

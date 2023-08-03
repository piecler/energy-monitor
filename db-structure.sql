-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jul 27, 2023 at 09:05 PM
-- Server version: 8.0.33-0ubuntu0.22.04.2
-- PHP Version: 8.1.2-1ubuntu2.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Database: `log`
--

-- --------------------------------------------------------

--
-- Table structure for table `em`
--

CREATE TABLE `em` (
  `row` int NOT NULL,
  `timestamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `unix_ts` bigint NOT NULL,
  `em_p1_V` float DEFAULT NULL,
  `em_p2_V` float DEFAULT NULL,
  `em_p3_V` float DEFAULT NULL,
  `em_p1_C` float DEFAULT NULL,
  `em_p2_C` float DEFAULT NULL,
  `em_p3_C` float DEFAULT NULL,
  `em_p1_P` float DEFAULT NULL,
  `em_p2_P` float DEFAULT NULL,
  `em_p3_P` float DEFAULT NULL,
  `em_p1_AP` float DEFAULT NULL,
  `em_p2_AP` float DEFAULT NULL,
  `em_p3_AP` float DEFAULT NULL,
  `em_p1_RP` float DEFAULT NULL,
  `em_p2_RP` float DEFAULT NULL,
  `em_p3_RP` float DEFAULT NULL,
  `em_p1_PF` float DEFAULT NULL,
  `em_p2_PF` float DEFAULT NULL,
  `em_p3_PF` float DEFAULT NULL,
  `em_p1_PA` float DEFAULT NULL,
  `em_p2_PA` float DEFAULT NULL,
  `em_p3_PA` float DEFAULT NULL,
  `em_frq` float DEFAULT NULL,
  `em_p1_p2_V` float DEFAULT NULL,
  `em_p2_p3_V` float DEFAULT NULL,
  `em_p3_p1_V` float DEFAULT NULL,
  `em_n_C` float DEFAULT NULL,
  `em_p1_import_E` float DEFAULT NULL,
  `em_p2_import_E` float DEFAULT NULL,
  `em_p3_import_E` float DEFAULT NULL,
  `em_p1_export_E` float DEFAULT NULL,
  `em_p2_export_E` float DEFAULT NULL,
  `em_p3_export_E` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `em_wago`
--

CREATE TABLE `em_wago` (
  `row` int NOT NULL,
  `timestamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `unix_ts` bigint NOT NULL,
  `frq` float DEFAULT NULL,
  `L1_V` float DEFAULT NULL,
  `L2_V` float DEFAULT NULL,
  `L3_V` float DEFAULT NULL,
  `L1_C` float DEFAULT NULL,
  `L2_C` float DEFAULT NULL,
  `L3_C` float DEFAULT NULL,
  `P` float DEFAULT NULL,
  `L1_P` float DEFAULT NULL,
  `L2_P` float DEFAULT NULL,
  `L3_P` float DEFAULT NULL,
  `RP` float DEFAULT NULL,
  `L1_RP` float DEFAULT NULL,
  `L2_RP` float DEFAULT NULL,
  `L3_RP` float DEFAULT NULL,
  `AP` float DEFAULT NULL,
  `L1_AP` float DEFAULT NULL,
  `L2_AP` float DEFAULT NULL,
  `L3_AP` float DEFAULT NULL,
  `PF` float DEFAULT NULL,
  `L1_PF` float DEFAULT NULL,
  `L2_PF` float DEFAULT NULL,
  `L3_PF` float DEFAULT NULL,
  `L1_L2_V` float DEFAULT NULL,
  `L1_L3_V` float DEFAULT NULL,
  `L2_L3_V` float DEFAULT NULL,
  `E` float DEFAULT NULL,
  `L1_E` float DEFAULT NULL,
  `L2_E` float DEFAULT NULL,
  `L3_E` float DEFAULT NULL,
  `import_E` float DEFAULT NULL,
  `import_L1_E` float DEFAULT NULL,
  `import_L2_E` float DEFAULT NULL,
  `import_L3_E` float DEFAULT NULL,
  `export_E` float DEFAULT NULL,
  `export_L1_E` float DEFAULT NULL,
  `export_L2_E` float DEFAULT NULL,
  `export_L3_E` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `pv`
--

CREATE TABLE `pv` (
  `row` int UNSIGNED NOT NULL,
  `timestamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `unix_ts` bigint NOT NULL,
  `status` tinyint UNSIGNED DEFAULT NULL,
  `carport_P` smallint DEFAULT NULL,
  `carport_V` smallint DEFAULT NULL,
  `carport_I` smallint DEFAULT NULL,
  `roof_P` smallint DEFAULT NULL,
  `roof_V` smallint DEFAULT NULL,
  `roof_I` smallint DEFAULT NULL,
  `gen_p1_P` smallint DEFAULT NULL,
  `gen_p2_P` smallint DEFAULT NULL,
  `gen_p3_P` smallint DEFAULT NULL,
  `gen_P` smallint DEFAULT NULL,
  `DC_transformer_T` smallint DEFAULT NULL,
  `heatsink_T` smallint DEFAULT NULL,
  `battery_T` smallint DEFAULT NULL,
  `battery_V` smallint DEFAULT NULL,
  `battery_SOC` smallint DEFAULT NULL,
  `battery_P` smallint DEFAULT NULL,
  `battery_I` smallint DEFAULT NULL,
  `grid_P` smallint DEFAULT NULL,
  `load_total_P` smallint DEFAULT NULL,
  `backup_P` smallint DEFAULT NULL,
  `inverter_p1_V` smallint UNSIGNED DEFAULT NULL,
  `inverter_p2_V` smallint UNSIGNED DEFAULT NULL,
  `inverter_p3_V` smallint UNSIGNED DEFAULT NULL,
  `inverter_p1_P` smallint DEFAULT NULL,
  `inverter_p2_P` smallint DEFAULT NULL,
  `inverter_p3_P` smallint DEFAULT NULL,
  `inverter_P` smallint DEFAULT NULL,
  `inverter_frq` smallint UNSIGNED DEFAULT NULL,
  `load_frq` smallint UNSIGNED DEFAULT NULL,
  `grid_frq` smallint DEFAULT NULL,
  `battery_charge_today_E` smallint UNSIGNED DEFAULT NULL,
  `battery_discharge_today_E` smallint UNSIGNED DEFAULT NULL,
  `battery_charge_total_E` int UNSIGNED DEFAULT NULL,
  `battery_discharge_total_E` int UNSIGNED DEFAULT NULL,
  `grid_in_today_E` smallint UNSIGNED DEFAULT NULL,
  `grid_out_today_E` smallint UNSIGNED DEFAULT NULL,
  `grid_in_total_E` int UNSIGNED DEFAULT NULL,
  `grid_out_total_E` int UNSIGNED DEFAULT NULL,
  `load_today_E` smallint UNSIGNED DEFAULT NULL,
  `load_total_E` int UNSIGNED DEFAULT NULL,
  `pv_today_E` smallint UNSIGNED DEFAULT NULL,
  `pv_total_E` int UNSIGNED DEFAULT NULL,
  `gen_today_E` smallint UNSIGNED DEFAULT NULL,
  `gen_total_E` int UNSIGNED DEFAULT NULL,
  `em_frq` float DEFAULT NULL,
  `em_grid_P` float DEFAULT NULL,
  `em_import_E` float DEFAULT NULL,
  `em_export_E` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `pv_E`
--

CREATE TABLE `pv_E` (
  `id` int UNSIGNED NOT NULL,
  `date` date NOT NULL,
  `pv` int UNSIGNED DEFAULT NULL,
  `grid_out` int UNSIGNED DEFAULT NULL,
  `grid_in` int UNSIGNED DEFAULT NULL,
  `battery_charge` int UNSIGNED DEFAULT NULL,
  `battery_discharge` int UNSIGNED DEFAULT NULL,
  `load` int UNSIGNED DEFAULT NULL,
  `gen` int UNSIGNED DEFAULT NULL,
  `em_import` float DEFAULT NULL,
  `em_export` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `pv_values`
--

CREATE TABLE `pv_values` (
  `inverter_timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `styleboiler`
--

CREATE TABLE `styleboiler` (
  `row` int NOT NULL,
  `timestamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `unix_ts` bigint NOT NULL,
  `power` smallint DEFAULT NULL,
  `mode` smallint DEFAULT NULL,
  `mode_op` smallint DEFAULT NULL,
  `flags` smallint DEFAULT NULL,
  `status1` smallint DEFAULT NULL,
  `status2` smallint DEFAULT NULL,
  `error` smallint DEFAULT NULL,
  `Tx` float DEFAULT NULL,
  `Ts` float DEFAULT NULL,
  `T5U` float DEFAULT NULL,
  `T5L` float DEFAULT NULL,
  `T3` float DEFAULT NULL,
  `T4` float DEFAULT NULL,
  `Tp` float DEFAULT NULL,
  `Th` float DEFAULT NULL,
  `pmv` smallint DEFAULT NULL,
  `current` smallint DEFAULT NULL,
  `Ts_min` smallint DEFAULT NULL,
  `Ts_max` smallint DEFAULT NULL,
  `rhw` smallint DEFAULT NULL,
  `compressor_runtime` smallint DEFAULT NULL,
  `hour` smallint DEFAULT NULL,
  `minute` smallint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `sun`
--

CREATE TABLE `sun` (
  `unix_ts` bigint NOT NULL,
  `azimuth` float NOT NULL,
  `elevation` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `weather`
--

CREATE TABLE `weather` (
  `timestamp` bigint NOT NULL,
  `datetime` timestamp NOT NULL,
  `location` varchar(5) NOT NULL,
  `PPPP` float DEFAULT NULL,
  `TX` float DEFAULT NULL,
  `TTT` float DEFAULT NULL,
  `Td` float DEFAULT NULL,
  `TN` float DEFAULT NULL,
  `T5cm` float DEFAULT NULL,
  `DD` float DEFAULT NULL,
  `FF` float DEFAULT NULL,
  `FX1` float DEFAULT NULL,
  `FX3` float DEFAULT NULL,
  `FXh` float DEFAULT NULL,
  `FXh25` float DEFAULT NULL,
  `FXh40` float DEFAULT NULL,
  `FXh55` float DEFAULT NULL,
  `N` float DEFAULT NULL,
  `Neff` float DEFAULT NULL,
  `Nh` float DEFAULT NULL,
  `Nm` float DEFAULT NULL,
  `Nl` float DEFAULT NULL,
  `N05` float DEFAULT NULL,
  `VV` float DEFAULT NULL,
  `wwM` float DEFAULT NULL,
  `wwM6` float DEFAULT NULL,
  `wwMh` float DEFAULT NULL,
  `ww` float DEFAULT NULL,
  `W1W2` float DEFAULT NULL,
  `RR1c` float DEFAULT NULL,
  `RRS1c` float DEFAULT NULL,
  `RR3c` float DEFAULT NULL,
  `RRS3c` float DEFAULT NULL,
  `R602` float DEFAULT NULL,
  `R650` float DEFAULT NULL,
  `Rh00` float DEFAULT NULL,
  `Rh02` float DEFAULT NULL,
  `Rh10` float DEFAULT NULL,
  `Rh50` float DEFAULT NULL,
  `Rd02` float DEFAULT NULL,
  `Rd50` float DEFAULT NULL,
  `Rad1h` float DEFAULT NULL,
  `SunD1` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `em`
--
ALTER TABLE `em`
  ADD PRIMARY KEY (`row`),
  ADD KEY `timestamp` (`timestamp`),
  ADD KEY `unix_ts` (`unix_ts`);

--
-- Indexes for table `em_wago`
--
ALTER TABLE `em_wago`
  ADD PRIMARY KEY (`row`),
  ADD KEY `timestamp` (`timestamp`),
  ADD KEY `unix_ts` (`unix_ts`);

--
-- Indexes for table `pv`
--
ALTER TABLE `pv`
  ADD PRIMARY KEY (`row`),
  ADD KEY `timestamp` (`timestamp`),
  ADD KEY `unix_ts` (`unix_ts`);

--
-- Indexes for table `pv_E`
--
ALTER TABLE `pv_E`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `date` (`date`);

--
-- Indexes for table `styleboiler`
--
ALTER TABLE `styleboiler`
  ADD PRIMARY KEY (`row`),
  ADD KEY `timestamp` (`timestamp`),
  ADD KEY `unix_ts` (`unix_ts`);

--
-- Indexes for table `sun`
--
ALTER TABLE `sun`
  ADD UNIQUE KEY `unix_ts` (`unix_ts`);

--
-- Indexes for table `weather`
--
ALTER TABLE `weather`
  ADD PRIMARY KEY (`timestamp`,`location`),
  ADD KEY `location` (`location`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `em`
--
ALTER TABLE `em`
  MODIFY `row` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `em_wago`
--
ALTER TABLE `em_wago`
  MODIFY `row` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `pv`
--
ALTER TABLE `pv`
  MODIFY `row` int UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `pv_E`
--
ALTER TABLE `pv_E`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `styleboiler`
--
ALTER TABLE `styleboiler`
  MODIFY `row` int NOT NULL AUTO_INCREMENT;
COMMIT;

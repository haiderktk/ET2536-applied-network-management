-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Dec 10, 2016 at 01:03 PM
-- Server version: 5.5.53-0ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.20

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `anm`
--

-- --------------------------------------------------------

--
-- Table structure for table `device`
--

CREATE TABLE IF NOT EXISTS `device` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip_port` varchar(255) NOT NULL,
  `community` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=24 ;

--
-- Dumping data for table `device`
--

INSERT INTO `device` (`id`, `ip_port`, `community`) VALUES
(23, '10.1.0.169:162', 'public');

-- --------------------------------------------------------

--
-- Table structure for table `snmptraps`
--

CREATE TABLE IF NOT EXISTS `snmptraps` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device` varchar(255) NOT NULL,
  `status` int(10) NOT NULL,
  `time` varchar(255) NOT NULL,
  `p_status` int(10) DEFAULT NULL,
  `p_time` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=18 ;

--
-- Dumping data for table `snmptraps`
--

INSERT INTO `snmptraps` (`id`, `device`, `status`, `time`, `p_status`, `p_time`) VALUES
(15, 'bubbly.bth.se', 2, '1479973593', 1, '1479973354'),
(16, 'lovely.bth.se', 2, '1479973473', 1, '1479973378'),
(17, 'troubly.bth.se', 3, '1479973615', 2, '1479973605');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

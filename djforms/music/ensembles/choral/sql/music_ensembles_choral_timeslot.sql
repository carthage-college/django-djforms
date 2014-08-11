-- phpMyAdmin SQL Dump
-- version 3.3.2deb1ubuntu1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Aug 01, 2013 at 11:26 AM
-- Server version: 5.1.70
-- PHP Version: 5.3.2-1ubuntu4.20

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `djforms`
--

-- --------------------------------------------------------

--
-- Table structure for table `music_ensembles_choral_timeslot`
--

CREATE TABLE IF NOT EXISTS `music_ensembles_choral_timeslot` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_time` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=93 ;

--
-- Dumping data for table `music_ensembles_choral_timeslot`
--

INSERT INTO `music_ensembles_choral_timeslot` (`date_time`, `active`) VALUES
('Monday, September 2: 2:00pm', 1),
('Monday, September 2: 2:10pm', 1),
('Monday, September 2: 2:20pm', 1),
('Monday, September 2: 2:30pm', 1),
('Monday, September 2: 2:40pm', 1),
('Monday, September 2: 2:50pm', 1),
('Monday, September 2: 3:00pm', 1),
('Monday, September 2: 3:10pm', 1),
('Monday, September 2: 3:20pm', 1),
('Monday, September 2: 3:30pm', 1),
('Monday, September 2: 3:40pm', 1),
('Monday, September 2: 3:50pm', 1),
('Monday, September 2: 4:00pm', 1),
('Monday, September 2: 4:10pm', 1),
('Monday, September 2: 4:20pm', 1),
('Monday, September 2: 4:30pm', 1),
('Monday, September 2: 4:40pm', 1),
('Monday, September 2: 4:50pm', 1),
('Monday, September 2: 5:00pm', 1),
('Monday, September 2: 5:10pm', 1),
('Monday, September 2: 5:20pm', 1),
('Monday, September 2: 5:30pm', 1),
('Monday, September 2: 5:40pm', 1),
('Monday, September 2: 5:50pm', 1),
('Monday, September 2: 6:00pm', 1),
('Monday, September 2: 6:10pm', 1),
('Monday, September 2: 6:20pm', 1),
('Monday, September 2: 6:30pm', 1),
('Monday, September 2: 6:40pm', 1),
('Monday, September 2: 6:50pm', 1),
('Monday, September 2: 7:00pm', 1),
('Monday, September 2: 7:10pm', 1),
('Monday, September 2: 7:20pm', 1),
('Monday, September 2: 7:30pm', 1),
('Monday, September 2: 7:40pm', 1),
('Monday, September 2: 7:50pm', 1),
('Monday, September 2: 8:00pm', 1),
('Tuesday, September 3: 9:00am', 1),
('Tuesday, September 3: 9:10am', 1),
('Tuesday, September 3: 9:20am', 1),
('Tuesday, September 3: 9:30am', 1),
('Tuesday, September 3: 9:40am', 1),
('Tuesday, September 3: 9:50am', 1),
('Tuesday, September 3: 10:00am', 1),
('Tuesday, September 3: 10:10am', 1),
('Tuesday, September 3: 10:20am', 1),
('Tuesday, September 3: 10:30am', 1),
('Tuesday, September 3: 10:40am', 1),
('Tuesday, September 3: 10:50am', 1),
('Tuesday, September 3: 11:00am', 1),
('Tuesday, September 3: 11:10am', 1),
('Tuesday, September 3: 11:20am', 1),
('Tuesday, September 3: 11:30am', 1),
('Tuesday, September 3: 11:40am', 1),
('Tuesday, September 3: 11:50am', 1),
('Tuesday, September 3: 12:00pm', 1),
('Tuesday, September 3: 12:10pm', 1),
('Tuesday, September 3: 12:20pm', 1),
('Tuesday, September 3: 12:30pm', 1),
('Tuesday, September 3: 12:40pm', 1),
('Tuesday, September 3: 12:50pm', 1),
('Tuesday, September 3: 1:00pm', 1),
('Tuesday, September 3: 1:10pm', 1),
('Tuesday, September 3: 1:20pm', 1),
('Tuesday, September 3: 1:30pm', 1),
('Tuesday, September 3: 1:40pm', 1),
('Tuesday, September 3: 1:50pm', 1),
('Tuesday, September 3: 2:00pm', 1),
('Tuesday, September 3: 2:10pm', 1),
('Tuesday, September 3: 2:20pm', 1),
('Tuesday, September 3: 2:30pm', 1),
('Tuesday, September 3: 2:40pm', 1),
('Tuesday, September 3: 2:50pm', 1),
('Tuesday, September 3: 3:00pm', 1),
('Tuesday, September 3: 3:10pm', 1),
('Tuesday, September 3: 3:20pm', 1),
('Tuesday, September 3: 3:30pm', 1),
('Tuesday, September 3: 3:40pm', 1),
('Tuesday, September 3: 3:50pm', 1),
('Tuesday, September 3: 4:00pm', 1),
('Tuesday, September 3: 4:10pm', 1),
('Tuesday, September 3: 4:20pm', 1),
('Tuesday, September 3: 4:30pm', 1),
('Tuesday, September 3: 4:40pm', 1),
('Tuesday, September 3: 4:50pm', 1),
('Tuesday, September 3: 5:00pm', 1),
('Tuesday, September 3: 5:10pm', 1),
('Tuesday, September 3: 5:20pm', 1),
('Tuesday, September 3: 5:30pm', 1),
('Tuesday, September 3: 5:40pm', 1),
('Tuesday, September 3: 5:50pm', 1),
('Tuesday, September 3: 6:00pm', 1),
('Tuesday, September 3: 6:10pm', 1),
('Tuesday, September 3: 6:20pm', 1),
('Tuesday, September 3: 6:30pm', 1),
('Tuesday, September 3: 6:40pm', 1),
('Tuesday, September 3: 6:50pm', 1),
('Tuesday, September 3: 7:00pm', 1),
('Tuesday, September 3: 7:10pm', 1),
('Tuesday, September 3: 7:20pm', 1),
('Tuesday, September 3: 7:30pm', 1),
('Tuesday, September 3: 7:40pm', 1),
('Tuesday, September 3: 7:50pm', 1),
('Tuesday, September 3: 8:00pm', 1);

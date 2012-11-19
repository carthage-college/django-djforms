CREATE TABLE IF NOT EXISTS `alumni_classnotes_contact` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `first_name` varchar(128) NOT NULL,
  `last_name` varchar(128) NOT NULL,
  `second_name` varchar(128) DEFAULT NULL,
  `previous_name` varchar(128) DEFAULT NULL,
  `salutation` varchar(16) DEFAULT NULL,
  `suffix` varchar(16) DEFAULT NULL,
  `email` varchar(75) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `maidenname` varchar(255) DEFAULT NULL,
  `classyear` varchar(10) NOT NULL,
  `spousename` varchar(50) DEFAULT NULL,
  `spousemaidenname` varchar(50) DEFAULT NULL,
  `spouseyear` varchar(10) DEFAULT NULL,
  `classnote` longtext,
  `pubtext` longtext,
  `alumnistatus` int(11) NOT NULL DEFAULT '0',
  `alumnicomments` longtext,
  `pubstatus` int(11) NOT NULL DEFAULT '0',
  `pubstatusdate` datetime DEFAULT NULL,
  `carthaginianstatus` int(11) NOT NULL DEFAULT '0',
  `notesubmitteddate` datetime DEFAULT NULL,
  `picture` varchar(255) DEFAULT NULL,
  `caption` varchar(255) DEFAULT NULL,
  `webpicname` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2780

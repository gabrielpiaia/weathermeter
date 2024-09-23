CREATE DATABASE weathermeter

CREATE TABLE `temperatura` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cidade` varchar(50) DEFAULT NULL,
  `temperature` float DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT
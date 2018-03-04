-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: localhost    Database: ichp
-- ------------------------------------------------------
-- Server version	5.7.17-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `activity`
--

DROP TABLE IF EXISTS `activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;

CREATE TABLE `activity` (
  `act_id` int(11) NOT NULL AUTO_INCREMENT,
  `publisher` int(11) DEFAULT NULL,
  `issue_date` date DEFAULT NULL,
  `title` char(20) DEFAULT NULL,
  `content` text NOT NULL,
  `hold_date` date DEFAULT NULL,
  `hold_addr` char(100) DEFAULT NULL,
  `act_src` text,
  PRIMARY KEY (`act_id`),
  KEY `publisher` (`publisher`),
  CONSTRAINT `activity_ibfk_1` FOREIGN KEY (`publisher`) REFERENCES `user` (`user_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activity`
--

LOCK TABLES `activity` WRITE;
/*!40000 ALTER TABLE `activity` DISABLE KEYS */;
/*!40000 ALTER TABLE `activity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attention_info`
--

DROP TABLE IF EXISTS `attention_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `attention_info` (
  `att_id` int(11) NOT NULL AUTO_INCREMENT,
  `pay_id` int(11) DEFAULT NULL,
  `be_paid_id` int(11) DEFAULT NULL,
  `pay_date` date DEFAULT NULL,
  PRIMARY KEY (`att_id`),
  KEY `be_paid_id` (`be_paid_id`),
  KEY `pay_id` (`pay_id`),
  CONSTRAINT `attention_info_ibfk_1` FOREIGN KEY (`be_paid_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `attention_info_ibfk_2` FOREIGN KEY (`pay_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attention_info`
--

LOCK TABLES `attention_info` WRITE;
/*!40000 ALTER TABLE `attention_info` DISABLE KEYS */;
/*!40000 ALTER TABLE `attention_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `coll_activity`
--

DROP TABLE IF EXISTS `coll_activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `coll_activity` (
  `act_id` int(11) NOT NULL,
  `collector` int(11) NOT NULL,
  `coll_date` date DEFAULT NULL,
  PRIMARY KEY (`act_id`,`collector`),
  KEY `collector` (`collector`),
  CONSTRAINT `coll_activity_ibfk_1` FOREIGN KEY (`act_id`) REFERENCES `activity` (`act_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `coll_activity_ibfk_2` FOREIGN KEY (`collector`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coll_activity`
--

LOCK TABLES `coll_activity` WRITE;
/*!40000 ALTER TABLE `coll_activity` DISABLE KEYS */;
/*!40000 ALTER TABLE `coll_activity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `coll_entry`
--

DROP TABLE IF EXISTS `coll_entry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `coll_entry` (
  `entry_id` int(11) NOT NULL,
  `collector` int(11) NOT NULL,
  `coll_date` date DEFAULT NULL,
  PRIMARY KEY (`entry_id`,`collector`),
  KEY `collector` (`collector`),
  CONSTRAINT `coll_entry_ibfk_1` FOREIGN KEY (`entry_id`) REFERENCES `entry` (`entry_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `coll_entry_ibfk_2` FOREIGN KEY (`collector`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coll_entry`
--

LOCK TABLES `coll_entry` WRITE;
/*!40000 ALTER TABLE `coll_entry` DISABLE KEYS */;
/*!40000 ALTER TABLE `coll_entry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `coll_record`
--

DROP TABLE IF EXISTS `coll_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `coll_record` (
  `rec_id` int(11) NOT NULL,
  `collector` int(11) NOT NULL,
  `coll_date` date DEFAULT NULL,
  PRIMARY KEY (`rec_id`,`collector`),
  KEY `collector` (`collector`),
  CONSTRAINT `coll_record_ibfk_1` FOREIGN KEY (`rec_id`) REFERENCES `record` (`rec_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `coll_record_ibfk_2` FOREIGN KEY (`collector`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coll_record`
--

LOCK TABLES `coll_record` WRITE;
/*!40000 ALTER TABLE `coll_record` DISABLE KEYS */;
/*!40000 ALTER TABLE `coll_record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comm_comm`
--

DROP TABLE IF EXISTS `comm_comm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comm_comm` (
  `comm_comm_id` int(11) NOT NULL AUTO_INCREMENT,
  `comm_rec_id` int(11) DEFAULT NULL,
  `commer` int(11) DEFAULT NULL,
  `content` text NOT NULL,
  `comm_date` date DEFAULT NULL,
  `appr_num` int(11) DEFAULT NULL,
  PRIMARY KEY (`comm_comm_id`),
  KEY `commer` (`commer`),
  KEY `comm_rec_id` (`comm_rec_id`),
  CONSTRAINT `comm_comm_ibfk_1` FOREIGN KEY (`commer`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `comm_comm_ibfk_2` FOREIGN KEY (`comm_rec_id`) REFERENCES `comm_rec` (`comm_rec_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comm_comm`
--

LOCK TABLES `comm_comm` WRITE;
/*!40000 ALTER TABLE `comm_comm` DISABLE KEYS */;
/*!40000 ALTER TABLE `comm_comm` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comm_rec`
--

DROP TABLE IF EXISTS `comm_rec`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comm_rec` (
  `comm_rec_id` int(11) NOT NULL AUTO_INCREMENT,
  `rec_id` int(11) DEFAULT NULL,
  `commer` int(11) DEFAULT NULL,
  `content` text NOT NULL,
  `comm_date` date DEFAULT NULL,
  `appr_num` int(11) DEFAULT NULL,
  PRIMARY KEY (`comm_rec_id`),
  KEY `commer` (`commer`),
  KEY `rec_id` (`rec_id`),
  CONSTRAINT `comm_rec_ibfk_1` FOREIGN KEY (`commer`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `comm_rec_ibfk_2` FOREIGN KEY (`rec_id`) REFERENCES `record` (`rec_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comm_rec`
--

LOCK TABLES `comm_rec` WRITE;
/*!40000 ALTER TABLE `comm_rec` DISABLE KEYS */;
/*!40000 ALTER TABLE `comm_rec` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entry`
--

DROP TABLE IF EXISTS `entry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entry` (
  `entry_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(50) NOT NULL,
  `content` text NOT NULL,
  `editor` int(11) DEFAULT NULL,
  PRIMARY KEY (`entry_id`),
  KEY `editor` (`editor`),
  CONSTRAINT `entry_ibfk_1` FOREIGN KEY (`editor`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entry`
--

LOCK TABLES `entry` WRITE;
/*!40000 ALTER TABLE `entry` DISABLE KEYS */;
/*!40000 ALTER TABLE `entry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mail`
--

DROP TABLE IF EXISTS `mail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mail` (
  `mail_id` int(11) NOT NULL AUTO_INCREMENT,
  `sender` int(11) DEFAULT NULL,
  `recipient` int(11) DEFAULT NULL,
  `content` text NOT NULL,
  `send_date` date DEFAULT NULL,
  PRIMARY KEY (`mail_id`),
  KEY `sender` (`sender`),
  KEY `recipient` (`recipient`),
  CONSTRAINT `mail_ibfk_1` FOREIGN KEY (`sender`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `mail_ibfk_2` FOREIGN KEY (`recipient`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mail`
--

LOCK TABLES `mail` WRITE;
/*!40000 ALTER TABLE `mail` DISABLE KEYS */;
/*!40000 ALTER TABLE `mail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `record`
--

DROP TABLE IF EXISTS `record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `record` (
  `rec_id` int(11) NOT NULL AUTO_INCREMENT,
  `recorder` int(11) DEFAULT NULL,
  `title` char(20) DEFAULT NULL,
  `content` text NOT NULL,
  `issue_date` date DEFAULT NULL,
  `type` char(4) DEFAULT NULL,
  `addr` char(100) DEFAULT NULL,
  `appr_num` int(11) DEFAULT NULL,
  `comm_num` int(11) DEFAULT NULL,
  PRIMARY KEY (`rec_id`),
  KEY `recorder` (`recorder`),
  CONSTRAINT `record_ibfk_1` FOREIGN KEY (`recorder`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `record`
--

LOCK TABLES `record` WRITE;
/*!40000 ALTER TABLE `record` DISABLE KEYS */;
/*!40000 ALTER TABLE `record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `role` smallint(6) DEFAULT NULL,
  `telephone` char(11) DEFAULT NULL,
  `psw` char(40) NOT NULL,
  `image_src` text,
  `name` char(20) DEFAULT NULL,
  `sign` char(50) DEFAULT NULL,
  `acc_point` smallint(6) DEFAULT NULL,
  `account_name` char(20) DEFAULT NULL,
  `reg_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1119 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1000,0,'13327278686','111',NULL,'y','hello',1,NULL,'2018-03-04 09:59:10'),(1111,0,'13327278686','111',NULL,'y','hello',1,'yj','2018-03-04 09:59:10'),(1114,NULL,NULL,'111',NULL,NULL,NULL,NULL,'yml','2018-03-04 09:59:10'),(1115,1,'1234567890','111',NULL,'yjj',NULL,NULL,'yy','2018-03-04 09:59:10'),(1116,NULL,NULL,'111',NULL,NULL,NULL,NULL,'yjhh','2018-03-04 09:59:10'),(1117,2,'123','111',NULL,'yj','hello ,i am yj',NULL,'hhappy','2018-03-04 10:30:35'),(1118,1,NULL,'111',NULL,NULL,NULL,NULL,'hhh','2018-03-04 11:10:26');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-03-04 11:44:27

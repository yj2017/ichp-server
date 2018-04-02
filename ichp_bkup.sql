# Host: localhost  (Version 5.7.17-log)
# Date: 2018-04-02 13:42:37
# Generator: MySQL-Front 5.4  (Build 3.52)
# Internet: http://www.mysqlfront.de/

/*!40101 SET NAMES utf8 */;

#
# Structure for table "user"
#

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `role` smallint(6) DEFAULT NULL,
  `telephone` char(11) DEFAULT NULL,
  `psw` char(40) NOT NULL,
  `image_src` text,
  `name` char(20) DEFAULT NULL,
  `sign` char(50) DEFAULT NULL,
  `acc_point` smallint(6) DEFAULT '0',
  `account_name` char(20) DEFAULT NULL,
  `reg_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1119 DEFAULT CHARSET=utf8;

#
# Data for table "user"
#

INSERT INTO `user` VALUES (1000,0,'13327278686','111',NULL,'y','hello',1,NULL,'2018-03-04 09:59:10'),(1111,1,'13327278686','111',NULL,'y','hello',941,'yj','2018-03-04 09:59:10'),(1114,1,NULL,'111',NULL,NULL,NULL,NULL,'yml','2018-03-04 09:59:10'),(1115,1,'1234567890','111',NULL,'yjj',NULL,NULL,'yy','2018-03-04 09:59:10'),(1116,1,NULL,'111',NULL,NULL,NULL,NULL,'yjhh','2018-03-04 09:59:10'),(1117,1,'123','111',NULL,'yj','hello ,i am yj',NULL,'hhappy','2018-03-04 10:30:35'),(1118,1,NULL,'111',NULL,NULL,NULL,NULL,'hhh','2018-03-04 11:10:26');

#
# Structure for table "record"
#

DROP TABLE IF EXISTS `record`;
CREATE TABLE `record` (
  `rec_id` int(11) NOT NULL AUTO_INCREMENT,
  `recorder` int(11) DEFAULT NULL,
  `title` char(20) DEFAULT NULL,
  `url` text,
  `type` int(4) DEFAULT NULL,
  `addr` char(100) DEFAULT NULL,
  `appr_num` int(11) DEFAULT NULL,
  `comm_num` int(11) DEFAULT NULL,
  `issue_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `discribe` char(100) DEFAULT NULL,
  `labels_id_str` char(12) DEFAULT NULL,
  PRIMARY KEY (`rec_id`),
  KEY `recorder` (`recorder`),
  CONSTRAINT `record_ibfk_1` FOREIGN KEY (`recorder`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;

#
# Data for table "record"
#

INSERT INTO `record` VALUES (3,1111,'h','',1,'湖北武汉',0,0,'2018-03-04 16:04:29','test','6,7'),(5,1111,'yyyyyyyyyyyyyyyyyyy','yhujk',2,'ffrgbb',0,0,'2018-03-23 22:09:30','sdfvdxgvszg','6,7'),(6,1111,'yyyyyyyyyyyyyyyyyyy','yhujk',3,'ffrgbb',0,0,'2018-03-23 22:14:10','sdfvdxgvszg','6,7'),(8,1111,'111','http://p5o94s90i.bkt.clouddn.com/5c70500a-3498-11e8-b671-d05349e3b743QQ图片20170323151308.jpg,http://p5o94s90i.bkt.clouddn.com/78e25902-3498-11e8-94c4-d05349e3b74320170104064612159_0001.jpg',1,'wuhan',0,0,'2018-03-31 12:08:27','hhhhhh','6,7'),(9,1111,'111','http://p5o94s90i.bkt.clouddn.com/5c70500a-3498-11e8-b671-d05349e3b743QQ图片20170323151308.jpg,http://p5o94s90i.bkt.clouddn.com/78e25902-3498-11e8-94c4-d05349e3b74320170104064612159_0001.jpg',1,'wuhan',0,0,'2018-03-31 12:09:28','hhhhhh','6,7'),(10,1111,'瓷器','http://p5o94s90i.bkt.clouddn.com/5c70500a-3498-11e8-b671-d05349e3b743QQ图片20170323151308.jpg,http://p5o94s90i.bkt.clouddn.com/78e25902-3498-11e8-94c4-d05349e3b74320170104064612159_0001.jpg',1,'wuhan',0,0,'2018-03-31 12:10:41','hhhhhh','6,7'),(11,1118,'剪纸','http://p5o94s90i.bkt.clouddn.com/78e25902-3498-11e8-94c4-d05349e3b74320170104064612159_0001.jpg',1,'湖北武汉',0,0,'2018-03-31 18:05:47','111','6,7'),(12,1118,'太平鼓','http://p5o94s90i.bkt.clouddn.com/78e25902-3498-11e8-94c4-d05349e3b74320170104064612159_0001.jpg',2,'湖北武汉',0,0,'2018-03-31 18:06:24','happy','6,7'),(13,1111,'None','http://p5o94s90i.bkt.clouddn.com/78e25902-3498-11e8-94c4-d05349e3b74320170104064612159_0001.jpg',2,'湖北武汉',0,0,'2018-03-31 18:08:34','happy','6,7'),(14,1111,'dance','http://p5o94s90i.bkt.clouddn.com/78e25902-3498-11e8-94c4-d05349e3b74320170104064612159_0001.jpg',2,'湖北武汉',0,0,'2018-03-31 18:13:54','happy','6,7'),(15,1111,'dance','http://p5o94s90i.bkt.clouddn.com/78e25902-3498-11e8-94c4-d05349e3b74320170104064612159_0001.jpg',2,'湖北武汉',0,0,'2018-03-31 18:13:58','happy','6,7');

#
# Structure for table "mail"
#

DROP TABLE IF EXISTS `mail`;
CREATE TABLE `mail` (
  `mail_id` int(11) NOT NULL AUTO_INCREMENT,
  `sender` int(11) DEFAULT NULL,
  `recipient` int(11) DEFAULT NULL,
  `content` text NOT NULL,
  `send_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`mail_id`),
  KEY `sender` (`sender`),
  KEY `recipient` (`recipient`),
  CONSTRAINT `mail_ibfk_1` FOREIGN KEY (`sender`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `mail_ibfk_2` FOREIGN KEY (`recipient`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

#
# Data for table "mail"
#

INSERT INTO `mail` VALUES (1,1111,1114,'去哪吃饭','2018-03-17 16:25:19');

#
# Structure for table "entry"
#

DROP TABLE IF EXISTS `entry`;
CREATE TABLE `entry` (
  `entry_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(12) NOT NULL DEFAULT '',
  `content` text NOT NULL,
  `editor` int(11) DEFAULT NULL,
  `url` text,
  PRIMARY KEY (`entry_id`),
  KEY `editor` (`editor`),
  CONSTRAINT `entry_ibfk_1` FOREIGN KEY (`editor`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

#
# Data for table "entry"
#

INSERT INTO `entry` VALUES (6,'皮影戏','by yj',1111,NULL),(7,'古法','源于湘西',1111,NULL);

#
# Structure for table "comm_rec"
#

DROP TABLE IF EXISTS `comm_rec`;
CREATE TABLE `comm_rec` (
  `comm_rec_id` int(11) NOT NULL AUTO_INCREMENT,
  `rec_id` int(11) DEFAULT NULL,
  `commer` int(11) DEFAULT NULL,
  `content` text NOT NULL,
  `appr_num` int(11) DEFAULT NULL,
  `comm_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`comm_rec_id`),
  KEY `commer` (`commer`),
  KEY `rec_id` (`rec_id`),
  CONSTRAINT `comm_rec_ibfk_1` FOREIGN KEY (`commer`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `comm_rec_ibfk_2` FOREIGN KEY (`rec_id`) REFERENCES `record` (`rec_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

#
# Data for table "comm_rec"
#

INSERT INTO `comm_rec` VALUES (3,3,1111,'i love ',2,'2018-03-18 21:53:34');

#
# Structure for table "comm_comm"
#

DROP TABLE IF EXISTS `comm_comm`;
CREATE TABLE `comm_comm` (
  `comm_comm_id` int(11) NOT NULL AUTO_INCREMENT,
  `comm_rec_id` int(11) DEFAULT NULL,
  `commer` int(11) DEFAULT NULL,
  `content` text NOT NULL,
  `appr_num` int(11) DEFAULT NULL,
  `comm_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`comm_comm_id`),
  KEY `commer` (`commer`),
  KEY `comm_rec_id` (`comm_rec_id`),
  CONSTRAINT `comm_comm_ibfk_1` FOREIGN KEY (`commer`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `comm_comm_ibfk_2` FOREIGN KEY (`comm_rec_id`) REFERENCES `comm_rec` (`comm_rec_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

#
# Data for table "comm_comm"
#

INSERT INTO `comm_comm` VALUES (1,3,1111,'hhh',0,'2018-03-23 21:36:11'),(3,3,1111,'hhh',0,'2018-03-23 21:38:05'),(4,3,1111,'hhh',0,'2018-03-23 21:39:00'),(5,3,1111,'hhh',0,'2018-03-23 21:39:28');

#
# Structure for table "coll_record"
#

DROP TABLE IF EXISTS `coll_record`;
CREATE TABLE `coll_record` (
  `rec_id` int(11) NOT NULL,
  `collector` int(11) NOT NULL,
  `coll_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`rec_id`,`collector`),
  KEY `collector` (`collector`),
  CONSTRAINT `coll_record_ibfk_1` FOREIGN KEY (`rec_id`) REFERENCES `record` (`rec_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `coll_record_ibfk_2` FOREIGN KEY (`collector`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Data for table "coll_record"
#


#
# Structure for table "coll_entry"
#

DROP TABLE IF EXISTS `coll_entry`;
CREATE TABLE `coll_entry` (
  `entry_id` int(11) NOT NULL,
  `collector` int(11) NOT NULL,
  `coll_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`entry_id`,`collector`),
  KEY `collector` (`collector`),
  CONSTRAINT `coll_entry_ibfk_1` FOREIGN KEY (`entry_id`) REFERENCES `entry` (`entry_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `coll_entry_ibfk_2` FOREIGN KEY (`collector`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Data for table "coll_entry"
#

INSERT INTO `coll_entry` VALUES (7,1111,'2018-03-18 17:19:39');

#
# Structure for table "attention_info"
#

DROP TABLE IF EXISTS `attention_info`;
CREATE TABLE `attention_info` (
  `att_id` int(11) NOT NULL AUTO_INCREMENT,
  `pay_id` int(11) DEFAULT NULL,
  `be_paid_id` int(11) DEFAULT NULL,
  `pay_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`att_id`),
  KEY `be_paid_id` (`be_paid_id`),
  KEY `pay_id` (`pay_id`),
  CONSTRAINT `attention_info_ibfk_1` FOREIGN KEY (`be_paid_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `attention_info_ibfk_2` FOREIGN KEY (`pay_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

#
# Data for table "attention_info"
#

INSERT INTO `attention_info` VALUES (1,1111,1114,'2018-03-17 16:17:06');

#
# Structure for table "activity"
#

DROP TABLE IF EXISTS `activity`;
CREATE TABLE `activity` (
  `act_id` int(11) NOT NULL AUTO_INCREMENT,
  `publisher` int(11) DEFAULT NULL,
  `title` char(20) DEFAULT NULL,
  `content` text NOT NULL,
  `hold_addr` char(100) DEFAULT NULL,
  `act_src` text,
  `issue_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `hold_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`act_id`),
  KEY `publisher` (`publisher`),
  CONSTRAINT `activity_ibfk_1` FOREIGN KEY (`publisher`) REFERENCES `user` (`user_id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;

#
# Data for table "activity"
#

INSERT INTO `activity` VALUES (2,1111,'hh','hh','北京','baidu','2018-03-18 09:04:50','2018-03-18 09:04:50'),(3,1111,'1111','hhhh','beij','baidu','2018-03-18 21:10:41','2018-01-01 00:00:00'),(4,1111,'123','welcome','北京','http://baidu.com','2018-03-31 18:22:19','2018-04-01 00:00:00'),(5,1118,'皮影戏','111','北京','http/:baidu.com','2018-03-31 21:44:39','2018-07-08 00:00:00'),(6,1118,'古法培训','111','北京','http/:baidu.com','2018-03-31 21:44:59','2018-07-08 00:00:00'),(7,1118,'古法培训','111','武汉','http/:baidu.com','2018-03-31 21:45:09','2018-07-08 00:00:00'),(8,1118,'古法培训','111','湖北武汉','http/:baidu.com','2018-03-31 21:45:28','2018-07-08 00:00:00'),(9,1118,'皮影戏培训','111','湖北武汉','http/:baidu.com','2018-03-31 21:45:40','2018-07-08 00:00:00'),(10,1118,'皮影戏','111','湖北武汉','http/:baidu.com','2018-03-31 21:45:48','2018-07-08 00:00:00'),(11,1118,'皮影戏','111','北京','http/:baidu.com','2018-03-31 21:45:54','2018-07-08 00:00:00');

#
# Structure for table "coll_activity"
#

DROP TABLE IF EXISTS `coll_activity`;
CREATE TABLE `coll_activity` (
  `act_id` int(11) NOT NULL,
  `collector` int(11) NOT NULL,
  `coll_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`act_id`,`collector`),
  KEY `collector` (`collector`),
  CONSTRAINT `coll_activity_ibfk_1` FOREIGN KEY (`act_id`) REFERENCES `activity` (`act_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `coll_activity_ibfk_2` FOREIGN KEY (`collector`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Data for table "coll_activity"
#

INSERT INTO `coll_activity` VALUES (3,1111,'2018-03-23 21:46:59');

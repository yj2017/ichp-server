﻿# Host: localhost  (Version 5.7.17-log)
# Date: 2018-04-01 17:45:00
# Generator: MySQL-Front 5.4  (Build 3.52)
# Internet: http://www.mysqlfront.de/

/*!40101 SET NAMES utf8 */;

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

# Host: localhost  (Version 5.7.17-log)
# Date: 2018-04-26 17:34:31
# Generator: MySQL-Front 5.4  (Build 3.52)
# Internet: http://www.mysqlfront.de/

/*!40101 SET NAMES utf8 */;

#
# Structure for table "coll_activity"
#

DROP TABLE IF EXISTS `coll_activity`;
CREATE TABLE `coll_activity` (
  `act_id` int(11) NOT NULL,
  `collector` int(11) NOT NULL,
  `coll_date` datetime DEFAULT CURRENT_TIMESTAMP,
  KEY `collector` (`collector`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Data for table "coll_activity"
#

INSERT INTO `coll_activity` VALUES (22,1119,'2018-04-26 17:12:24'),(9,1119,'2018-04-26 17:12:30'),(7,1119,'2018-04-26 17:15:44');

#
# Structure for table "coll_entry"
#

DROP TABLE IF EXISTS `coll_entry`;
CREATE TABLE `coll_entry` (
  `entry_id` int(11) NOT NULL,
  `collector` int(11) NOT NULL,
  `coll_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`entry_id`,`collector`),
  KEY `collector` (`collector`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Data for table "coll_entry"
#

INSERT INTO `coll_entry` VALUES (9,1119,'2018-04-26 17:25:02');

#
# Structure for table "coll_record"
#

DROP TABLE IF EXISTS `coll_record`;
CREATE TABLE `coll_record` (
  `rec_id` int(11) NOT NULL,
  `collector` int(11) NOT NULL,
  `coll_date` datetime DEFAULT CURRENT_TIMESTAMP,
  KEY `collector` (`collector`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Data for table "coll_record"
#

INSERT INTO `coll_record` VALUES (20,1119,'2018-04-26 16:57:22'),(23,1119,'2018-04-26 15:18:07'),(37,1119,'2018-04-25 10:34:39');

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
) ENGINE=InnoDB AUTO_INCREMENT=1128 DEFAULT CHARSET=utf8;

#
# Data for table "user"
#

INSERT INTO `user` VALUES (1119,0,'134','123456','http://p5o94s90i.bkt.clouddn.com/eb070226-3f02-11e8-8bee-525400ae50a0tooopen_sy_139205349641.jpg','mm','mm',3890,'wuruoye','2018-04-12 16:44:14'),(1120,0,NULL,'123',NULL,NULL,NULL,0,'zq','2018-04-12 22:02:14'),(1121,0,NULL,'123',NULL,NULL,NULL,100,'zqq','2018-04-12 22:03:01'),(1122,0,NULL,'123456',NULL,NULL,NULL,0,'wuruoy','2018-04-12 22:03:31'),(1123,0,NULL,'123',NULL,NULL,NULL,0,'zqqq','2018-04-12 22:05:22'),(1124,1,'','123456','http://p5o94s90i.bkt.clouddn.com/ad2781dc-3f26-11e8-8bee-525400ae50a0tooopen_sy_139205349641.jpg','','',1610,'wuruoyee','2018-04-13 14:33:59'),(1125,1,'12345678911','123456','http://baidu.com','tt','frdgvb',300,'hh','2018-04-13 15:33:09'),(1126,1,'','980924','http://p5o94s90i.bkt.clouddn.com/7e1690fe-3f85-11e8-8bee-525400ae50a02025054453.jpg','','',3160,'zwzw','2018-04-14 09:37:52'),(1127,0,NULL,'123456',NULL,NULL,NULL,0,'yml','2018-04-14 12:00:20');

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
  `discribe` char(255) DEFAULT NULL,
  `labels_id_str` char(12) DEFAULT NULL,
  PRIMARY KEY (`rec_id`),
  KEY `recorder` (`recorder`),
  CONSTRAINT `record_ibfk_1` FOREIGN KEY (`recorder`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8;

#
# Data for table "record"
#

INSERT INTO `record` VALUES (20,1124,'标题3','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/aaaca622-3f89-11e8-8bee-525400ae50a0tooopen_sy_139205349641.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]',0,'湖北省武汉市武昌区友谊大道辅路,30.609757,114.355843',0,0,'2018-04-14 10:15:14','内容3','9'),(22,1126,'测试','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/a1b5feb2-3f8c-11e8-8bee-525400ae50a0magazine-unlock-01-2.3.949-_31394df8393240a8b4d1d9da53ea1261.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]',0,'湖北省武汉市武昌区交通一路,30.60611859127983,114.35099984597609',0,0,'2018-04-14 10:36:31','啊','13'),(25,1124,'标题','[\"{\\\"url\\\":\\\"\\\",\\\"type\\\":\\\"\\\"}\"]',0,' , ,',0,0,'2018-04-14 11:13:37','内容','9'),(26,1126,'测试','[\"{\\\"url\\\":\\\"\\\",\\\"type\\\":\\\"\\\"}\"]',0,' ,0,0',0,0,'2018-04-14 11:20:30','测试','13'),(27,1124,'标题','[\"{\\\"url\\\":\\\"\\\",\\\"type\\\":\\\"\\\"}\"]',0,'湖北省武汉市武昌区友谊大道辅路,30.609752,114.355827',0,0,'2018-04-14 11:22:22','内容','9'),(28,1124,'标题','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/5f280067-3f93-11e8-8bee-525400ae50a0tooopen_sy_139205349641.jpg\\\",\\\"type\\\":\\\"1\\\"}\",\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/5f280066-3f93-11e8-8bee-525400ae50a0tooopen_sy_139205349641.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]',0,'湖北省武汉市武昌区友谊大道辅路,30.609752,114.355827',0,0,'2018-04-14 11:24:44','内容','9'),(29,1126,'测试图','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/d79907f2-3f93-11e8-8bee-525400ae50a045D53C5NFES{ATKC0N6NF[L.png\\\",\\\"type\\\":\\\"1\\\"}\"]',0,'湖北省武汉市武昌区友谊大道辅路,30.606032903621884,114.351119810094',0,0,'2018-04-14 11:28:07','测试','13'),(30,1126,'成都糖画','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/f72ea266-3f93-11e8-8bee-525400ae50a02025054453.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]',0,'湖北省武汉市武昌区友谊大道辅路,30.60606302055407,114.35104548266473',0,0,'2018-04-14 11:28:59','糖画测试','12'),(31,1126,'高龙','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/b1602e02-3f94-11e8-8bee-525400ae50a0HJ~}J%0OU{P9EB~GB_)@@]M.png\\\",\\\"type\\\":\\\"1\\\"}\"]',0,'湖北省武汉市武昌区友谊大道辅路,30.60605718794061,114.3510748960031',0,0,'2018-04-14 11:34:10','高龙','15'),(33,1126,'测试','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/30b4b096-3f96-11e8-8bee-525400ae50a02025054453.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]',0,'湖北省武汉市武昌区友谊大道辅路,30.606120070459642,114.35081358566353',0,0,'2018-04-14 11:44:54','测试','13'),(35,1126,'测试','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/ce6344a4-3f98-11e8-8bee-525400ae50a02025054453.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]',0,'湖北省武汉市武昌区友谊大道辅路,30.60597585884165,114.3509640652218',0,0,'2018-04-14 12:03:38','测试','13'),(36,1126,'测试','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/0c0ed066-3f99-11e8-8bee-525400ae50a02025054453.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]',0,'湖北省武汉市武昌区交通一路,30.606103901385666,114.35130588829918',0,0,'2018-04-14 12:05:21','测试','13'),(37,1126,'测试','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/9a7cfeca-3faa-11e8-8bee-525400ae50a02025054453.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]',0,' ,0,0',2,0,'2018-04-14 14:11:02','测试','13');

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Data for table "mail"
#


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
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;

#
# Data for table "entry"
#

INSERT INTO `entry` VALUES (9,'123','content',1119,'url'),(10,'1234','content',1119,'url'),(11,'1','1',1119,'http://p5o94s90i.bkt.clouddn.com/c242cbd8-3eb5-11e8-8bee-525400ae50a0tooopen_sy_139205349641.jpg'),(12,'成都糖画','成都的非遗项目',1126,'http://p5o94s90i.bkt.clouddn.com/39ec2f6a-3f85-11e8-8bee-525400ae50a02025054453.jpg'),(13,'汉剧','湖北省地方戏曲剧种之一，皮簧腔系主要剧种。早期称“楚腔”、“楚调”，以后又称“汉调”、“汉戏”，俗称“二簧”。在鄂北有“一清二簧三越调”的谚语;而在鄂东又有“一清二弹”之说，称汉剧为“乱弹”或“弹戏”。文献记载中曾有“湖广调”、“黄腔”、“皮簧”等称谓。辛亥革命前仍称“汉调”，从民国初年起开始改称“汉剧”。汉剧流行于湖北省境内的长江和汉水流域及其邻近的河南、湖南、陕西、四川等省的部分地区。代表人物有陈伯华、吴天保等;代表剧目有《宇宙锋》等。',1126,'http://p5o94s90i.bkt.clouddn.com/5256b222-3f86-11e8-8bee-525400ae50a0汉剧.jpg'),(15,'高龙','武汉高龙的发祥地在汉阳地区，盛行于汉阳区江堤乡鲤鱼洲和永丰乡龙阳湖一带，那里从古至今都时兴舞高龙，其中江堤乡渔业村高龙队、永丰乡龙阳村高龙队是杰出代表。',1126,'http://p5o94s90i.bkt.clouddn.com/a8d5907e-3f94-11e8-8bee-525400ae50a0HJ~}J%0OU{P9EB~GB_)@@]M.png');

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
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;

#
# Data for table "comm_rec"
#

INSERT INTO `comm_rec` VALUES (23,22,1124,'评论',0,'2018-04-14 11:00:35'),(24,28,1124,'困',0,'2018-04-14 11:25:31'),(26,37,1119,'评论',0,'2018-04-24 12:46:36');

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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

#
# Data for table "comm_comm"
#

INSERT INTO `comm_comm` VALUES (1,23,1124,'hnjftgcjndcj',1,'2018-04-18 22:00:00');

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Data for table "attention_info"
#


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
  `image_src` text,
  `labels_id_str` char(12) DEFAULT NULL,
  PRIMARY KEY (`act_id`),
  KEY `publisher` (`publisher`),
  CONSTRAINT `activity_ibfk_1` FOREIGN KEY (`publisher`) REFERENCES `user` (`user_id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;

#
# Data for table "activity"
#

INSERT INTO `activity` VALUES (7,1124,'标题','内容','地点','入口','2018-04-14 07:56:16','2018-04-04 00:00:00','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/410142d6-3f76-11e8-8bee-525400ae50a0tooopen_sy_139205349641.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]','9'),(8,1124,'标题2','内容2','武汉理工大学','无','2018-04-14 08:38:05','2018-04-14 00:00:00','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/173f2e31-3f7c-11e8-8bee-525400ae50a0tooopen_sy_139205349641.jpg\\\",\\\"type\\\":\\\"1\\\"}\",\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/173f2e30-3f7c-11e8-8bee-525400ae50a0tooopen_sy_139205349641.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]','9'),(9,1126,'成都糖画学习','糖画学习','武汉理工大学余家头校区','www.whut.edu.com','2018-04-14 09:44:48','2018-05-04 00:00:00','[\"{\\\"url\\\":\\\"\\\",\\\"type\\\":\\\"\\\"}\"]','12'),(10,1126,'汉剧赏析活动','汉剧赏析','武汉','www','2018-04-14 10:34:37','2018-05-04 00:00:00','[\"{\\\"url\\\":\\\"\\\",\\\"type\\\":\\\"\\\"}\"]','13'),(11,1126,'成都糖画','测试','aaa','444','2018-04-14 11:43:11','2018-04-15 00:00:00','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/e85df5a0-3f95-11e8-8bee-525400ae50a02025054453.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]','13'),(12,1126,'测试','测试','aaa','aaa','2018-04-14 11:43:35','2018-04-15 00:00:00','[\"{\\\"url\\\":\\\"\\\",\\\"type\\\":\\\"\\\"}\"]','13'),(13,1126,'测试','测试','888','888','2018-04-14 11:44:16','2018-05-05 00:00:00','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/19e2612e-3f96-11e8-8bee-525400ae50a02025054453.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]','13'),(14,1126,'测试','测试','888','888','2018-04-14 11:46:06','2018-04-08 00:00:00','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/5ade50b6-3f96-11e8-8bee-525400ae50a02025054453.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]','13'),(15,1126,'测试','测试','888','888','2018-04-14 11:46:42','2018-08-08 00:00:00','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/70dbbea8-3f96-11e8-8bee-525400ae50a02025054453.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]','13'),(16,1126,'测试','测试','888','888','2018-04-14 11:47:35','2018-08-08 00:00:00','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/9046b84c-3f96-11e8-8bee-525400ae50a02025054453.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]','13'),(17,1126,'测试','测试','测试','测试','2018-04-14 11:48:04','2018-08-08 00:00:00','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/a1cdfefe-3f96-11e8-8bee-525400ae50a02025054453.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]','13'),(18,1126,'测试','测试','888','888','2018-04-14 11:48:36','2018-08-08 00:00:00','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/b4f1c8ee-3f96-11e8-8bee-525400ae50a02025054453.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]','13'),(19,1126,'测试','测试','888','888','2018-04-14 11:49:09','2018-08-08 00:00:00','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/c86dac12-3f96-11e8-8bee-525400ae50a02025054453.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]','13'),(20,1126,'测试','测试','888','888','2018-04-14 11:50:00','2018-08-08 00:00:00','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/e6d8b55c-3f96-11e8-8bee-525400ae50a02025054453.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]','13'),(21,1126,'测试','测试','888','888','2018-04-14 12:06:11','2018-08-08 00:00:00','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/282e03ca-3f99-11e8-8bee-525400ae50a02025054453.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]','13'),(22,1126,'测试','测试','888','888','2018-04-14 12:06:11','2018-08-08 00:00:00','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/282e03cb-3f99-11e8-8bee-525400ae50a02025054453.jpg\\\",\\\"type\\\":\\\"1\\\"}\",\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/282e03ca-3f99-11e8-8bee-525400ae50a02025054453.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]','13');

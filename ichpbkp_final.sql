-- MySQL dump 10.13  Distrib 5.7.22, for Linux (x86_64)
--
-- Host: localhost    Database: ichp
-- ------------------------------------------------------
-- Server version	5.7.22-0ubuntu0.16.04.1

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
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activity`
--

LOCK TABLES `activity` WRITE;
/*!40000 ALTER TABLE `activity` DISABLE KEYS */;
INSERT INTO `activity` VALUES (25,1134,'牌子锣鼓技艺欣赏','行于武汉市新洲区的牌子锣(牌子锣鼓)，由古代鼓吹乐演绎发展而来。唐明皇(玄宗李隆基)将民间锣鼓音乐引入宫廷，依宫廷诗词歌赋作曲，书于木牌，供演奏时对照，故名“牌子锣鼓”。为牌子锣鼓作曲的一名乐师，被唐明皇封为“老郎”，并规定农历3月18日为“老郎”纪念日。此后牌子锣鼓又从宫廷流传到民间，多用于婚丧、祝寿、祭祀等仪式。','湖北省武汉市新洲区','www.dizhi.com','2018-05-02 20:14:59','2018-08-08 00:00:00','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/6eea689a-4e02-11e8-8bee-525400ae50a0tiny-109-2018-05-02-20-14-58.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]','20,21,22'),(26,1134,'武汉归元庙会活动','有着悠久历史的归元庙会既是一项民间传统文化娱乐活动，也是一场热热闹闹的商贸活动。1963年春节，归元寺曾举行过一次庙会。文革期间，时任方丈昌明法师上书周总理，请求保护寺庙，得到总理亲自批示，归元寺因此幸免于浩劫。1977年，归元禅寺重新对外开放，但传统的庙会活动没有恢复。\r\n为满足市民的文化生活需求，1989年开始，汉阳区重新恢复举办庙会，2001年正式定名为武汉归元庙会。','湖北省武汉市归元庙','www.dizhi.com','2018-05-02 20:19:28','2018-08-08 00:00:00','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/0f265f6c-4e03-11e8-8bee-525400ae50a0tiny-87-2018-05-02-20-19-27.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]','23,24'),(27,1134,'鲁班锁体验学习','鲁班锁，起源于古代中国建筑中首创的榫卯结构。这种三维的拼插器具内部的凹凸部分（即榫卯结构）啮合，十分巧妙。原创为木质结构，外观看是严丝合缝的十字立方体。 孔明锁类玩具比较多，形状和内部的构造各不相同，一般都是易拆难装。拼装时需要仔细观察，认真思考，分析其内部结构。它有利于开发大脑，灵活手指，是一种很好的益智玩具。','湖北省武汉市武昌区楚河汉街1号云旅游客厅','http://www.cjfygift.com/intangibleNews/newsInfo?id=185&type=26','2018-05-02 20:27:20','2018-08-08 00:00:00','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/2849b8e5-4e04-11e8-8bee-525400ae50a0tiny-217-2018-05-02-20-27-19.jpg\\\",\\\"type\\\":\\\"1\\\"}\",\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/2849b8e4-4e04-11e8-8bee-525400ae50a0tiny-989-2018-05-02-20-27-19.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]','25'),(28,1134,'汉绣体验课','简单讲解汉绣基本知识，在绣绷上体验绣制过程。','湖北省武汉市沿江大道武汉巷科技馆旁','http://www.cjfygift.com/intangibleNews/newsInfo?id=185&type=26','2018-05-02 20:32:05','2018-08-08 00:00:00','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/d2a4c5c2-4e04-11e8-8bee-525400ae50a0tiny-703-2018-05-02-20-32-05.jpg\\\",\\\"type\\\":\\\"1\\\"}\",\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/d2a4c5c3-4e04-11e8-8bee-525400ae50a0tiny-731-2018-05-02-20-32-05.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]','16'),(29,1135,'长沙弹词欣赏','长沙弹词在不同的历史时期发挥着其历史补遗，警示教育、休闲娱乐的功能，他是具有浓郁地方特色的古老曲证。是湖湘曲苑三大演唱艺术之一。在表演艺术上以其丰富的曲目，以生动、形象的演唱方式，在很长的历史时期内广泛地在人民大众中流传，被誉为长沙历史文化艺术的“活化石”。是我省著名曲艺艺术品牌。保护、传承好长沙弹词，对湖湘文化及中国民间文化艺术的研究都有着极高的价值。','湖南省长沙市','www.dizhi.com','2018-05-02 20:41:05','2018-08-08 00:00:00','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/144a04be-4e06-11e8-8bee-525400ae50a0tiny-448-2018-05-02-20-41-04.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]','26,27'),(30,1135,'湖南祁剧赏析','祁剧，也叫祁阳戏，楚南戏，因发祥于湖南省祁阳县而得名。明朝中叶，“弋阳腔”传入祁阳，与本地的民歌、小调相结合，形成了祁剧的雏形。明嘉靖时，祁剧已初具规模，明末清初相当盛行。现在，湘南、湘西、赣西南、桂北、粤北、闽西甚至新疆等地都有祁剧演出。','湖南省','www.dizhi.com','2018-05-02 20:47:15','2018-08-08 00:00:00','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/f0e5d2ae-4e06-11e8-8bee-525400ae50a0tiny-6-2018-05-02-20-47-14.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]','28,29'),(31,1135,'湘西土陶制作工艺学习','湘西土陶是土家族特有的生活用品，它的生产工序原始产品品种多，式样全。从生产工序和流程上看，它首先要选料，制丕，晒丕，装窑，烧窑等四个重要环节。产品品种主要有，碗、坛子、缸、盐、罐、油灯。 ','湖南省龙山县','www.dizhi.com','2018-05-02 20:52:19','2018-08-08 00:00:00','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/a5b856ca-4e07-11e8-8bee-525400ae50a0tiny-359-2018-05-02-20-52-17.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]','30,31'),(32,1135,'侗族芦笙吹奏学习','         侗族芦笙，是侗族民间传统的竹制簧管乐器，主要流传于通道侗族自治县。\r\n\r\n　　根据芦笙吹奏的形式和表演手法的不同，分为地筒、特大芦笙、大芦笙、中芦笙、小芦笙、最小芦笙6种。芦笙的筒身及吹管均由竹管构成，一筒一音。芦笙从传统的三音芦笙发展到多音芦笙。侗族芦笙曲牌现仅存九首。常用的曲牌有[集合曲]、[进堂曲]、[踩堂曲]、[扫堂曲]、[同去曲]、[上路曲]、[比赛曲]、[走曲]、[圆圈曲]等。','湖南省','www.dizhi.com','2018-05-02 20:55:47','2018-08-08 00:00:00','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/224731e8-4e08-11e8-8bee-525400ae50a0tiny-668-2018-05-02-20-55-46.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]','33,32'),(33,1136,'安徽池州傩戏欣赏','池州傩戏源于原始宗教意识和图腾崇拜意识，主要流传于中国佛教圣地九华山麓方圆百公里的贵池、石台和青阳等县（区），尤其集中于池州市贵池区的刘街、梅街、茅坦等乡镇几十个大姓家族，史载“无傩不成村”，至今仍以宗族为演出单位，以请神祭祖、驱邪纳福为目的，以戴面具为表演特征的古老艺术形式。 ','安徽省','www.dizhi.com','2018-05-02 21:07:26','2018-08-08 00:00:00','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/c2f9ade0-4e09-11e8-8bee-525400ae50a0tiny-303-2018-05-02-21-07-26.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]','35,28'),(34,1136,'细阳刺绣学习','细阳刺绣已有一千多年的历史，它来自民间，有着广泛的群众基础，由于地处中原，吸收东西南北文化于一体，因此，细阳刺绣形成自己的独特风格：既有粤绣的富丽堂皇，蜀绣的细腻、京绣的端庄，苏绣的秀丽与妩媚，又有卞绣的粗狂与古朴。绣品精细规整，色彩浓艳，花纹苍劲，形象优美，质地坚牢。 细阳刺绣技艺繁琐而细致，是皖北独有的工艺制作，工艺水平的高低对于研究当时社会的自然经济和生产力水平的发展有着重要的历史参考价值。','安徽省','www.dizhi.com','2018-05-02 21:10:56','2018-08-08 00:00:00','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/4976797a-4e0a-11e8-8bee-525400ae50a0tiny-952-2018-05-02-21-11-11.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]','37,36');
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
  `pay_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`att_id`),
  KEY `be_paid_id` (`be_paid_id`),
  KEY `pay_id` (`pay_id`),
  CONSTRAINT `attention_info_ibfk_1` FOREIGN KEY (`be_paid_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `attention_info_ibfk_2` FOREIGN KEY (`pay_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attention_info`
--

LOCK TABLES `attention_info` WRITE;
/*!40000 ALTER TABLE `attention_info` DISABLE KEYS */;
INSERT INTO `attention_info` VALUES (29,1131,1132,'2018-05-01 22:53:31'),(30,1133,1132,'2018-05-02 18:39:01'),(31,1134,1132,'2018-05-02 20:04:55'),(32,1136,1135,'2018-05-02 21:34:38'),(33,1132,1134,'2018-05-03 08:13:20'),(34,1137,1135,'2018-05-03 11:28:00');
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
  `coll_date` datetime DEFAULT CURRENT_TIMESTAMP,
  KEY `collector` (`collector`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coll_activity`
--

LOCK TABLES `coll_activity` WRITE;
/*!40000 ALTER TABLE `coll_activity` DISABLE KEYS */;
INSERT INTO `coll_activity` VALUES (27,1133,'2018-05-02 20:30:48'),(25,1133,'2018-05-02 20:30:54'),(31,1136,'2018-05-02 21:12:28'),(31,1132,'2018-05-03 13:47:37');
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
  `coll_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`entry_id`,`collector`),
  KEY `collector` (`collector`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coll_entry`
--

LOCK TABLES `coll_entry` WRITE;
/*!40000 ALTER TABLE `coll_entry` DISABLE KEYS */;
INSERT INTO `coll_entry` VALUES (18,1133,'2018-05-02 19:37:07'),(23,1133,'2018-05-02 20:31:20');
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
  `coll_date` datetime DEFAULT CURRENT_TIMESTAMP,
  KEY `collector` (`collector`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coll_record`
--

LOCK TABLES `coll_record` WRITE;
/*!40000 ALTER TABLE `coll_record` DISABLE KEYS */;
INSERT INTO `coll_record` VALUES (46,1131,'2018-05-01 22:53:59'),(45,1133,'2018-05-02 18:40:05'),(44,1133,'2018-05-02 18:57:31'),(46,1133,'2018-05-02 18:59:23'),(48,1132,'2018-05-03 13:47:32'),(49,1132,'2018-05-03 13:47:41');
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
  `appr_num` int(11) DEFAULT NULL,
  `comm_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`comm_comm_id`),
  KEY `commer` (`commer`),
  KEY `comm_rec_id` (`comm_rec_id`),
  CONSTRAINT `comm_comm_ibfk_1` FOREIGN KEY (`commer`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `comm_comm_ibfk_2` FOREIGN KEY (`comm_rec_id`) REFERENCES `comm_rec` (`comm_rec_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
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
  `appr_num` int(11) DEFAULT NULL,
  `comm_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`comm_rec_id`),
  KEY `commer` (`commer`),
  KEY `rec_id` (`rec_id`),
  CONSTRAINT `comm_rec_ibfk_1` FOREIGN KEY (`commer`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `comm_rec_ibfk_2` FOREIGN KEY (`rec_id`) REFERENCES `record` (`rec_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comm_rec`
--

LOCK TABLES `comm_rec` WRITE;
/*!40000 ALTER TABLE `comm_rec` DISABLE KEYS */;
INSERT INTO `comm_rec` VALUES (40,44,1133,'评论',0,'2018-05-01 21:23:51'),(41,46,1131,'赞一个！',0,'2018-05-01 22:56:40'),(42,46,1134,'感兴趣！',0,'2018-05-03 10:51:13');
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
  `name` char(12) NOT NULL DEFAULT '',
  `content` text NOT NULL,
  `editor` int(11) DEFAULT NULL,
  `url` text,
  PRIMARY KEY (`entry_id`),
  KEY `editor` (`editor`),
  CONSTRAINT `entry_ibfk_1` FOREIGN KEY (`editor`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entry`
--

LOCK TABLES `entry` WRITE;
/*!40000 ALTER TABLE `entry` DISABLE KEYS */;
INSERT INTO `entry` VALUES (16,'汉绣','汉绣，中国特色传统刺绣工艺之一，以楚绣为基础，融汇南北诸家绣法之长，揉合出了富有鲜明地方特色的新绣法。汉绣主要流行于湖北的荆州、荆门，武汉、洪湖、仙桃，潜江一带。',1132,'http://p5o94s90i.bkt.clouddn.com/83bd8d80-4d42-11e8-8bee-525400ae50a0tiny-541-2018-05-01-21-21-10.jpg'),(17,'北京面人','面人也称面塑，是一种制作简单但艺术性很高的中国传统手工艺品。它先是用面粉、糯米粉为主要原料，再加上色彩、石蜡、蜂蜜等成分，经过防裂防霉处理，制成柔软的各色面团。面塑的形象多是传统戏曲、四大名著、民间传说、神话故事、儿童卡通中的人物以及十二生肖和其他动物。比如刘备、关羽、张飞、福禄寿、八仙、嫦娥、哪吒、唐僧 师徒等。                                         ',1132,'http://p5o94s90i.bkt.clouddn.com/f9feed80-4d43-11e8-8bee-525400ae50a0tiny-966-2018-05-01-21-31-38.jpg'),(18,'成都糖画','成都糖画是集民间工艺美术与美食于一体独特的传统手工技艺，主要流传于四川省成都市及周边地区。四川民间过去又称倒糖饼儿、糖粑粑儿、糖灯影儿等。',1134,'http://p5o94s90i.bkt.clouddn.com/65ea962a-4d44-11e8-8bee-525400ae50a0tiny-671-2018-05-01-21-34-39.jpg'),(19,'传统技艺',' 传统技艺是民间传承下来的技艺，每一门技艺都烙着民族的印记。传统技艺包括：剪纸，陶艺，年画，皮影，还有变脸，刺绣，泥塑，木刻，木雕，舞龙，戏曲等等',1132,'http://p5o94s90i.bkt.clouddn.com/cd41b68c-4d4e-11e8-8bee-525400ae50a0tiny-931-2018-05-01-22-49-07.jpg'),(20,'鼓吹乐','以打击乐器、吹奏乐器等合奏形式为主的传统音乐。',1134,'http://p5o94s90i.bkt.clouddn.com/27dc9b94-4e02-11e8-8bee-525400ae50a0tiny-620-2018-05-02-20-12-59.jpg'),(21,'锣鼓','锣鼓是中国民俗文化中必不可少的乐器。是戏剧节奏的支柱。',1134,'http://p5o94s90i.bkt.clouddn.com/4678faa2-4e02-11e8-8bee-525400ae50a0tiny-782-2018-05-02-20-13-50.jpg'),(22,'牌子锣鼓','行于武汉市新洲区的牌子锣(牌子锣鼓)，由古代鼓吹乐演绎发展而来。唐明皇(玄宗李隆基)将民间锣鼓音乐引入宫廷，依宫廷诗词歌赋作曲，书于木牌，供演奏时对照，故名“牌子锣鼓”。',1134,'http://p5o94s90i.bkt.clouddn.com/66773404-4e02-11e8-8bee-525400ae50a0tiny-60-2018-05-02-20-14-44.jpg'),(23,'庙会','庙会，又称“庙市”或“节场”。是中国民间宗教及岁时风俗，一般在农历新年、元宵节、二月二龙抬头等节日举行。',1134,'http://p5o94s90i.bkt.clouddn.com/f2255c2e-4e02-11e8-8bee-525400ae50a0tiny-847-2018-05-02-20-18-38.jpg'),(24,'归元庙会','有着悠久历史的归元庙会既是一项民间传统文化娱乐活动，也是一场热热闹闹的商贸活动。1963年春节，归元寺曾举行过一次庙会。文革期间，时任方丈昌明法师上书周总理，请求保护寺庙，得到总理亲自批示，归元寺因此幸免于浩劫。',1134,'http://p5o94s90i.bkt.clouddn.com/060c2f42-4e03-11e8-8bee-525400ae50a0tiny-991-2018-05-02-20-19-11.jpg'),(25,'鲁班锁','鲁班锁，起源于古代中国建筑中首创的榫卯结构。这种三维的拼插器具内部的凹凸部分（即榫卯结构）啮合，十分巧妙。原创为木质结构，外观看是严丝合缝的十字立方体。 孔明锁类玩具比较多，形状和内部的构造各不相同，一般都是易拆难装。拼装时需要仔细观察，认真思考，分析其内部结构。它有利于开发大脑，灵活手指，是一种很好的益智玩具。',1134,'http://p5o94s90i.bkt.clouddn.com/1e62840a-4e04-11e8-8bee-525400ae50a0tiny-507-2018-05-02-20-27-02.jpg'),(26,'长沙弹词','长沙弹词在不同的历史时期发挥着其历史补遗，警示教育、休闲娱乐的功能，他是具有浓郁地方特色的古老曲证。是湖湘曲苑三大演唱艺术之一。在表演艺术上以其丰富的曲目，以生动、形象的演唱方式，在很长的历史时期内广泛地在人民大众中流传，被誉为长沙历史文化艺术的“活化石”。是我省著名曲艺艺术品牌。保护、传承好长沙弹词，对湖湘文化及中国民间文化艺术的研究都有着极高的价值。',1135,'http://p5o94s90i.bkt.clouddn.com/e75e8bbe-4e05-11e8-8bee-525400ae50a0tiny-603-2018-05-02-20-39-49.jpg'),(27,'曲艺','曲艺是中华民族各种“说唱艺术”的统称，它是由民间口头文学和歌唱艺术经过长期发展演变形成的一种独特的艺术形式。',1135,'http://p5o94s90i.bkt.clouddn.com/0f1d77f0-4e06-11e8-8bee-525400ae50a0tiny-761-2018-05-02-20-40-56.jpg'),(28,'戏剧','戏剧，指以语言、动作、舞蹈、音乐、木偶等形式达到叙事目的的舞台表演艺术的总称。文学上的戏剧概念是指为戏剧表演所创作的脚本，即剧本。戏剧的表演形式多种多样，常见的包括话剧、歌剧、舞剧、音乐剧、木偶戏等。',1135,'http://p5o94s90i.bkt.clouddn.com/c74440e8-4e06-11e8-8bee-525400ae50a0tiny-589-2018-05-02-20-46-04.jpg'),(29,'祁剧','祁剧，也叫祁阳戏，楚南戏，因发祥于湖南省祁阳县而得名。明朝中叶，“弋阳腔”传入祁阳，与本地的民歌、小调相结合，形成了祁剧的雏形。明嘉靖时，祁剧已初具规模，明末清初相当盛行。现在，湘南、湘西、赣西南、桂北、粤北、闽西甚至新疆等地都有祁剧演出。',1135,'http://p5o94s90i.bkt.clouddn.com/e5957cc4-4e06-11e8-8bee-525400ae50a0tiny-963-2018-05-02-20-46-55.jpg'),(30,'湘西土陶','湘西土陶是土家族特有的生活用品，它的生产工序原始产品品种多，式样全。从生产工序和流程上看，它首先要选料，制丕，晒丕，装窑，烧窑等四个重要环节。产品品种主要有，碗、坛子、缸、盐、罐、油灯。 ',1135,'http://p5o94s90i.bkt.clouddn.com/7b689eca-4e07-11e8-8bee-525400ae50a0tiny-664-2018-05-02-20-51-06.jpg'),(31,'陶艺','陶艺，广泛讲是中国传统古老文化与现代艺术结合的艺术形式。从历史的发展可知，“陶瓷艺术”是一门综合艺术，经历了一个复杂而漫长的文化积淀历程。',1135,'http://p5o94s90i.bkt.clouddn.com/9d6a52a2-4e07-11e8-8bee-525400ae50a0tiny-656-2018-05-02-20-52-04.jpg'),(32,'侗族芦笙','侗族芦笙，是侗族民间传统的竹制簧管乐器，主要流传于通道侗族。根据芦笙吹奏的形式和表演手法的不同，分为地筒、特大芦笙、大芦笙、中芦笙、小芦笙、最小芦笙6种。芦笙的筒身及吹管均由竹管构成，一筒一音。芦笙从传统的三音芦笙发展到多音芦笙。侗族芦笙曲牌现仅存九首。常用的曲牌有[集合曲]、[进堂曲]、[踩堂曲]、[扫堂曲]、[同去曲]、[上路曲]、[比赛曲]、[走曲]、[圆圈曲]等。',1135,'http://p5o94s90i.bkt.clouddn.com/0f65d85e-4e08-11e8-8bee-525400ae50a0tiny-375-2018-05-02-20-55-13.jpg'),(33,'芦笙','芦笙，为西南地区苗、瑶、侗等民族的簧管乐器。 发源于中原，后来在少数民族地区发扬光大，其前身为竽。',1135,'http://p5o94s90i.bkt.clouddn.com/1aaa3b74-4e08-11e8-8bee-525400ae50a0tiny-413-2018-05-02-20-55-33.jpg'),(34,'苗族古歌','苗族古歌是中国苗族中特有的口碑文献，历史悠久，内容极为丰富，对研究苗族古代的历史、农学、天文、饮食、生产、生活、婚姻、民俗、军事、科技、部族战争以及、民族迁徙等，具有十分重要的价值。',1132,'http://p5o94s90i.bkt.clouddn.com/ad4a949c-4e08-11e8-8bee-525400ae50a0tiny-133-2018-05-02-20-59-39.jpg'),(35,'池州傩戏','池州傩戏源于原始宗教意识和图腾崇拜意识，主要流传于中国佛教圣地九华山麓方圆百公里的贵池、石台和青阳等县（区），尤其集中于池州市贵池区的刘街、梅街、茅坦等乡镇几十个大姓家族，史载“无傩不成村”，至今仍以宗族为演出单位，以请神祭祖、驱邪纳福为目的，以戴面具为表演特征的古老艺术形式。 ',1136,'http://p5o94s90i.bkt.clouddn.com/ba8fb5c8-4e09-11e8-8bee-525400ae50a0tiny-228-2018-05-02-21-07-12.jpg'),(36,'细阳刺绣','细阳刺绣已有一千多年的历史，它来自民间，有着广泛的群众基础，由于地处中原，吸收东西南北文化于一体，因此，细阳刺绣形成自己的独特风格：既有粤绣的富丽堂皇，蜀绣的细腻、京绣的端庄，苏绣的秀丽与妩媚，又有卞绣的粗狂与古朴。绣品精细规整，色彩浓艳，花纹苍劲，形象优美，质地坚牢。 细阳刺绣技艺繁琐而细致，是皖北独有的工艺制作，工艺水平的高低对于研究当时社会的自然经济和生产力水平的发展有着重要的历史参考价值。',1136,'http://p5o94s90i.bkt.clouddn.com/1c943e9c-4e0a-11e8-8bee-525400ae50a0tiny-62-2018-05-02-21-09-56.jpg'),(37,'刺绣','刺绣是针线在织物上绣制的各种装饰图案的总称。刺绣分丝线刺绣和羽毛刺绣两种。就是用针将丝线或其他纤维、纱线以一定图案和色彩在绣料上穿刺，以绣迹构成花纹的装饰织物。它是用针和线把人的设计和制作添加在任何存在的织物上的一种艺术。刺绣是中国民间传统手工艺之一，在中国至少有二三千年历史。',1136,'http://p5o94s90i.bkt.clouddn.com/3af854d6-4e0a-11e8-8bee-525400ae50a0tiny-20-2018-05-02-21-10-47.jpg'),(38,'凤阳花鼓',' “凤阳花鼓”又称“花鼓”、“打花鼓”、“花鼓小锣”等。是集歌、舞、演奏、表演为一体的民间艺术。主要分布于凤阳县燃灯、小溪河等乡镇一带。 “花鼓”原是凤阳民间礼乐的领奏乐器，明初以后，凤阳移民出门卖艺时，将花鼓众多乐器中的一鼓一锣取出，唱着小曲走四方。流传中国大江南北的凤阳花鼓由此诞生。',1136,'http://p5o94s90i.bkt.clouddn.com/cc424ab4-4e0a-11e8-8bee-525400ae50a0tiny-106-2018-05-02-21-14-51.jpg'),(39,'高跷','高跷也叫“高跷秧歌”，是一种广泛流传于全国各地的民间舞蹈，因舞蹈时多双脚踩踏木跷而得名。高跷历史久远，源于古代百戏中的一种技术表演。',1139,'http://p5o94s90i.bkt.clouddn.com/ede99228-4e9e-11e8-8bee-525400ae50a0tiny-539-2018-05-03-14-55-13.jpg'),(40,'陕北秧歌','陕北秧歌是流传于陕西陕北高原的一种具有广泛群众性和代表性的地方传统舞蹈，又称\"闹红火\"、\"闹秧歌\"、\"闹社火\"、\"闹阳歌\"等。',1139,'http://p5o94s90i.bkt.clouddn.com/5d485762-4e9f-11e8-8bee-525400ae50a0tiny-421-2018-05-03-14-58-19.jpg'),(41,'秧歌','秧歌是中国（主要在北方地区）广泛流传的一种极具群众性和代表性的民间舞蹈的类称，不同地区有不同称谓和风格样式。在民间，对秧歌的称谓分为两种：踩跷表演的称为“高跷秧歌”，不踩跷表演的称为“地秧歌”。近代所称的“秧歌”大多指“地秧歌”。秧歌历史悠久，南宋周密在《武林旧事》中介绍的民间舞队中就有“村田乐”的记载，清代吴锡麟的《新年杂咏抄》中明文记载了现存秧歌与宋代“村田乐”的源流关系。',1139,'http://p5o94s90i.bkt.clouddn.com/66f7eaca-4e9f-11e8-8bee-525400ae50a0tiny-842-2018-05-03-14-58-36.jpg'),(42,'锦鸡舞','锦鸡舞以芦笙伴奏，表演时女性个个绾发高耸,头上插戴锦鸡银饰，穿绣花超短百褶裙，戴全套银项圈手镯，脚穿翘尖绣花鞋，打扮得像美丽的锦鸡一样。男性吹芦笙作前导，女性随后起舞，排成一字形，沿着逆时针方向转圆圈跳。',1139,'http://p5o94s90i.bkt.clouddn.com/b36b71c4-4e9f-11e8-8bee-525400ae50a0tiny-528-2018-05-03-15-00-44.jpg');
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
  `send_date` datetime DEFAULT CURRENT_TIMESTAMP,
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
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `record`
--

LOCK TABLES `record` WRITE;
/*!40000 ALTER TABLE `record` DISABLE KEYS */;
INSERT INTO `record` VALUES (44,1132,'汉绣体验','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/c57d07e6-4d42-11e8-8bee-525400ae50a0tiny-241-2018-05-01-21-23-00.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]',0,'湖北省武汉市武昌区友谊大道,30.60540069858335,114.35098899859084',2,1,'2018-05-01 21:23:01','\r\n汉绣，中国特色传统刺绣工艺之一，以楚绣为基础，融汇南北诸家绣法之长，揉合出了富有鲜明地方特色的新绣法。汉绣主要流行于湖北的荆州、荆门，武汉、洪湖、仙桃，潜江一带。','16'),(45,1132,'北京面人','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/0222121c-4d44-11e8-8bee-525400ae50a0tiny-229-2018-05-01-21-31-52.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]',0,'北京市朝阳区崔各庄地区崔各庄村西北方向,40.0309490000,116.4661670000',3,0,'2018-05-01 21:31:52','面人也称面塑，是一种制作简单但艺术性很高的中国传统手工艺品。它先是用面粉、糯米粉为主要原料，再加上色彩、石蜡、蜂蜜等成分，经过防裂防霉处理，制成柔软的各色面团。面塑的形象多是传统戏曲、四大名著、民间传说、神话故事、儿童卡通中的人物以及十二生肖和其他动物。比如刘备、关羽、张飞、福禄寿、八仙、嫦娥、哪吒、唐僧 师徒等。','17'),(46,1132,'成都糖画','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/75592631-4d44-11e8-8bee-525400ae50a0tiny-451-2018-05-01-21-35-05.jpg\\\",\\\"type\\\":\\\"1\\\"}\",\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/75592630-4d44-11e8-8bee-525400ae50a0tiny-566-2018-05-01-21-35-05.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]',0,'四川省成都市武侯区石羊场街道裕民村东北方向,30.5730950000,104.0661430000',7,2,'2018-05-01 21:35:06','成都糖画是集民间工艺美术与美食于一体独特的传统手工技艺，主要流传于四川省成都市及周边地区。四川民间过去又称倒糖饼儿、糖粑粑儿、糖灯影儿等。是用融化的糖汁作画曾广泛流行于四川省成都市及周边巴蜀大地城市乡村。列中国国家级第二批非物质文化遗产名录。','18'),(47,1135,'苗族古歌亲体验','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/c0bd35b6-4e08-11e8-8bee-525400ae50a0tiny-859-2018-05-02-21-00-12.jpg\\\",\\\"type\\\":\\\"1\\\"}\",\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/c0bd35b7-4e08-11e8-8bee-525400ae50a0tiny-867-2018-05-02-21-00-13.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]',0,'湖南省娄底市涟源市石马山镇,27.695864,111.720664',0,0,'2018-05-02 21:00:14','苗族古歌在湘、黔、渝、鄂四省市边区深受苗族群众喜爱。对加强边区民族团结，构建和谐社会具有十分重要的现实意义呢。','34'),(48,1134,'武汉归元庙会之行','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/403c475a-4e09-11e8-8bee-525400ae50a0tiny-319-2018-05-02-21-03-46.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]',0,'湖北省武汉市汉阳区建桥街,30.55,114.27',1,0,'2018-05-02 21:03:47','锣鼓响起来，高龙舞起来，作为武汉历史最悠久的庙会，也是武汉非物质文化遗产代表项目，归元庙会今天在汉阳江欣苑社区开锣了，现场还有不少颇具特色的传统文化表演。归元庙会将一直持续到正月十五元宵节，期间还会有楚剧、单口相声、湖北大鼓等一系列民俗表演精彩上演噢！','23,24'),(49,1136,'凤阳花鼓体验','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/870d5615-4e0c-11e8-8bee-525400ae50a0tiny-41-2018-05-02-21-27-14.jpg\\\",\\\"type\\\":\\\"1\\\"}\",\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/870d5612-4e0c-11e8-8bee-525400ae50a0tiny-109-2018-05-02-21-27-14.jpg\\\",\\\"type\\\":\\\"1\\\"}\",\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/870d5613-4e0c-11e8-8bee-525400ae50a0tiny-149-2018-05-02-21-27-14.jpg\\\",\\\"type\\\":\\\"1\\\"}\",\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/870d5614-4e0c-11e8-8bee-525400ae50a0tiny-617-2018-05-02-21-27-14.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]',0,'徽省滁州市凤阳县总铺镇鹿塘村西北方向,32.792215,117.611472',0,0,'2018-05-02 21:26:41',' “凤阳花鼓”又称“花鼓”、“打花鼓”、“花鼓小锣”等。是集歌、舞、演奏、表演为一体的民间艺术。主要分布于凤阳县燃灯、小溪河等乡镇一带。 “花鼓”原是凤阳民间礼乐的领奏乐器，明初以后，凤阳移民出门卖艺时，将花鼓众多乐器中的一鼓一锣取出，唱着小曲走四方。流传中国大江南北的凤阳花鼓由此诞生。','38,38'),(51,1139,'踩高跷','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/fe44a464-4e9e-11e8-8bee-525400ae50a0tiny-564-2018-05-03-14-55-40.jpg\\\",\\\"type\\\":\\\"1\\\"}\",\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/f3605c14-4e9e-11e8-8bee-525400ae50a0VID_20180503_145349.mp4\\\",\\\"type\\\":\\\"2\\\"}\"]',0,'天津市和平区南市街道裕德里社区,39.1362330000,117.1887910000',0,0,'2018-05-03 14:55:24','高跷的音乐伴奏是民间的锣鼓乐队伴奏。踩高跷的步伐，全靠锣鼓乐队的快慢指挥着高跷队的表演，十分有趣。因此人们编顺口溜说：堵单堵，高跷过来快些躲，踩着你，买上二两果丹皮','39'),(52,1139,'陕北秧歌表演','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/6dd493a2-4e9f-11e8-8bee-525400ae50a0tiny-322-2018-05-03-14-58-47.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]',0,'陕西省西安市莲湖区青年路街道莲湖路,34.2683800000,108.9466430000',0,0,'2018-05-03 14:58:48','在锣鼓乐器伴奏下以腰部为中心点，头和上体随双臂大幅度扭动，整支舞蹈热烈而充满欢快的氛围。陕北秧歌历史悠久，内容丰富，形式多样，以“绥德秧歌”最具代表性。\r\n人们的生活富起来了，日子越过越好，幸福全在这喜气洋洋的陕北秧歌中。','40,41'),(53,1139,'锦鸡舞欣赏','[\"{\\\"url\\\":\\\"http:\\\\\\/\\\\\\/p5o94s90i.bkt.clouddn.com\\\\\\/b9026d86-4e9f-11e8-8bee-525400ae50a0tiny-706-2018-05-03-15-00-53.jpg\\\",\\\"type\\\":\\\"1\\\"}\"]',0,'湖南省湘西州吉首市镇溪街,28.3104360000,109.7436780000',1,0,'2018-05-03 15:00:54','锦鸡舞真的是太壮观啦！','42');
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
  `role` smallint(6) DEFAULT '0',
  `telephone` char(11) DEFAULT NULL,
  `psw` char(40) NOT NULL,
  `image_src` text,
  `name` char(20) DEFAULT NULL,
  `sign` char(50) DEFAULT NULL,
  `acc_point` smallint(6) DEFAULT '0',
  `account_name` char(20) DEFAULT NULL,
  `reg_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1140 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1131,0,'','273841','http://p5o94s90i.bkt.clouddn.com/ebd284d6-4d4f-11e8-8bee-525400ae50a0tiny-573-2018-05-01-22-57-08.jpg','','',116,'yj666','2018-05-01 20:59:14'),(1132,0,'123456789','98','http://p5o94s90i.bkt.clouddn.com/f067cc70-4d42-11e8-8bee-525400ae50a0tiny-424-2018-05-01-21-24-12.jpg','无','爱非遗爱生活！',464,'zw981','2018-05-01 21:06:42'),(1133,1,'15827652010','123','http://p5o94s90i.bkt.clouddn.com/8e630abc-4d42-11e8-8bee-525400ae50a0tiny-24-2018-05-01-21-21-28.jpg','张群','做一个传承文化',141,'123','2018-05-01 21:10:06'),(1134,1,'123456789','office1','http://p5o94s90i.bkt.clouddn.com/93742cb4-4e02-11e8-8bee-525400ae50a0tiny-983-2018-05-02-20-15-59.jpg','','武汉市非物质文化遗产活动负责人',436,'office1','2018-05-02 19:51:32'),(1135,1,'123456789','office2','http://p5o94s90i.bkt.clouddn.com/47cceef8-4e08-11e8-8bee-525400ae50a0tiny-630-2018-05-02-20-56-49.jpg','','湖南省非遗活动发布人',480,'office2','2018-05-02 19:53:19'),(1136,1,'','office3','http://p5o94s90i.bkt.clouddn.com/61eb0b6a-4e0a-11e8-8bee-525400ae50a0tiny-506-2018-05-02-21-11-52.jpg','','安徽省非遗活动发布人',343,'office3','2018-05-02 19:53:44'),(1137,0,'','123','http://p5o94s90i.bkt.clouddn.com/d8e822bc-4e81-11e8-8bee-525400ae50a0tiny-790-2018-05-03-11-27-01.jpg','','非遗爱好者~',0,'汉美人','2018-05-03 11:26:29'),(1138,0,'','98','http://p5o94s90i.bkt.clouddn.com/a88a28fa-4e99-11e8-8bee-525400ae50a0tiny-574-2018-05-03-14-17-28.jpg','','非遗探索者',102,'zw982','2018-05-03 14:17:01'),(1139,0,'123456789','98','http://p5o94s90i.bkt.clouddn.com/e4c63eec-4e9b-11e8-8bee-525400ae50a0tiny-130-2018-05-03-14-33-28.jpg','','非遗传播者就是我~',241,'zw983','2018-05-03 14:32:38');
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

-- Dump completed on 2018-05-03 18:10:50

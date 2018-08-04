create database jingdong charset='utf8';

CREATE TABLE `jingdong` (
  Id int primary key auto_increment,
  `project_id` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `comment_num` varchar(255) DEFAULT NULL,
  `shop_name` varchar(255) DEFAULT NULL,
  `link` varchar(255) DEFAULT NULL,
  `GoodCountStr` varchar(255) DEFAULT NULL,
  `AfterCount` varchar(255) DEFAULT NULL,
  `PoorCount` varchar(255) DEFAULT NULL,
  `price` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `jd_comment`;

CREATE TABLE `jd_comment` (
   Id int primary key auto_increment,
  `user_name` varchar(255) DEFAULT NULL,
  `user_id` varchar(255) DEFAULT NULL,
  `userProvince` varchar(255) DEFAULT NULL,
  `content` longtext,
  `good_id` varchar(255) DEFAULT NULL,
  `good_name` varchar(255) DEFAULT NULL,
  `date` varchar(255) DEFAULT NULL,
  `replyCount` varchar(255) DEFAULT NULL,
  `score` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `userLevelId` varchar(255) DEFAULT NULL,
  `productColor` varchar(255) DEFAULT NULL,
  `productSize` varchar(255) DEFAULT NULL,
  `userLevelName` varchar(255) DEFAULT NULL,
  `userClientShow` varchar(255) DEFAULT NULL,
  `isMobile` varchar(255) DEFAULT NULL,
  `days` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


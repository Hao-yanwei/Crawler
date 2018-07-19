create database example;

#小说详情表,共计19个字段
create table novel(
id bigint NOT NULL AUTO_INCREMENT,
bookname varchar(355) not null,
novel_url varchar(355) not null,
cover_url varchar(355) not null,
author varchar(355) not null,
status varchar(100) not null,
laber text not null,
description text,
PRIMARY KEY ( id )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

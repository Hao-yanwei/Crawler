create database job_items charset='utf8';
create table sina_items(
id bigint not null primary key auto_increment,
job_name varchar(255) not null,
job_link varchar(255) not null,
job_info varchar(255) not null,
company varchar(255) not null,
address varchar(255) not null,
salary varchar(100) not null,
)charset=utf8;
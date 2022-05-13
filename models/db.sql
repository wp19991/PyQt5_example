use mysql;
drop database if exists pyqt5_example_db;

create database if not exists pyqt5_example_db
    default character set utf8mb4
    default collate utf8mb4_unicode_ci;

use pyqt5_example_db;


drop table if exists `t_user`;
create table if not exists `t_user`
(
    `id`               bigint unsigned     not null auto_increment comment '自增id',
    `gmt_created`      datetime            not null default current_timestamp comment '自动生成-创建时间',
    `gmt_modified`     datetime            not null default current_timestamp on update current_timestamp comment '自动生成-修改时间',

    `user_name`        varchar(25)         not null unique comment '用户名(唯一,不为空)',
    `is_valid`         tinyint(1)          not null default 0 comment '用户是否注销(1:是,0:否)',
    `phone_number`     varchar(11) unique comment '手机号(唯一,但是可为空)',
    `email_address`    varchar(50) unique comment '用户邮箱(唯一,但是可为空)',
    `encoded_password` varchar(255)        not null comment '密码',
    `type`             tinyint(3) unsigned not null default 1 comment '用户的类型(1:普通用户 2:管理员)',
    `brief`            varchar(255)        not null default '无' comment '用户简要说明',

    constraint t_user_pk primary key (id)
) engine = InnoDB comment '用户表';
insert into `t_user`(user_name, encoded_password, type)
values ('admin', md5(123456), 2);

insert into `t_user`(user_name, encoded_password, type)
values ('user_1', md5(123456), 1),
       ('user_2', md5(123456), 1);


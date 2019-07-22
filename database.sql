CREATE TABLE IF NOT EXISTS `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(40) NOT NULL COMMENT '用户名',
  `password_hash` VARCHAR(128) NOT NULL COMMENT '密码hash',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '用户信息表';


CREATE TABLE IF NOT EXISTS `user_follow` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_id` INT(11) NOT NULL COMMENT '用户id',
  `follow_user_id` INT(11) NOT NULL COMMENT '关注的用户id',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `follow_unique` (`user_id`,`follow_user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COMMENT '用户关注表';



CREATE TABLE IF NOT EXISTS `user_repo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` INT(11) NOT NULL COMMENT '用户id',
  `repo_name` VARCHAR(40) NOT NULL COMMENT '仓库名',
  `repo_desc` VARCHAR(128) NOT NULL COMMENT '仓库描述',
  `repo_tags` VARCHAR(1024) NOT NULL COMMENT '标签',
  `repo_type` TINYINT NOT NULL COMMENT '仓库类型 0 自己创建的, 1 fork',
  `origin_repo_id` INT COMMENT '源 repo_id',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `repo_unique` (`user_id`,`repo_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '用户仓库表';


CREATE TABLE IF NOT EXISTS `repo_star` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_id` INT(11) NOT NULL COMMENT '用户id',
  `repo_id` INT(11) NOT NULL COMMENT '仓库id',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `star_unique` (`user_id`,`repo_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COMMENT 'repo_star';


CREATE TABLE IF NOT EXISTS `repo_fork` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_id` INT(11) NOT NULL COMMENT '用户id',
  `repo_id` INT(11) NOT NULL COMMENT '仓库id',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `fork_unique` (`user_id`,`repo_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COMMENT 'repo_fork';


CREATE TABLE IF NOT EXISTS `news_event` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_id` INT(11) NOT NULL COMMENT '用户id',
  `event_type` TINYINT NOT NULL COMMENT '消息类型 0 fork_repo, 1 create_repo, 2 star_user, 3 star_repo',
  `event_data` TEXT COMMENT '消息内容具 半结构化json数据',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8
COMMENT '用户活动消息';

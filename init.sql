CREATE TABLE IF NOT EXISTS `assos` (
  `id` varchar(24) NOT NULL COMMENT 'identifier (slug like)',
  `names` text NOT NULL COMMENT 'names separated by comma',
  `logos` text NOT NULL COMMENT 'logos path separated by comma',
  `start` int DEFAULT NULL COMMENT 'creation year',
  `end` int DEFAULT NULL COMMENT 'dissolution year',
  `theme` text NOT NULL COMMENT 'theme',
  `campus` text NOT NULL COMMENT 'campus',
  `room` text DEFAULT NULL COMMENT 'room',
  `socials` text NOT NULL COMMENT 'social networks separated by comma and colon',
  `description` text DEFAULT NULL COMMENT 'description',
  `color` mediumint UNSIGNED NOT NULL COMMENT 'main color',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `events` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'identifier',
  `asso_id` varchar(24) NOT NULL COMMENT 'organizing asso id',
  `title` tinytext NOT NULL COMMENT 'title',
  `poster` tinytext COMMENT 'poster path',
  `description` text COMMENT 'description',
  `date` datetime NOT NULL COMMENT 'datetime',
  `place` tinytext NOT NULL COMMENT 'place',
  `price` tinytext COMMENT 'price',
  `link` tinytext COMMENT 'url',
  `access` tinytext COMMENT 'who can join',
  `status` tinytext NOT NULL DEFAULT ('Programmé') COMMENT 'status',
  `capacity` int DEFAULT NULL COMMENT 'max number of participants',
  `createDate` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'create datetime',
  `lastUpdateDate` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'last update datetime',
  PRIMARY KEY (`id`),
  KEY `event_asso_id` (`asso_id`)
) ENGINE=InnoDB;

ALTER TABLE `events`
  ADD CONSTRAINT `event_asso` FOREIGN KEY (`asso_id`) REFERENCES `assos` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

CREATE TABLE IF NOT EXISTS `sessions` (
  `id` varchar(32) NOT NULL COMMENT 'identifier (hexadecimal)',
  `asso_id` varchar(24) NOT NULL COMMENT 'asso id',
  `createDate` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'creation datetime',
  PRIMARY KEY (`id`),
  KEY `session_asso_id` (`asso_id`)
) ENGINE=InnoDB;

ALTER TABLE `sessions`
  ADD CONSTRAINT `session_asso` FOREIGN KEY (`asso_id`) REFERENCES `assos` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
CREATE TABLE `class` (
  `id` int UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `chat_id` int UNIQUE NOT NULL,
  `admin_id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `lang` varchar(255) NOT NULL,
  `notify` boolean NOT NULL,
  `lesson` int NOT NULL,
  `tomorrow` datetime NOT NULL,
  `timezone` int NOT NULL
);

CREATE TABLE `group` (
  `id` int UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `class_id` int NOT NULL,
  `name` varchar(255) NOT NULL
);

CREATE TABLE `lesson` (
  `id` int UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `start` datetime NOT NULL,
  `length` int NOT NULL,
  `homework` varchar(255),
  `place` varchar(255),
  `weekly` boolean NOT NULL
);

ALTER TABLE `group` ADD FOREIGN KEY (`class_id`) REFERENCES `class` (`id`);

ALTER TABLE `lesson` ADD FOREIGN KEY (`group_id`) REFERENCES `group` (`id`);

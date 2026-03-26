-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: edtech
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `course_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses`
--

LOCK TABLES `courses` WRITE;
/*!40000 ALTER TABLE `courses` DISABLE KEYS */;
INSERT INTO `courses` VALUES (1,'Python Programming'),(2,'MySQL Database'),(3,'JavaScript Basics'),(4,'Data Science');
/*!40000 ALTER TABLE `courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `enrollments`
--

DROP TABLE IF EXISTS `enrollments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `enrollments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_name` varchar(100) DEFAULT NULL,
  `course_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enrollments`
--

LOCK TABLES `enrollments` WRITE;
/*!40000 ALTER TABLE `enrollments` DISABLE KEYS */;
INSERT INTO `enrollments` VALUES (1,'aradhya','Python Programming'),(2,'aradhya','MySQL Database'),(3,'aradhya','JavaScript Basics'),(4,'aradhya','JavaScript Basics'),(5,'Priyam','Python Programming'),(6,'Priyam','Data Science'),(7,'aradhya','Data Science');
/*!40000 ALTER TABLE `enrollments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lessons`
--

DROP TABLE IF EXISTS `lessons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lessons` (
  `id` int NOT NULL AUTO_INCREMENT,
  `course_id` int DEFAULT NULL,
  `lesson_title` varchar(200) DEFAULT NULL,
  `video_url` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lessons`
--

LOCK TABLES `lessons` WRITE;
/*!40000 ALTER TABLE `lessons` DISABLE KEYS */;
INSERT INTO `lessons` VALUES (1,1,'Python Introduction','https://www.youtube.com/embed/rfscVS0vtbw'),(2,1,'Variables','https://www.youtube.com/embed/kqtD5dpn9C8'),(3,1,'Loops','https://www.youtube.com/embed/6iF8Xb7Z3wQ'),(4,2,'MySQL Basics','https://www.youtube.com/embed/7S_tz1z_5bA'),(5,2,'Creating Tables','https://www.youtube.com/embed/9ylj9NR0Lcg'),(6,2,'MySQL Introduction','https://www.youtube.com/embed/7S_tz1z_5bA'),(7,3,'JavaScript Introduction','https://www.youtube.com/embed/W6NZfCO5SIk'),(8,3,'Functions','https://www.youtube.com/embed/N8ap4k_1QEQ'),(9,3,'JavaScript Variables','https://www.youtube.com/embed/Bv_5Zv5c-Ts'),(10,4,'Introduction to Data Science','https://www.youtube.com/embed/X3paOmcrTjQ');
/*!40000 ALTER TABLE `lessons` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `progress`
--

DROP TABLE IF EXISTS `progress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `progress` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_name` varchar(100) DEFAULT NULL,
  `lesson_id` int DEFAULT NULL,
  `completed` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `progress`
--

LOCK TABLES `progress` WRITE;
/*!40000 ALTER TABLE `progress` DISABLE KEYS */;
INSERT INTO `progress` VALUES (1,'Priyam',1,0),(2,'Priyam',2,0),(3,'Priyam',1,1),(4,'Priyam',3,1),(5,'aradhya',9,1),(6,'aradhya',6,1),(7,'aradhya',4,1),(8,'Priyam',2,1),(9,'Priyam',3,1),(10,'Priyam',1,1),(11,'aradhya',5,1),(12,'aradhya',10,1),(13,'aradhya',3,1),(14,'aradhya',1,1);
/*!40000 ALTER TABLE `progress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(120) DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL,
  `role` varchar(20) DEFAULT 'student',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (4,'Abha','abha@gmail.com','scrypt:32768:8:1$EGqTOHxtez8RErPr$46b226f834997d95724e13194c2b8947783e5f5bf8f74e0cc65e04a6af19dd095935a86aa71d2b17c0dc649e4d2c5bfec94af89dff197fe937348e55de3da8b0','student'),(5,'suneeta','suneeta@gmail.com','scrypt:32768:8:1$6n5PR2GiWM1TTJGM$95ffb731dfeb2eb20924bc94ac4274ed4d2324c11401b9f935dcf287a009940ca21ccea64a1d4b51ac253df8aac033c60cc4452b59b882b081cd80e46ea60077','student'),(6,'Ridhima','ridhima@gmail.com','scrypt:32768:8:1$BUJmYFFa6Yo5h5sy$9a5f26f8a9d8b1674420b72b5239150b7b089e2113f4b357cd4b5a05865381792e9cf046c9f36c05b025999d82e295df9515e1e7a739a29677922cacf4a96582','student'),(7,'aradhya','aru@gmail.com','scrypt:32768:8:1$8Un8Q9NuTCDfcsT5$6f9bcb4fd7927940c27cc02cf455f1447a47f970b1d6a92998afe97368f7eb450e9a5823db81f40a7be54cf62146f09625712087111b2c572c4ce3413509bf2e','student'),(10,'Priyam','pri@gmail.com','scrypt:32768:8:1$S31FhdCEDl7kDnpP$ed2f11c994ac8d9901a3b5cfb3eabda33a2c7069ab9762bc313305fdd9618dcdaf5adeccea6d2673d9d6f2e76f375461bb4286f87c2a3e6b2580776af4f13247','student'),(11,'suneeta','suneeta01@gmail.com','scrypt:32768:8:1$brNt7x85CRJMO9kD$f8deb610ceefb01def4cd0ad7699a2629b04b895388c29b6b57dbba19132b449bb6cc342c40ae8bedfdedabb8a1534ad102a0a368bfc1a93ac4034f049b3eb1f','admin');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-26 13:03:58

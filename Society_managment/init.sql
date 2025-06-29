-- MySQL dump 10.13  Distrib 9.2.0, for Linux (x86_64)
--
-- Host: localhost    Database: Society_managment
-- ------------------------------------------------------
-- Server version	9.2.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `buildings`
--

DROP TABLE IF EXISTS `buildings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `buildings` (
  `building_no` int NOT NULL AUTO_INCREMENT,
  `building_name` varchar(100) NOT NULL,
  `floors` int NOT NULL,
  `flats_per_floor` int NOT NULL,
  PRIMARY KEY (`building_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `buildings`
--

LOCK TABLES `buildings` WRITE;
/*!40000 ALTER TABLE `buildings` DISABLE KEYS */;
/*!40000 ALTER TABLE `buildings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flat_type_mappings`
--

DROP TABLE IF EXISTS `flat_type_mappings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flat_type_mappings` (
  `building_no` int NOT NULL,
  `flat_no` varchar(10) NOT NULL,
  `flat_type` varchar(20) NOT NULL,
  PRIMARY KEY (`building_no`,`flat_no`),
  KEY `flat_type` (`flat_type`),
  CONSTRAINT `flat_type_mappings_ibfk_1` FOREIGN KEY (`building_no`) REFERENCES `buildings` (`building_no`) ON DELETE CASCADE,
  CONSTRAINT `flat_type_mappings_ibfk_2` FOREIGN KEY (`flat_type`) REFERENCES `flat_types` (`type_name`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flat_type_mappings`
--

LOCK TABLES `flat_type_mappings` WRITE;
/*!40000 ALTER TABLE `flat_type_mappings` DISABLE KEYS */;
/*!40000 ALTER TABLE `flat_type_mappings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flat_types`
--

DROP TABLE IF EXISTS `flat_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flat_types` (
  `type_name` varchar(20) NOT NULL,
  `maintenance_fee` int NOT NULL,
  `rent` int DEFAULT NULL,
  PRIMARY KEY (`type_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flat_types`
--

LOCK TABLES `flat_types` WRITE;
/*!40000 ALTER TABLE `flat_types` DISABLE KEYS */;
/*!40000 ALTER TABLE `flat_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flats`
--

DROP TABLE IF EXISTS `flats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flats` (
  `building_no` int NOT NULL,
  `flat_no` varchar(10) NOT NULL,
  `flat_type` varchar(20) DEFAULT NULL,
  `status` enum('empty','owned','rented') DEFAULT 'empty',
  `start_date` date DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  `due_amt` int DEFAULT NULL,
  `fine` int DEFAULT '0',
  `miscellaneous` int DEFAULT '0',
  `maintenance_fee` int DEFAULT NULL,
  `total_due` int DEFAULT NULL,
  PRIMARY KEY (`building_no`,`flat_no`),
  KEY `fk_flat_type` (`flat_type`),
  CONSTRAINT `fk_flat_building` FOREIGN KEY (`building_no`) REFERENCES `buildings` (`building_no`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_flat_type` FOREIGN KEY (`flat_type`) REFERENCES `flat_types` (`type_name`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flats`
--

LOCK TABLES `flats` WRITE;
/*!40000 ALTER TABLE `flats` DISABLE KEYS */;
/*!40000 ALTER TABLE `flats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password_hash` text,
  `oauth_provider` varchar(50) DEFAULT NULL,
  `oauth_id` varchar(100) DEFAULT NULL,
  `role` enum('admin','owner','renter') DEFAULT 'renter',
  `flat_building_no` int DEFAULT NULL,
  `flat_no` varchar(10) DEFAULT NULL,
  `building_no` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `fk_user_flat` (`flat_building_no`,`flat_no`),
  CONSTRAINT `fk_user_flat` FOREIGN KEY (`flat_building_no`, `flat_no`) REFERENCES `flats` (`building_no`, `flat_no`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'danyalahmad190405@gmail.com','danyal','$2b$12$jWbEQTTEvQtTU796DMv5Rue14trsAJqbKTRA2ZxrCJBjA/yZj5YMq',NULL,NULL,'admin',NULL,NULL,NULL);
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

-- Dump completed on 2025-06-28 14:50:51

-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: assignment4
-- ------------------------------------------------------
-- Server version	8.0.35

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
-- Table structure for table `exercise`
--

DROP TABLE IF EXISTS `exercise`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exercise` (
  `exerciseName` varchar(255) NOT NULL,
  `exerciseDescription` varchar(255) DEFAULT NULL,
  `duration` float DEFAULT NULL,
  `burnedCalories` float DEFAULT NULL,
  `targetMuscle` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`exerciseName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exercise`
--

LOCK TABLES `exercise` WRITE;
/*!40000 ALTER TABLE `exercise` DISABLE KEYS */;
INSERT INTO `exercise` VALUES ('Bench Press','Upper body exercise',8,40,'Chest'),('Bicep Curl','Arm exercise',5,15,'Biceps'),('Box Jumps','Lower body exercise',5,25,'Legs'),('Burpees','Full-body exercise',7,40,'Full Body'),('Calf Raises','Lower body exercise',5,20,'Calves'),('Crunches','Core exercise',4,20,'Abdominals'),('Cycling','Cardiovascular exercise',45,300,'Legs'),('Deadlift','Full-body exercise',10,50,'Back'),('Dumbbell Row','Upper body exercise',6,25,'Back'),('Hanging Leg Raise','Core exercise',4,18,'Abdominals'),('Jumping Jacks','Cardiovascular exercise',5,30,'Full Body'),('Leg Press','Lower body exercise',8,30,'Legs'),('Lunges','Lower body exercise',6,30,'Legs'),('Mountain Climbers','Cardio and Core exercise',5,25,'Full Body'),('Plank','Core exercise',3,15,'Abdominals'),('Pullup','Upper body exercise',4,18,'Back'),('Pushup','Upper body exercise',5,20,'Chest'),('Running','Cardiovascular exercise',30,200,'Legs'),('Russian Twist','Core exercise',4,20,'Obliques'),('Shoulder Press','Upper body exercise',8,35,'Shoulders'),('Squat','Lower body exercise',6,25,'Legs'),('Swimming','Full-body exercise',45,400,'Full Body'),('Tricep Dip','Arm exercise',4,18,'Triceps'),('Yoga','Flexibility and relaxation',60,150,'Full Body');
/*!40000 ALTER TABLE `exercise` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-06 15:19:47

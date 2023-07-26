--
-- Current Database: `rosguard1`
--

/*!40000 DROP DATABASE IF EXISTS `%s` */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/ `rosguard1` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `rosguard1`;

-- MySQL dump 10.13  Distrib 5.6.22, for Win32 (x86)
--
-- Host: localhost    Database: rosguard1
-- ------------------------------------------------------
-- Server version	5.6.15

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `call log`
--

DROP TABLE IF EXISTS `call log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `call log` (
  `Id_vizova` tinyint(4) NOT NULL,
  `Id_ekipaja` smallint(6) DEFAULT NULL,
  `Data` varchar(19) DEFAULT NULL,
  `Time` varchar(19) DEFAULT NULL,
  `Adress_vizova` varchar(12) DEFAULT NULL,
  PRIMARY KEY (`Id_vizova`),
  KEY `Id_ekipaja` (`Id_ekipaja`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `call log`
--

LOCK TABLES `call log` WRITE;
/*!40000 ALTER TABLE `call log` DISABLE KEYS */;
INSERT  IGNORE INTO `call log` VALUES (1,333,'2021-10-11 00:00:00','1899-12-30 08:00:00','ГРЭС'),(2,111,'2021-10-02 00:00:00','1899-12-30 16:00:00','Толстого 10'),(3,333,'2021-10-05 00:00:00','1899-12-30 11:00:00','5 микрорайон'),(4,222,'2021-10-01 00:00:00','1899-12-30 04:00:00','ГРЭС'),(5,555,'2021-10-19 00:00:00','1899-12-30 19:00:00','Пионерская 8'),(6,444,'2021-10-09 00:00:00','1899-12-30 18:00:00','Малышева 14'),(7,222,'2021-10-07 00:00:00','1899-12-30 10:30:00','Толстого 10'),(8,444,'2021-10-16 00:00:00','1899-12-30 23:00:00','Сибирская 21'),(9,555,'2021-10-04 00:00:00','1899-12-30 18:00:00','ГРЭС'),(10,222,'2021-10-03 00:00:00','1899-12-30 21:30:00','Толстого 10');
/*!40000 ALTER TABLE `call log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ekipaj`
--

DROP TABLE IF EXISTS `ekipaj`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ekipaj` (
  `Id_ekipaja` smallint(6) DEFAULT NULL,
  `Id_sotrudnika` tinyint(4) DEFAULT NULL,
  KEY `Id_sotrudnika` (`Id_sotrudnika`),
  KEY `Id_ekipaja` (`Id_ekipaja`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ekipaj`
--

LOCK TABLES `ekipaj` WRITE;
/*!40000 ALTER TABLE `ekipaj` DISABLE KEYS */;
INSERT  IGNORE INTO `ekipaj` VALUES (111,1),(222,2),(333,3),(444,4),(555,5),(111,6),(222,7),(333,8),(444,9),(555,10),(111,11),(222,12),(333,13),(444,14),(555,15);
/*!40000 ALTER TABLE `ekipaj` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nazvanie_ekipaja`
--

DROP TABLE IF EXISTS `nazvanie_ekipaja`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nazvanie_ekipaja` (
  `Id_ekipaja` smallint(6) DEFAULT NULL,
  `Name` varchar(8) DEFAULT NULL,
  KEY `Id_ekipaja` (`Id_ekipaja`),
  CONSTRAINT `nazvanie_ekipaja_fk2` FOREIGN KEY (`Id_ekipaja`) REFERENCES `call log` (`Id_ekipaja`),
  CONSTRAINT `nazvanie_ekipaja_fk1` FOREIGN KEY (`Id_ekipaja`) REFERENCES `ekipaj` (`Id_ekipaja`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nazvanie_ekipaja`
--

LOCK TABLES `nazvanie_ekipaja` WRITE;
/*!40000 ALTER TABLE `nazvanie_ekipaja` DISABLE KEYS */;
INSERT  IGNORE INTO `nazvanie_ekipaja` VALUES (111,'Дракон'),(222,'Тигрище'),(333,'Леопард'),(444,'Медведь'),(555,'Динозавр');
/*!40000 ALTER TABLE `nazvanie_ekipaja` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sotrudniki`
--

DROP TABLE IF EXISTS `sotrudniki`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sotrudniki` (
  `Id_sotrudnika` tinyint(4) NOT NULL,
  `F_I_O` varchar(33) DEFAULT NULL,
  `Mobil_telephone` bigint(20) DEFAULT NULL,
  `Adress` varchar(11) DEFAULT NULL,
  `Zvanie` varchar(17) DEFAULT NULL,
  PRIMARY KEY (`Id_sotrudnika`),
  CONSTRAINT `sotrudniki_fk1` FOREIGN KEY (`Id_sotrudnika`) REFERENCES `ekipaj` (`Id_sotrudnika`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sotrudniki`
--

LOCK TABLES `sotrudniki` WRITE;
/*!40000 ALTER TABLE `sotrudniki` DISABLE KEYS */;
INSERT  IGNORE INTO `sotrudniki` VALUES (1,'Деренченко Евгений Николаевич',89080559614,'Гагарина 1','Майор'),(2,'Шеметов Даниил Александрович',89000930983,'Гагарина 2','Старший лейтенант'),(3,'Хомутков Алексей Сергеевич',89080524230,'Гагарина 3','Подполковник'),(4,'Шеметов Антон Александрович',85467854567,'Гагарина 4','Старший прапорщик'),(5,'Тарасюк Данил Николаевич',85613561351,'Гагарина 5','Генерал Майор'),(6,'Карнаухов Владислав Александрович',82358617864,'Гагарина 6','Капитан'),(7,'Черкозьянов Аркадий Борисович',89562154561,'Гагарина 7','Генерал майор'),(8,'Шеметов Андрей Викторович',89256471398,'Гагарина 8','Генерал лейтенант'),(9,'Локтионов Сергей Михайлович',89526157432,'Гагарина 9','Лейтенант'),(10,'Валеев Хамид Мидхатович',81234569875,'Гагарина 10','Генерал полковник'),(11,'Бахарев Валерий Петрович',89632587412,'Гагарина 11','Генерал лейтенант'),(12,'Исхаков Рамиль Кираматович',82591569732,'Гагарина 12','Капитан'),(13,'Шеметов Сергей Дмитриевич',87785461355,'Гагарина 13','Подполковник'),(14,'Дубовик Владимир Михайлович',89637414562,'Гагарина 14','Генерал полковник'),(15,'Затеев Виктор Михайлович',81569924736,'Гагарина 15','Майор');
/*!40000 ALTER TABLE `sotrudniki` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'rosguard1'
--

--
-- Dumping routines for database 'rosguard1'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-10-13 12:53:23

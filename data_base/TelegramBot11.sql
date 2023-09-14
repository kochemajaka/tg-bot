-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: telegrambot
-- ------------------------------------------------------
-- Server version	8.0.19

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
-- Table structure for table `cars`
--

DROP TABLE IF EXISTS `cars`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cars` (
  `idCars` int NOT NULL,
  `ModelMarka` int NOT NULL,
  `ProbegNumber` int NOT NULL,
  `YearCar` int NOT NULL,
  `Title` int NOT NULL,
  PRIMARY KEY (`idCars`,`ModelMarka`,`ProbegNumber`,`YearCar`,`Title`),
  KEY `fk_Cars_Probeg_idx` (`ProbegNumber`),
  KEY `fk_Cars_Year1_idx` (`YearCar`),
  KEY `fk_Cars_Title1_idx` (`Title`),
  KEY `fk_Cars_Model_Marka1_idx` (`ModelMarka`),
  CONSTRAINT `fk_Cars_Model_Marka1` FOREIGN KEY (`ModelMarka`) REFERENCES `model_marka` (`idModel_Marka`),
  CONSTRAINT `fk_Cars_Probeg` FOREIGN KEY (`ProbegNumber`) REFERENCES `probeg` (`idProbeg`),
  CONSTRAINT `fk_Cars_Title1` FOREIGN KEY (`Title`) REFERENCES `title` (`idTitle`),
  CONSTRAINT `fk_Cars_Year1` FOREIGN KEY (`YearCar`) REFERENCES `year` (`idYear`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cars`
--

LOCK TABLES `cars` WRITE;
/*!40000 ALTER TABLE `cars` DISABLE KEYS */;
INSERT INTO `cars` VALUES (1,1,1,1,1);
/*!40000 ALTER TABLE `cars` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `model_marka`
--

DROP TABLE IF EXISTS `model_marka`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `model_marka` (
  `idModel_Marka` int NOT NULL,
  `ModelName` varchar(45) NOT NULL,
  `MarkaName` varchar(45) NOT NULL,
  PRIMARY KEY (`idModel_Marka`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `model_marka`
--

LOCK TABLES `model_marka` WRITE;
/*!40000 ALTER TABLE `model_marka` DISABLE KEYS */;
INSERT INTO `model_marka` VALUES (1,'Renault','Duster'),(2,'Lada','Kalina Cross'),(3,'Skoda','Octavia');
/*!40000 ALTER TABLE `model_marka` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `probeg`
--

DROP TABLE IF EXISTS `probeg`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `probeg` (
  `idProbeg` int NOT NULL,
  `Number` varchar(45) NOT NULL,
  PRIMARY KEY (`idProbeg`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `probeg`
--

LOCK TABLES `probeg` WRITE;
/*!40000 ALTER TABLE `probeg` DISABLE KEYS */;
INSERT INTO `probeg` VALUES (1,'57000'),(2,'66919'),(3,'82982');
/*!40000 ALTER TABLE `probeg` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `title`
--

DROP TABLE IF EXISTS `title`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `title` (
  `idTitle` int NOT NULL,
  `Text` varchar(5000) NOT NULL,
  PRIMARY KEY (`idTitle`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `title`
--

LOCK TABLES `title` WRITE;
/*!40000 ALTER TABLE `title` DISABLE KEYS */;
INSERT INTO `title` VALUES (1,'* Объем двигателя: 2.0 * Мощность (ЛС): 143 * Коробка передач: МКПП * Привод: Полный * Владельцев по ПТС: 1 * Цена в объявлении: 1350000 ₽ * Город клиента: Санкт-Петербург *Город поиска: Санкт-Петербург * Цена относительно рынка: средняя * Преимущества этого автомобиля: -Один подкрас, -отличное состояние кузова, -небольшой пробег, -по технике без особых нареканий.'),(2,'Объем двигателя: 1.6 * Мощность: 106 л.с. * Коробка передач: робот * Привод: передний * Владельцев по ПТС: 2 * Цена покупки: 580 000 * Цена относительно рынка: средняя * Преимущества этого авто: -родной окрас, -максимальная комплектация, -полностью дилерское обслуживание, -хорошее состояние.'),(3,'Объём двигателя: 1.4 (150 л.с.) * Коробка передач: mt * Владельцев по ПТС: 2 * Цена: 1\'545\'000₽ * Город: Санкт-Петербург Продавец по телефону очень хвалил автомобиль и заявлял, что в таком состоянии их не найти. Осмотр проводился для клиента из Иваново в его присутствии. Сразу надо сказать что кузов находился под толстым слоем высохшей грязи, но все равно были найдены некоторые замечания, о которых не было сказано. Притир по левой стороне на стыке переднего крыла и бампера, пара сколов на капоте и пара \"тычков\" на заднем бампере. Заявлялось о замене тормозных дисков, но на них отчетливо видна выработка почти в миллиметр, колодки еще в норме. Салон действительно, не имел повреждений и царапин. Но уличной грязи там килограммы.Pленная летняя резина вторым комплектом уже давно износилась, и не имела ценности. По итогу мы видим авто в заводским окрасе с незначительными нареканиями, салон под глубокую химчистку и технически без срочных вложений.');
/*!40000 ALTER TABLE `title` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vin`
--

DROP TABLE IF EXISTS `vin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vin` (
  `idVIN` int NOT NULL,
  `VINNumber` varchar(45) NOT NULL,
  PRIMARY KEY (`idVIN`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vin`
--

LOCK TABLES `vin` WRITE;
/*!40000 ALTER TABLE `vin` DISABLE KEYS */;
INSERT INTO `vin` VALUES (1,'1D3HE28K27S'),(2,'1J3HE42K17R'),(3,'TY3HE52P879');
/*!40000 ALTER TABLE `vin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `year`
--

DROP TABLE IF EXISTS `year`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `year` (
  `idYear` int NOT NULL,
  `Year` varchar(45) NOT NULL,
  PRIMARY KEY (`idYear`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `year`
--

LOCK TABLES `year` WRITE;
/*!40000 ALTER TABLE `year` DISABLE KEYS */;
INSERT INTO `year` VALUES (1,'2017'),(2,'2016'),(3,'2017');
/*!40000 ALTER TABLE `year` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-04-20  0:13:33

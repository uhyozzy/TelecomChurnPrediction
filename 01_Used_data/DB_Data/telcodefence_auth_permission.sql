-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: telcodefence
-- ------------------------------------------------------
-- Server version	8.0.34

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
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb3_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb3_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=93 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add 계약 종류',7,'add_tbcontractcontract'),(26,'Can change 계약 종류',7,'change_tbcontractcontract'),(27,'Can delete 계약 종류',7,'delete_tbcontractcontract'),(28,'Can view 계약 종류',7,'view_tbcontractcontract'),(29,'Can add 요금제 수정 로그',8,'add_tbcontractlog'),(30,'Can change 요금제 수정 로그',8,'change_tbcontractlog'),(31,'Can delete 요금제 수정 로그',8,'delete_tbcontractlog'),(32,'Can view 요금제 수정 로그',8,'view_tbcontractlog'),(33,'Can add 기본 요금대',9,'add_tbcontractmonthc'),(34,'Can change 기본 요금대',9,'change_tbcontractmonthc'),(35,'Can delete 기본 요금대',9,'delete_tbcontractmonthc'),(36,'Can view 기본 요금대',9,'view_tbcontractmonthc'),(37,'Can add 계약 기간대',10,'add_tbcontracttim'),(38,'Can change 계약 기간대',10,'change_tbcontracttim'),(39,'Can delete 계약 기간대',10,'delete_tbcontracttim'),(40,'Can view 계약 기간대',10,'view_tbcontracttim'),(41,'Can add 결합 상품 수',11,'add_tbservicecp'),(42,'Can change 결합 상품 수',11,'change_tbservicecp'),(43,'Can delete 결합 상품 수',11,'delete_tbservicecp'),(44,'Can view 결합 상품 수',11,'view_tbservicecp'),(45,'Can add 서비스 수정 로그',12,'add_tbservicelog'),(46,'Can change 서비스 수정 로그',12,'change_tbservicelog'),(47,'Can delete 서비스 수정 로그',12,'delete_tbservicelog'),(48,'Can view 서비스 수정 로그',12,'view_tbservicelog'),(49,'Can add 가족 결합 수',13,'add_tbservicenod'),(50,'Can change 가족 결합 수',13,'change_tbservicenod'),(51,'Can delete 가족 결합 수',13,'delete_tbservicenod'),(52,'Can view 가족 결합 수',13,'view_tbservicenod'),(53,'Can add 부가 서비스 수',14,'add_tbservicests'),(54,'Can change 부가 서비스 수',14,'change_tbservicests'),(55,'Can delete 부가 서비스 수',14,'delete_tbservicests'),(56,'Can view 부가 서비스 수',14,'view_tbservicests'),(57,'Can add 기술 서비스 수',15,'add_tbservicets'),(58,'Can change 기술 서비스 수',15,'change_tbservicets'),(59,'Can delete 기술 서비스 수',15,'delete_tbservicets'),(60,'Can view 기술 서비스 수',15,'view_tbservicets'),(61,'Can add 유저 테이블',16,'add_tbuser'),(62,'Can change 유저 테이블',16,'change_tbuser'),(63,'Can delete 유저 테이블',16,'delete_tbuser'),(64,'Can view 유저 테이블',16,'view_tbuser'),(65,'Can add 나이대',17,'add_tbuseragerange'),(66,'Can change 나이대',17,'change_tbuseragerange'),(67,'Can delete 나이대',17,'delete_tbuseragerange'),(68,'Can view 나이대',17,'view_tbuseragerange'),(69,'Can add 해지 카테고리',18,'add_tbusercv'),(70,'Can change 해지 카테고리',18,'change_tbusercv'),(71,'Can delete 해지 카테고리',18,'delete_tbusercv'),(72,'Can view 해지 카테고리',18,'view_tbusercv'),(73,'Can add 유저 수정 로그',19,'add_tbuserlog'),(74,'Can change 유저 수정 로그',19,'change_tbuserlog'),(75,'Can delete 유저 수정 로그',19,'delete_tbuserlog'),(76,'Can view 유저 수정 로그',19,'view_tbuserlog'),(77,'Can add 관리 점수',20,'add_tbuserss'),(78,'Can change 관리 점수',20,'change_tbuserss'),(79,'Can delete 관리 점수',20,'delete_tbuserss'),(80,'Can view 관리 점수',20,'view_tbuserss'),(81,'Can add 요금제 정보',21,'add_tbcontract'),(82,'Can change 요금제 정보',21,'change_tbcontract'),(83,'Can delete 요금제 정보',21,'delete_tbcontract'),(84,'Can view 요금제 정보',21,'view_tbcontract'),(85,'Can add 서비스 정보',22,'add_tbservice'),(86,'Can change 서비스 정보',22,'change_tbservice'),(87,'Can delete 서비스 정보',22,'delete_tbservice'),(88,'Can view 서비스 정보',22,'view_tbservice'),(89,'Can add 고객 점수',23,'add_tbusercltv'),(90,'Can change 고객 점수',23,'change_tbusercltv'),(91,'Can delete 고객 점수',23,'delete_tbusercltv'),(92,'Can view 고객 점수',23,'view_tbusercltv');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-10-25 17:43:05

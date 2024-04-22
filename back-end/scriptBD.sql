-- MariaDB dump 10.19  Distrib 10.6.16-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: H2024
-- ------------------------------------------------------
-- Server version	10.6.16-MariaDB-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('f993472800eb');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `city`
--

DROP TABLE IF EXISTS `city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `city` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `city` varchar(100) NOT NULL,
  `idRegion` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_city_idRegion` (`idRegion`)
) ENGINE=InnoDB AUTO_INCREMENT=1254 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `city`
--

LOCK TABLES `city` WRITE;
/*!40000 ALTER TABLE `city` DISABLE KEYS */;
INSERT INTO `city` VALUES (1,'Abercorn',16),(2,'Acton Vale',16),(3,'Adstock',12),(4,'Aguanish',9),(5,'Akulivik',10),(6,'Akwesasne',16),(7,'Albanel',2),(8,'Albertville',1),(9,'Alleyn-et-Cawood',7),(10,'Alma',2),(11,'Amherst',15),(12,'Amos',8),(13,'Amqui',1),(14,'Ange-Gardien',16),(15,'Armagh',12),(16,'Arundel',15),(17,'Ascot Corner',5),(18,'Aston-Jonction',17),(19,'Auclair',1),(20,'Audet',5),(21,'Aumond',7),(22,'Aupaluk',10),(23,'Austin',5),(24,'Authier',8),(25,'Authier-Nord',8),(26,'Ayer\'s Cliff',5),(27,'Baie-Atibenne',14),(28,'Baie-Comeau',9),(29,'Baie-de-la-Bouteille',14),(30,'Baie-des-Chaloupes',15),(31,'Baie-des-Sables',1),(32,'Baie-d\'Hudson',10),(33,'Baie-du-Febvre',17),(34,'Baie-D\'Urfé',6),(35,'Baie-Johan-Beetz',9),(36,'Baie-Obaoca',14),(37,'Baie-Sainte-Catherine',3),(38,'Baie-Saint-Paul',3),(39,'Baie-Trinité',9),(40,'Barkmere',15),(41,'Barnston-Ouest',5),(42,'Barraute',8),(43,'Batiscan',4),(44,'Beaconsfield',6),(45,'Béarn',8),(46,'Beauceville',12),(47,'Beauharnois',16),(48,'Beaulac-Garthby',12),(49,'Beaumont',12),(50,'Beaupré',3),(51,'Bécancour',17),(52,'Bedford',16),(53,'Bégin',2),(54,'Belcourt',8),(55,'Belle-Rivière',2),(56,'Belleterre',8),(57,'Belœil',16),(58,'Berry',8),(59,'Berthier-sur-Mer',12),(60,'Berthierville',14),(61,'Béthanie',16),(62,'Biencourt',1),(63,'Blainville',15),(64,'Blanc-Sablon',9),(65,'Blue Sea',7),(66,'Boileau',7),(67,'Boisbriand',15),(68,'Boischatel',3),(69,'Bois-des-Filion',15),(70,'Bois-Franc',7),(71,'Bolton-Est',5),(72,'Bolton-Ouest',16),(73,'Bonaventure',11),(74,'Bonne-Espérance',9),(75,'Bonsecours',5),(76,'Boucherville',16),(77,'Bouchette',7),(78,'Bowman',7),(79,'Brébeuf',15),(80,'Brigham',16),(81,'Bristol',7),(82,'Brome',16),(83,'Bromont',16),(84,'Brossard',16),(85,'Brownsburg-Chatham',15),(86,'Bryson',7),(87,'Bury',5),(88,'Cacouna',1),(89,'Calixa-Lavallée',16),(90,'Campbell\'s Bay',7),(91,'Candiac',16),(92,'Caniapiscau',9),(93,'Cantley',7),(94,'Cap-Chat',11),(95,'Caplan',11),(96,'Cap-Saint-Ignace',12),(97,'Cap-Santé',3),(98,'Carignan',16),(99,'Carleton-sur-Mer',11),(100,'Cascades-Malignes',7),(101,'Cascapédia–Saint-Jules',11),(102,'Causapscal',1),(103,'Cayamant',7),(104,'Chambly',16),(105,'Chambord',2),(106,'Champlain',4),(107,'Champneuf',8),(108,'Chandler',11),(109,'Chapais',10),(110,'Charette',4),(111,'Charlemagne',14),(112,'Chartierville',5),(113,'Châteauguay',16),(114,'Château-Richer',3),(115,'Chazel',8),(116,'Chelsea',7),(117,'Chénéville',7),(118,'Chertsey',14),(119,'Chesterville',17),(120,'Chibougamau',10),(121,'Chichester',7),(122,'Chisasibi',10),(123,'Chute-aux-Outardes',9),(124,'Chute-Saint-Philippe',15),(125,'Clarendon',7),(126,'Clermont',8),(127,'Clermont',3),(128,'Clerval',8),(129,'Cleveland',5),(130,'Cloridorme',11),(131,'Coaticook',5),(132,'Collines-du-Basque',11),(133,'Colombier',9),(134,'Compton',5),(135,'Contrecœur',16),(136,'Cookshire-Eaton',5),(137,'Coteau-du-Lac',16),(138,'Côte-Nord-du-Golfe-du-Saint-Laurent',9),(139,'Côte-Saint-Luc',6),(140,'Coucoucache',4),(141,'Coulée-des-Adolphe',11),(142,'Courcelles',5),(143,'Cowansville',16),(144,'Crabtree',14),(145,'Danville',5),(146,'Daveluyville',17),(147,'Dégelis',1),(148,'Déléage',7),(149,'Delson',16),(150,'Denholm',7),(151,'Dépôt-Échouani',7),(152,'Desbiens',2),(153,'Deschaillons-sur-Saint-Laurent',17),(154,'Deschambault-Grondines',3),(155,'Deux-Montagnes',15),(156,'Disraeli',12),(157,'Dixville',5),(158,'Dolbeau-Mistassini',2),(159,'Dollard-Des Ormeaux',6),(160,'Doncaster',15),(161,'Donnacona',3),(162,'Dorval',6),(163,'Dosquet',12),(164,'Drummondville',17),(165,'Dudswell',5),(166,'Duhamel',7),(167,'Duhamel-Ouest',8),(168,'Dundee',16),(169,'Dunham',16),(170,'Duparquet',8),(171,'Dupuy',8),(172,'Durham-Sud',17),(173,'East Angus',5),(174,'East Broughton',12),(175,'East Farnham',16),(176,'East Hereford',5),(177,'Eastmain',10),(178,'Eastman',5),(179,'Eeyou Istchee Baie-James',10),(180,'Egan-Sud',7),(181,'Elgin',16),(182,'Entrelacs',14),(183,'Escuminac',11),(184,'Esprit-Saint',1),(185,'Essipit',9),(186,'Estérel',15),(187,'Farnham',16),(188,'Fassett',7),(189,'Ferland-et-Boilleau',2),(190,'Ferme-Neuve',15),(191,'Fermont',9),(192,'Forestville',9),(193,'Fort-Coulonge',7),(194,'Fortierville',17),(195,'Fossambault-sur-le-Lac',3),(196,'Frampton',12),(197,'Franklin',16),(198,'Franquelin',9),(199,'Frelighsburg',16),(200,'Frontenac',5),(201,'Fugèreville',8),(202,'Gallichan',8),(203,'Gaspé',11),(204,'Gatineau',7),(205,'Gesgapegiag',11),(206,'Girardville',2),(207,'Godbout',9),(208,'Godmanchester',16),(209,'Gore',15),(210,'Gracefield',7),(211,'Granby',16),(212,'Grande-Rivière',11),(213,'Grandes-Piles',4),(214,'Grande-Vallée',11),(215,'Grand-Métis',1),(216,'Grand-Remous',7),(217,'Grand-Saint-Esprit',17),(218,'Grenville',15),(219,'Grenville-sur-la-Rouge',15),(220,'Gros-Mécatina',9),(221,'Grosse-Île',11),(222,'Grosses-Roches',1),(223,'Guérin',8),(224,'Ham-Nord',17),(225,'Hampden',5),(226,'Hampstead',6),(227,'Ham-Sud',5),(228,'Harrington',15),(229,'Hatley',5),(230,'Havelock',16),(231,'Havre-Saint-Pierre',9),(232,'Hébertville',2),(233,'Hébertville-Station',2),(234,'Hemmingford',16),(235,'Henryville',16),(236,'Hérouxville',4),(237,'Hinchiidooke',16),(238,'Honfleur',12),(239,'Hope',11),(240,'Hope Town',11),(241,'Howick',16),(242,'Huberdeau',15),(243,'Hudson',16),(244,'Hunter\'s Point',8),(245,'Huntingdon',16),(246,'Inukjuak',10),(247,'Inverness',17),(248,'Irlande',12),(249,'Ivry-sur-le-Lac',15),(250,'Ivujivik',10),(251,'Joliette',14),(252,'Kahnawake',16),(253,'Kamouraska',1),(254,'Kanesatake',15),(255,'Kangiqsualujjuaq',10),(256,'Kangiqsujuaq',10),(257,'Kangirsuk',10),(258,'Kataskomiq',1),(259,'Kawawachikamach',10),(260,'Kawawachikamach',9),(261,'Kazabazua',7),(262,'Kebaowek',8),(263,'Kiamika',15),(264,'Kingsbury',5),(265,'Kingsey Falls',17),(266,'Kinnear\'s Mills',12),(267,'Kipawa',8),(268,'Kirkland',6),(269,'Kitcisakik',8),(270,'Kitigan Zibi',7),(271,'Kuujjuaq',10),(272,'Kuujjuarapik',10),(273,'Labelle',15),(274,'La Bostonnais',4),(275,'Labrecque',2),(276,'Lac-Achouakan',2),(277,'Lac-Akonapwehikan',15),(278,'Lac-à-la-Croix',1),(279,'Lac-Alfred',1),(280,'Lac-Ashuapmushuan',2),(281,'Lac-au-Brochet',9),(282,'Lac-au-Saumon',1),(283,'Lac-aux-Sables',4),(284,'Lac-Bazinet',15),(285,'Lac-Beauport',3),(286,'Lac-Blanc',3),(287,'Lac-Boisbouscache',1),(288,'Lac-Bouchette',2),(289,'Lac-Boulé',4),(290,'Lac-Brome',16),(291,'Lac-Cabasta',14),(292,'Lac-Casault',1),(293,'Lac-Chicobi',8),(294,'Lac-Croche',3),(295,'Lac-De La Bidière',15),(296,'Lac-Delage',3),(297,'Lac-de-la-Maison-de-Pierre',15),(298,'Lac-de-la-Pomme',15),(299,'Lac-des-Aigles',1),(300,'Lac-des-Dix-Milles',14),(301,'Lac-des-Eaux-Mortes',1),(302,'Lac-des-Écorces',15),(303,'Lac-Despinassy',8),(304,'Lac-des-Plages',7),(305,'Lac-des-Seize-Îles',15),(306,'Lac-Devenyns',14),(307,'Lac-Douaire',15),(308,'Lac-Drolet',5),(309,'Lac-du-Cerf',15),(310,'Lac-Duparquet',8),(311,'Lac-du-Taureau',14),(312,'Lac-Édouard',4),(313,'Lac-Ernest',15),(314,'Lac-Etchemin',12),(315,'Lac-Frontière',12),(316,'Lac-Granet',8),(317,'Lac-Huron',1),(318,'Lachute',15),(319,'Lac-Jacques-Cartier',3),(320,'Lac-Jérôme',9),(321,'Lac-John',9),(322,'Lac-Juillet',9),(323,'Lac-Lapeyrère',3),(324,'Lac-Legendre',14),(325,'Lac-Lenôtre',7),(326,'Lac-Marguerite',15),(327,'Lac-Masketsi',4),(328,'Lac-Matapédia',1),(329,'Lac-Matawin',14),(330,'Lac-Mégantic',5),(331,'Lac-Metei',8),(332,'Lac-Minaki',14),(333,'Lac-Ministuk',2),(334,'Lac-Moncouche',2),(335,'Lac-Moselle',7),(336,'Lac-Nilgaut',7),(337,'Lac-Normand',4),(338,'Lacolle',16),(339,'La Conception',15),(340,'La Corne',8),(341,'Lac-Oscar',15),(342,'Lac-Pikauba',3),(343,'Lac-Poulin',12),(344,'Lac-Pythonga',7),(345,'Lac-Rapide',7),(346,'Lac-Saguay',15),(347,'Lac-Sainte-Marie',7),(348,'Lac-Saint-Joseph',3),(349,'Lac-Saint-Paul',15),(350,'Lac-Santé',14),(351,'Lac-Sergent',3),(352,'Lac-Simon',7),(353,'Lac-Simon',8),(354,'Lac-Supérieur',15),(355,'Lac-Tremblant-Nord',15),(356,'Lac-Vacher',9),(357,'Lac-Wagwabika',15),(358,'Lac-Walker',9),(359,'La Doré',2),(360,'La Durantaye',12),(361,'Laforce',8),(362,'La Guadeloupe',12),(363,'Lalemant',2),(364,'La Macaza',15),(365,'La Malbaie',3),(366,'Lamarche',2),(367,'La Martre',11),(368,'Lambton',5),(369,'La Minerve',15),(370,'La Morandière',8),(371,'La Motte',8),(372,'L\'Ancienne-Lorette',3),(373,'Landrienne',8),(374,'L\'Ange-Gardien',7),(375,'L\'Ange-Gardien',3),(376,'Laniel',8),(377,'Lanoraie',14),(378,'L\'Anse-Saint-Jean',2),(379,'Lantier',15),(380,'La Patrie',5),(381,'La Pêche',7),(382,'La Pocatière',1),(383,'La Prairie',16),(384,'La Présentation',16),(385,'La Rédemption',1),(386,'La Reine',8),(387,'La Romaine',9),(388,'Larouche',2),(389,'La Sarre',8),(390,'L\'Ascension',15),(391,'L\'Ascension-de-Notre-Seigneur',2),(392,'L\'Ascension-de-Patapédia',11),(393,'L\'Assomption',14),(394,'La Trinité-des-Monts',1),(395,'Latulipe-et-Gaboury',8),(396,'La Tuque',4),(397,'Launay',8),(398,'Laurier-Station',12),(399,'Laurierville',17),(400,'Laval',13),(401,'Lavaltrie',14),(402,'L\'Avenir',17),(403,'Laverlochère-Angliers',8),(404,'La Visitation-de-l\'Île-Dupas',14),(405,'La Visitation-de-Yamaska',17),(406,'Lawrenceville',5),(407,'Lebel-sur-Quévillon',10),(408,'Leclercville',12),(409,'Lefebvre',17),(410,'Lejeune',1),(411,'Lemieux',17),(412,'L\'Épiphanie',14),(413,'Léry',16),(414,'Les Bergeronnes',9),(415,'Les Cèdres',16),(416,'Les Coteaux',16),(417,'Les Éboulements',3),(418,'Les Escoumins',9),(419,'Les Hauteurs',1),(420,'Les Îles-de-la-Madeleine',11),(421,'Les Lacs-du-Témiscamingue',8),(422,'Les Méchins',1),(423,'Lévis',12),(424,'L\'Île-Cadieux',16),(425,'L\'Île-d\'Anticosti',9),(426,'L\'Île-Dorval',6),(427,'L\'Île-du-Grand-Calumet',7),(428,'L\'Île-Perrot',16),(429,'Lingwick',5),(430,'Linton',3),(431,'L\'Isle-aux-Allumettes',7),(432,'L\'Isle-aux-Coudres',3),(433,'L\'Islet',12),(434,'L\'Isle-Verte',1),(435,'Listuguj',11),(436,'Litchfield',7),(437,'Lochaber',7),(438,'Lochaber-Partie-Ouest',7),(439,'Longue-Pointe-de-Mingan',9),(440,'Longue-Rive',9),(441,'Longueuil',16),(442,'Lorraine',15),(443,'Lorrainville',8),(444,'Lotbinière',12),(445,'Louiseville',4),(446,'Low',7),(447,'Lyster',17),(448,'Macamic',8),(449,'Maddington Falls',17),(450,'Magog',5),(451,'Malartic',8),(452,'Maliotenam',9),(453,'Manawan',14),(454,'Mandeville',14),(455,'Maniwaki',7),(456,'Manseau',17),(457,'Mansfield-et-Pontefract',7),(458,'Maria',11),(459,'Maricourt',5),(460,'Marieville',16),(461,'Marsoui',11),(462,'Marston',5),(463,'Martinville',5),(464,'Mascouche',14),(465,'Mashteuiatsh',2),(466,'Maskinongé',4),(467,'Massueville',16),(468,'Matagami',10),(469,'Matane',1),(470,'Matapédia',11),(471,'Matchi-Manitou',8),(472,'Matimekosh',9),(473,'Mayo',7),(474,'McMasterville',16),(475,'Melbourne',5),(476,'Mercier',16),(477,'Messines',7),(478,'Métabetchouan–Lac-à-la-Croix',2),(479,'Métis-sur-Mer',1),(480,'Milan',5),(481,'Mille-Isles',15),(482,'Mingan',9),(483,'Mirabel',15),(484,'Mistissini',10),(485,'Moffet',8),(486,'Mont-Albert',11),(487,'Mont-Alexandre',11),(488,'Mont-Apica',2),(489,'Montcalm',15),(490,'Mont-Carmel',1),(491,'Montcerf-Lytton',7),(492,'Montebello',7),(493,'Mont-Élie',3),(494,'Mont-Joli',1),(495,'Mont-Laurier',15),(496,'Montmagny',12),(497,'Montpellier',7),(498,'Montréal',6),(499,'Montréal-Est',6),(500,'Montréal-Ouest',6),(501,'Mont-Royal',6),(502,'Mont-Saint-Grégoire',16),(503,'Mont-Saint-Hilaire',16),(504,'Mont-Saint-Michel',15),(505,'Mont-Saint-Pierre',11),(506,'Mont-Tremblant',15),(507,'Mont-Valin',2),(508,'Morin-Heights',15),(509,'Mulgrave-et-Derry',7),(510,'Murdochville',11),(511,'Namur',7),(512,'Nantes',5),(513,'Napierville',16),(514,'Natashquan',9),(515,'Nédélec',8),(516,'Nemaska',10),(517,'Neuville',3),(518,'New Carlisle',11),(519,'Newport',5),(520,'New Richmond',11),(521,'Nicolet',17),(522,'Nominingue',15),(523,'Normandin',2),(524,'Normétal',8),(525,'North Hatley',5),(526,'Notre-Dame-Auxiliatrice-de-Buckland',12),(527,'Notre-Dame-de-Bonsecours',7),(528,'Notre-Dame-de-Ham',17),(529,'Notre-Dame-de-la-Merci',14),(530,'Notre-Dame-de-la-Paix',7),(531,'Notre-Dame-de-la-Salette',7),(532,'Notre-Dame-de-l\'Île-Perrot',16),(533,'Notre-Dame-de-Lorette',2),(534,'Notre-Dame-de-Lourdes',14),(535,'Notre-Dame-de-Lourdes',17),(536,'Notre-Dame-de-Montauban',4),(537,'Notre-Dame-de-Pontmain',15),(538,'Notre-Dame-des-Anges',3),(539,'Notre-Dame-des-Bois',5),(540,'Notre-Dame-des-Monts',3),(541,'Notre-Dame-des-Neiges',1),(542,'Notre-Dame-des-Pins',12),(543,'Notre-Dame-des-Prairies',14),(544,'Notre-Dame-des-Sept-Douleurs',1),(545,'Notre-Dame-de-Staididge',16),(546,'Notre-Dame-du-Bon-Conseil',17),(547,'Notre-Dame-du-Laus',15),(548,'Notre-Dame-du-Mont-Carmel',4),(549,'Notre-Dame-du-Nord',8),(550,'Notre-Dame-du-Portage',1),(551,'Notre-Dame-du-Rosaire',12),(552,'Notre-Dame-du-Sacré-Cœur-d\'Issoudun',12),(553,'Nouvelle',11),(554,'Noyan',16),(555,'Nutashkuan',9),(556,'Obedjiwan',4),(557,'Odanak',17),(558,'Ogden',5),(559,'Oka',15),(560,'Orford',5),(561,'Ormstown',16),(562,'Otterburn Park',16),(563,'Otter Lake',7),(564,'Oujé-Bougoumou',10),(565,'Packington',1),(566,'Padoue',1),(567,'Pakuashipi',9),(568,'Palmarolle',8),(569,'Papineauville',7),(570,'Parisville',17),(571,'Paspébiac',11),(572,'Passes-Dangereuses',2),(573,'Percé',11),(574,'Péribonka',2),(575,'Pessamit',9),(576,'Petite-Rivière-Saint-François',3),(577,'Petite-Vallée',11),(578,'Petit-Lac-Sainte-Anne',1),(579,'Petit-Mécatina',9),(580,'Petit-Saguenay',2),(581,'Picard',1),(582,'Piedmont',15),(583,'Pierreville',17),(584,'Pike River',16),(585,'Pikogan',8),(586,'Pincourt',16),(587,'Piopolis',5),(588,'Plaisance',7),(589,'Plessisville',17),(590,'Pohénégamook',1),(591,'Pointe-à-la-Croix',11),(592,'Pointe-aux-Outardes',9),(593,'Pointe-Calumet',15),(594,'Pointe-Claire',6),(595,'Pointe-des-Cascades',16),(596,'Pointe-Fortune',16),(597,'Pointe-Lebel',9),(598,'Pontiac',7),(599,'Pont-Rouge',3),(600,'Portage-du-Fort',7),(601,'Port-Cartier',9),(602,'Port-Daniel–Gascons',11),(603,'Portneuf',3),(604,'Portneuf-sur-Mer',9),(605,'Potton',5),(606,'Poularies',8),(607,'Preissac',8),(608,'Prévost',15),(609,'Price',1),(610,'Princeville',17),(611,'Puvirnituq',10),(612,'Quaqtaq',10),(613,'Québec',3),(614,'Racine',5),(615,'Ragueneau',9),(616,'Rapide-Danseur',8),(617,'Rapides-des-Joachims',7),(618,'Rawdon',14),(619,'Rémigny',8),(620,'Repentigny',14),(621,'Réservoir-Dozois',8),(622,'Richelieu',16),(623,'Richmond',5),(624,'Rigaud',16),(625,'Rimouski',1),(626,'Ripon',7),(627,'Ristigouche-Partie-Sud-Est',11),(628,'Rivière-à-Claude',11),(629,'Rivière-à-Pierre',3),(630,'Rivière-au-Tonnerre',9),(631,'Rivière-aux-Outardes',9),(632,'Rivière-Beaudette',16),(633,'Rivière-Bleue',1),(634,'Rivière-Bonaventure',11),(635,'Rivière-Bonjour',1),(636,'Rivière-de-la-Savane',4),(637,'Rivière-du-Loup',1),(638,'Rivière-Éternité',2),(639,'Rivière-Héva',8),(640,'Rivière-Koksoak',10),(641,'Rivière-Mistassini',2),(642,'Rivière-Mouchalagane',9),(643,'Rivière-Nipissis',9),(644,'Rivière-Nouvelle',11),(645,'Rivière-Ojima',8),(646,'Rivière-Ouelle',1),(647,'Rivière-Patapédia-Est',1),(648,'Rivière-Rouge',15),(649,'Rivière-Saint-Jean',11),(650,'Rivière-Saint-Jean',9),(651,'Rivière-Vaseuse',1),(652,'Roberval',2),(653,'Rochebaucourt',8),(654,'Roquemaure',8),(655,'Rosemère',15),(656,'Rougemont',16),(657,'Routhierville',1),(658,'Rouyn-Noranda',8),(659,'Roxton',16),(660,'Roxton Falls',16),(661,'Roxton Pond',16),(662,'Ruisseau-des-Mineurs',1),(663,'Ruisseau-Ferguson',11),(664,'Sacré-Cœur',9),(665,'Sacré-Cœur-de-Jésus',12),(666,'Sagard',3),(667,'Saguenay',2),(668,'Saint-Adalbert',12),(669,'Saint-Adelme',1),(670,'Saint-Adelphe',4),(671,'Saint-Adolphe-d\'Howard',15),(672,'Saint-Adrien',5),(673,'Saint-Adrien-d\'Irlande',12),(674,'Saint-Agapit',12),(675,'Saint-Aimé',16),(676,'Saint-Aimé-des-Lacs',3),(677,'Saint-Aimé-du-Lac-des-Îles',15),(678,'Saint-Alban',3),(679,'Saint-Albert',17),(680,'Saint-Alexandre',16),(681,'Saint-Alexandre-de-Kamouraska',1),(682,'Saint-Alexandre-des-Lacs',1),(683,'Saint-Alexis',14),(684,'Saint-Alexis-de-Matapédia',11),(685,'Saint-Alexis-des-Monts',4),(686,'Saint-Alfred',12),(687,'Saint-Alphonse',11),(688,'Saint-Alphonse-de-Granby',16),(689,'Saint-Alphonse-Rodriguez',14),(690,'Saint-Amable',16),(691,'Saint-Ambroise',2),(692,'Saint-Ambroise-de-Kildare',14),(693,'Saint-Anaclet-de-Lessard',1),(694,'Saint-André-Avellin',7),(695,'Saint-André-d\'Argenteuil',15),(696,'Saint-André-de-Kamouraska',1),(697,'Saint-André-de-Restigouche',11),(698,'Saint-André-du-Lac-Saint-Jean',2),(699,'Saint-Anicet',16),(700,'Saint-Anselme',12),(701,'Saint-Antoine-de-l\'Isle-aux-Grues',12),(702,'Saint-Antoine-de-Tilly',12),(703,'Saint-Antoine-sur-Richelieu',16),(704,'Saint-Antonin',1),(705,'Saint-Apollinaire',12),(706,'Saint-Armand',16),(707,'Saint-Arsène',1),(708,'Saint-Athanase',1),(709,'Saint-Aubert',12),(710,'Saint-Augustin',2),(711,'Saint-Augustin',9),(712,'Saint-Augustin-de-Desmaures',3),(713,'Saint-Augustin-de-Woburn',5),(714,'Saint-Barnabé',4),(715,'Saint-Barnabé-Sud',16),(716,'Saint-Barthélemy',14),(717,'Saint-Basile',3),(718,'Saint-Basile-le-Grand',16),(719,'Saint-Benjamin',12),(720,'Saint-Benoît-du-Lac',5),(721,'Saint-Benoît-Labre',12),(722,'Saint-Bernard',12),(723,'Saint-Bernard-de-Lacolle',16),(724,'Saint-Bernard-de-Michaudville',16),(725,'Saint-Blaise-sur-Richelieu',16),(726,'Saint-Bonaventure',17),(727,'Saint-Boniface',4),(728,'Saint-Bruno',2),(729,'Saint-Bruno-de-Guigues',8),(730,'Saint-Bruno-de-Kamouraska',1),(731,'Saint-Bruno-de-Montarville',16),(732,'Saint-Calixte',14),(733,'Saint-Camille',5),(734,'Saint-Camille-de-Lellis',12),(735,'Saint-Casimir',3),(736,'Saint-Célestin',17),(737,'Saint-Césaire',16),(738,'Saint-Charles-Borromée',14),(739,'Saint-Charles-de-Bellechasse',12),(740,'Saint-Charles-de-Bourget',2),(741,'Saint-Charles-Garnier',1),(742,'Saint-Charles-sur-Richelieu',16),(743,'Saint-Christophe-d\'Arthabaska',17),(744,'Saint-Chrysostome',16),(745,'Saint-Claude',5),(746,'Saint-Clément',1),(747,'Saint-Cléophas',1),(748,'Saint-Cléophas-de-Brandon',14),(749,'Saint-Clet',16),(750,'Saint-Colomban',15),(751,'Saint-Côme',14),(752,'Saint-Côme–Linière',12),(753,'Saint-Constant',16),(754,'Saint-Cuthbert',14),(755,'Saint-Cyprien',12),(756,'Saint-Cyprien',1),(757,'Saint-Cyprien-de-Napierville',16),(758,'Saint-Cyrille-de-Lessard',12),(759,'Saint-Cyrille-de-Wendover',17),(760,'Saint-Damase',16),(761,'Saint-Damase',1),(762,'Saint-Damase-de-L\'Islet',12),(763,'Saint-Damien',14),(764,'Saint-Damien-de-Buckland',12),(765,'Saint-David',16),(766,'Saint-David-de-Falardeau',2),(767,'Saint-Denis-de-Brompton',5),(768,'Saint-Denis-De La Bouteillerie',1),(769,'Saint-Denis-sur-Richelieu',16),(770,'Saint-Didace',14),(771,'Saint-Dominique',16),(772,'Saint-Dominique-du-Rosaire',8),(773,'Saint-Donat',14),(774,'Saint-Donat',1),(775,'Sainte-Adèle',15),(776,'Sainte-Agathe-de-Lotbinière',12),(777,'Sainte-Agathe-des-Monts',15),(778,'Sainte-Angèle-de-Mérici',1),(779,'Sainte-Angèle-de-Monnoir',16),(780,'Sainte-Angèle-de-Prémont',4),(781,'Sainte-Anne-de-Beaupré',3),(782,'Sainte-Anne-de-Bellevue',6),(783,'Sainte-Anne-de-la-Pérade',4),(784,'Sainte-Anne-de-la-Pocatière',1),(785,'Sainte-Anne-de-la-Rochelle',5),(786,'Sainte-Anne-de-Sabrevois',16),(787,'Sainte-Anne-des-Lacs',15),(788,'Sainte-Anne-des-Monts',11),(789,'Sainte-Anne-de-Sorel',16),(790,'Sainte-Anne-des-Plaines',15),(791,'Sainte-Anne-du-Lac',15),(792,'Sainte-Apolline-de-Patton',12),(793,'Sainte-Aurélie',12),(794,'Sainte-Barbe',16),(795,'Sainte-Béatrix',14),(796,'Sainte-Brigide-d\'Iberville',16),(797,'Sainte-Brigitte-de-Laval',3),(798,'Sainte-Brigitte-des-Saults',17),(799,'Sainte-Catherine',16),(800,'Sainte-Catherine-de-Hatley',5),(801,'Sainte-Catherine-de-la-Jacques-Cartier',3),(802,'Sainte-Cécile-de-Lévrard',17),(803,'Sainte-Cécile-de-Milton',16),(804,'Sainte-Cécile-de-Whitton',5),(805,'Sainte-Christine',16),(806,'Sainte-Christine-d\'Auvergne',3),(807,'Sainte-Claire',12),(808,'Sainte-Clotilde',16),(809,'Sainte-Clotilde-de-Beauce',12),(810,'Sainte-Clotilde-de-Horton',17),(811,'Sainte-Croix',12),(812,'Saint-Edmond-de-Grantham',17),(813,'Saint-Edmond-les-Plaines',2),(814,'Saint-Édouard',16),(815,'Saint-Édouard-de-Fabre',8),(816,'Saint-Édouard-de-Lotbinière',12),(817,'Saint-Édouard-de-Maskinongé',4),(818,'Sainte-Edwidge-de-Clifton',5),(819,'Sainte-Élisabeth',14),(820,'Sainte-Élizabeth-de-Warwick',17),(821,'Sainte-Émélie-de-l\'Énergie',14),(822,'Sainte-Eulalie',17),(823,'Sainte-Euphémie-sur-Rivière-du-Sud',12),(824,'Sainte-Famille-de-l\'Île-d\'Orléans',3),(825,'Sainte-Félicité',12),(826,'Sainte-Félicité',1),(827,'Sainte-Flavie',1),(828,'Sainte-Florence',1),(829,'Sainte-Françoise',1),(830,'Sainte-Françoise',17),(831,'Sainte-Geneviève-de-Batiscan',4),(832,'Sainte-Geneviève-de-Berthier',14),(833,'Sainte-Germaine-Boulé',8),(834,'Sainte-Gertrude-Manneville',8),(835,'Sainte-Hedwidge',2),(836,'Sainte-Hélène-de-Bagot',16),(837,'Sainte-Hélène-de-Chester',17),(838,'Sainte-Hélène-de-Kamouraska',1),(839,'Sainte-Hélène-de-Mancebourg',8),(840,'Sainte-Hénédine',12),(841,'Sainte-Irène',1),(842,'Sainte-Jeanne-d\'Arc',1),(843,'Sainte-Jeanne-d\'Arc',2),(844,'Sainte-Julie',16),(845,'Sainte-Julienne',14),(846,'Sainte-Justine',12),(847,'Sainte-Justine-de-Newton',16),(848,'Saint-Élie-de-Caxton',4),(849,'Saint-Éloi',1),(850,'Sainte-Louise',12),(851,'Saint-Elphège',17),(852,'Sainte-Luce',1),(853,'Sainte-Lucie-de-Beauregard',12),(854,'Sainte-Lucie-des-Laurentides',15),(855,'Saint-Elzéar',12),(856,'Saint-Elzéar',11),(857,'Saint-Elzéar-de-Témiscouata',1),(858,'Sainte-Madeleine',16),(859,'Sainte-Madeleine-de-la-Rivière-Madeleine',11),(860,'Sainte-Marcelline-de-Kildare',14),(861,'Sainte-Marguerite',12),(862,'Sainte-Marguerite-du-Lac-Masson',15),(863,'Sainte-Marguerite-Marie',1),(864,'Sainte-Marie',12),(865,'Sainte-Marie-de-Blandford',17),(866,'Sainte-Marie-Madeleine',16),(867,'Sainte-Marie-Salomé',14),(868,'Sainte-Marthe',16),(869,'Sainte-Marthe-sur-le-Lac',15),(870,'Sainte-Martine',16),(871,'Sainte-Mélanie',14),(872,'Saint-Émile-de-Suffolk',7),(873,'Sainte-Monique',17),(874,'Sainte-Monique',2),(875,'Sainte-Paule',1),(876,'Sainte-Perpétue',12),(877,'Sainte-Perpétue',17),(878,'Sainte-Pétronille',3),(879,'Saint-Éphrem-de-Beauce',12),(880,'Saint-Épiphane',1),(881,'Sainte-Praxède',12),(882,'Sainte-Rita',1),(883,'Sainte-Rose-de-Watford',12),(884,'Sainte-Rose-du-Nord',2),(885,'Sainte-Sabine',12),(886,'Sainte-Sabine',16),(887,'Sainte-Séraphine',17),(888,'Sainte-Sophie',15),(889,'Sainte-Sophie-de-Lévrard',17),(890,'Sainte-Sophie-d\'Halifax',17),(891,'Saint-Esprit',14),(892,'Sainte-Thècle',4),(893,'Sainte-Thérèse',15),(894,'Sainte-Thérèse-de-Gaspé',11),(895,'Sainte-Thérèse-de-la-Gatineau',7),(896,'Saint-Étienne-de-Beauharnois',16),(897,'Saint-Étienne-de-Bolton',5),(898,'Saint-Étienne-des-Grès',4),(899,'Saint-Eugène',17),(900,'Saint-Eugène-d\'Argentenay',2),(901,'Saint-Eugène-de-Guigues',8),(902,'Saint-Eugène-de-Ladrière',1),(903,'Sainte-Ursule',4),(904,'Saint-Eusèbe',1),(905,'Saint-Eustache',15),(906,'Saint-Évariste-de-Forsyth',12),(907,'Sainte-Victoire-de-Sorel',16),(908,'Saint-Fabien',1),(909,'Saint-Fabien-de-Panet',12),(910,'Saint-Faustin–Lac-Carré',15),(911,'Saint-Félicien',2),(912,'Saint-Félix-de-Dalquier',8),(913,'Saint-Félix-de-Kingsey',17),(914,'Saint-Félix-de-Valois',14),(915,'Saint-Félix-d\'Otis',2),(916,'Saint-Ferdinand',17),(917,'Saint-Ferréol-les-Neiges',3),(918,'Saint-Flavien',12),(919,'Saint-Fortunat',12),(920,'Saint-François-d\'Assise',11),(921,'Saint-François-de-la-Rivière-du-Sud',12),(922,'Saint-François-de-l\'Île-d\'Orléans',3),(923,'Saint-François-de-Sales',2),(924,'Saint-François-du-Lac',17),(925,'Saint-François-Xavier-de-Brompton',5),(926,'Saint-François-Xavier-de-Viger',1),(927,'Saint-Frédéric',12),(928,'Saint-Fulgence',2),(929,'Saint-Gabriel',14),(930,'Saint-Gabriel-de-Brandon',14),(931,'Saint-Gabriel-de-Rimouski',1),(932,'Saint-Gabriel-de-Valcartier',3),(933,'Saint-Gabriel-Lalemant',1),(934,'Saint-Gédéon',2),(935,'Saint-Gédéon-de-Beauce',12),(936,'Saint-Georges',12),(937,'Saint-Georges-de-Clarenceville',16),(938,'Saint-Georges-de-Windsor',5),(939,'Saint-Gérard-Majella',16),(940,'Saint-Germain',1),(941,'Saint-Germain-de-Grantham',17),(942,'Saint-Gervais',12),(943,'Saint-Gilbert',3),(944,'Saint-Gilles',12),(945,'Saint-Godefroi',11),(946,'Saint-Guillaume',17),(947,'Saint-Guillaume-Nord',14),(948,'Saint-Guy',1),(949,'Saint-Henri',12),(950,'Saint-Henri-de-Taillon',2),(951,'Saint-Herménégilde',5),(952,'Saint-Hilaire-de-Dorset',12),(953,'Saint-Hilarion',3),(954,'Saint-Hippolyte',15),(955,'Saint-Honoré',2),(956,'Saint-Honoré-de-Shenley',12),(957,'Saint-Honoré-de-Témiscouata',1),(958,'Saint-Hubert-de-Rivière-du-Loup',1),(959,'Saint-Hugues',16),(960,'Saint-Hyacinthe',16),(961,'Saint-Ignace-de-Loyola',14),(962,'Saint-Ignace-de-Staididge',16),(963,'Saint-Irénée',3),(964,'Saint-Isidore',12),(965,'Saint-Isidore',16),(966,'Saint-Isidore-de-Clifton',5),(967,'Saint-Jacques',14),(968,'Saint-Jacques-de-Leeds',12),(969,'Saint-Jacques-le-Majeur-de-Wolfestown',12),(970,'Saint-Jacques-le-Mineur',16),(971,'Saint-Janvier-de-Joly',12),(972,'Saint-Jean-Baptiste',16),(973,'Saint-Jean-de-Brébeuf',12),(974,'Saint-Jean-de-Cherbourg',1),(975,'Saint-Jean-de-Dieu',1),(976,'Saint-Jean-de-la-Lande',1),(977,'Saint-Jean-de-l\'Île-d\'Orléans',3),(978,'Saint-Jean-de-Matha',14),(979,'Saint-Jean-Port-Joli',12),(980,'Saint-Jean-sur-Richelieu',16),(981,'Saint-Jérôme',15),(982,'Saint-Joachim',3),(983,'Saint-Joachim-de-Shefford',16),(984,'Saint-Joseph-de-Beauce',12),(985,'Saint-Joseph-de-Coleraine',12),(986,'Saint-Joseph-de-Kamouraska',1),(987,'Saint-Joseph-de-Lepage',1),(988,'Saint-Joseph-des-Érables',12),(989,'Saint-Joseph-de-Sorel',16),(990,'Saint-Joseph-du-Lac',15),(991,'Saint-Jude',16),(992,'Saint-Jules',12),(993,'Saint-Julien',12),(994,'Saint-Just-de-Bretenières',12),(995,'Saint-Juste-du-Lac',1),(996,'Saint-Justin',4),(997,'Saint-Lambert',16),(998,'Saint-Lambert',8),(999,'Saint-Lambert-de-Lauzon',12),(1000,'Saint-Laurent-de-l\'Île-d\'Orléans',3),(1001,'Saint-Lazare',16),(1002,'Saint-Lazare-de-Bellechasse',12),(1003,'Saint-Léandre',1),(1004,'Saint-Léonard-d\'Aston',17),(1005,'Saint-Léonard-de-Portneuf',3),(1006,'Saint-Léon-de-Standon',12),(1007,'Saint-Léon-le-Grand',1),(1008,'Saint-Léon-le-Grand',4),(1009,'Saint-Liboire',16),(1010,'Saint-Liguori',14),(1011,'Saint-Lin–Laurentides',14),(1012,'Saint-Louis',16),(1013,'Saint-Louis-de-Blandford',17),(1014,'Saint-Louis-de-Gonzague',12),(1015,'Saint-Louis-de-Gonzague',16),(1016,'Saint-Louis-de-Gonzague-du-Cap-Tourmente',3),(1017,'Saint-Louis-du-Ha! Ha!',1),(1018,'Saint-Luc-de-Bellechasse',12),(1019,'Saint-Luc-de-Vincennes',4),(1020,'Saint-Lucien',17),(1021,'Saint-Ludger',5),(1022,'Saint-Ludger-de-Milot',2),(1023,'Saint-Magloire',12),(1024,'Saint-Majorique-de-Grantham',17),(1025,'Saint-Malachie',12),(1026,'Saint-Malo',5),(1027,'Saint-Marc-de-Figuery',8),(1028,'Saint-Marc-des-Carrières',3),(1029,'Saint-Marc-du-Lac-Long',1),(1030,'Saint-Marcel',12),(1031,'Saint-Marcel-de-Richelieu',16),(1032,'Saint-Marcellin',1),(1033,'Saint-Marc-sur-Richelieu',16),(1034,'Saint-Martin',12),(1035,'Saint-Mathias-sur-Richelieu',16),(1036,'Saint-Mathieu',16),(1037,'Saint-Mathieu-de-Belœil',16),(1038,'Saint-Mathieu-de-Rioux',1),(1039,'Saint-Mathieu-d\'Harricana',8),(1040,'Saint-Mathieu-du-Parc',4),(1041,'Saint-Maurice',4),(1042,'Saint-Maxime-du-Mont-Louis',11),(1043,'Saint-Médard',1),(1044,'Saint-Michel',16),(1045,'Saint-Michel-de-Bellechasse',12),(1046,'Saint-Michel-des-Saints',14),(1047,'Saint-Michel-du-Squatec',1),(1048,'Saint-Modeste',1),(1049,'Saint-Moïse',1),(1050,'Saint-Narcisse',4),(1051,'Saint-Narcisse-de-Beaurivage',12),(1052,'Saint-Narcisse-de-Rimouski',1),(1053,'Saint-Nazaire',2),(1054,'Saint-Nazaire-d\'Acton',16),(1055,'Saint-Nazaire-de-Dorchester',12),(1056,'Saint-Nérée-de-Bellechasse',12),(1057,'Saint-Noël',1),(1058,'Saint-Norbert',14),(1059,'Saint-Norbert-d\'Arthabaska',17),(1060,'Saint-Octave-de-Métis',1),(1061,'Saint-Odilon-de-Cranbourne',12),(1062,'Saint-Omer',12),(1063,'Saint-Onésime-d\'Ixworth',1),(1064,'Saint-Ours',16),(1065,'Saint-Pacôme',1),(1066,'Saint-Pamphile',12),(1067,'Saint-Pascal',1),(1068,'Saint-Patrice-de-Beaurivage',12),(1069,'Saint-Patrice-de-Sherrington',16),(1070,'Saint-Paul',14),(1071,'Saint-Paul-d\'Abbotsford',16),(1072,'Saint-Paul-de-la-Croix',1),(1073,'Saint-Paul-de-l\'Île-aux-Noix',16),(1074,'Saint-Paul-de-Montminy',12),(1075,'Saint-Paulin',4),(1076,'Saint-Philémon',12),(1077,'Saint-Philibert',12),(1078,'Saint-Philippe',16),(1079,'Saint-Philippe-de-Néri',1),(1080,'Saint-Pie',16),(1081,'Saint-Pie-de-Guire',17),(1082,'Saint-Pierre',14),(1083,'Saint-Pierre-Baptiste',17),(1084,'Saint-Pierre-de-Broughton',12),(1085,'Saint-Pierre-de-Lamy',1),(1086,'Saint-Pierre-de-la-Rivière-du-Sud',12),(1087,'Saint-Pierre-de-l\'Île-d\'Orléans',3),(1088,'Saint-Pierre-les-Becquets',17),(1089,'Saint-Placide',15),(1090,'Saint-Polycarpe',16),(1091,'Saint-Prime',2),(1092,'Saint-Prosper',12),(1093,'Saint-Prosper-de-Champlain',4),(1094,'Saint-Raphaël',12),(1095,'Saint-Raymond',3),(1096,'Saint-Rémi',16),(1097,'Saint-Rémi-de-Tingwick',17),(1098,'Saint-René',12),(1099,'Saint-René-de-Matane',1),(1100,'Saint-Robert',16),(1101,'Saint-Robert-Bellarmin',5),(1102,'Saint-Roch-de-l\'Achigan',14),(1103,'Saint-Roch-de-Mékinac',4),(1104,'Saint-Roch-de-Richelieu',16),(1105,'Saint-Roch-des-Aulnaies',12),(1106,'Saint-Roch-Ouest',14),(1107,'Saint-Romain',5),(1108,'Saint-Rosaire',17),(1109,'Saint-Samuel',17),(1110,'Saints-Anges',12),(1111,'Saint-Sauveur',15),(1112,'Saint-Sébastien',16),(1113,'Saint-Sébastien',5),(1114,'Saint-Sévère',4),(1115,'Saint-Séverin',12),(1116,'Saint-Séverin',4),(1117,'Saint-Siméon',3),(1118,'Saint-Siméon',11),(1119,'Saint-Simon',16),(1120,'Saint-Simon-de-Rimouski',1),(1121,'Saint-Simon-les-Mines',12),(1122,'Saint-Sixte',7),(1123,'Saints-Martyrs-Canadiens',17),(1124,'Saint-Stanislas',4),(1125,'Saint-Stanislas',2),(1126,'Saint-Stanislas-de-Kostka',16),(1127,'Saint-Sulpice',14),(1128,'Saint-Sylvère',17),(1129,'Saint-Sylvestre',12),(1130,'Saint-Télesphore',16),(1131,'Saint-Tharcisius',1),(1132,'Saint-Théodore-d\'Acton',16),(1133,'Saint-Théophile',12),(1134,'Saint-Thomas',14),(1135,'Saint-Thomas-Didyme',2),(1136,'Saint-Thuribe',3),(1137,'Saint-Tite',4),(1138,'Saint-Tite-des-Caps',3),(1139,'Saint-Ubalde',3),(1140,'Saint-Ulric',1),(1141,'Saint-Urbain',3),(1142,'Saint-Urbain-Premier',16),(1143,'Saint-Valentin',16),(1144,'Saint-Valère',17),(1145,'Saint-Valérien',1),(1146,'Saint-Valérien-de-Milton',16),(1147,'Saint-Vallier',12),(1148,'Saint-Venant-de-Paquette',5),(1149,'Saint-Vianney',1),(1150,'Saint-Victor',12),(1151,'Saint-Wenceslas',17),(1152,'Saint-Zacharie',12),(1153,'Saint-Zénon',14),(1154,'Saint-Zénon-du-Lac-Humqui',1),(1155,'Saint-Zéphirin-de-Courval',17),(1156,'Saint-Zotique',16),(1157,'Salaberry-de-Valleyfield',16),(1158,'Salluit',10),(1159,'Sault-au-Cochon',3),(1160,'Sayabec',1),(1161,'Schefferville',9),(1162,'Scotstown',5),(1163,'Scott',12),(1164,'Senneterre',8),(1165,'Senneville',6),(1166,'Sept-Îles',9),(1167,'Shannon',3),(1168,'Shawinigan',4),(1169,'Shawville',7),(1170,'Sheenboro',7),(1171,'Shefford',16),(1172,'Sherbrooke',5),(1173,'Shigawake',11),(1174,'Sorel-Tracy',16),(1175,'Staididge East',16),(1176,'Staididge Station',16),(1177,'Stanstead',5),(1178,'Stanstead-Est',5),(1179,'Stoke',5),(1180,'Stoneham-et-Tewkesbury',3),(1181,'Stornoway',5),(1182,'Stratford',5),(1183,'Stukely-Sud',5),(1184,'Sutton',16),(1185,'Tadoussac',9),(1186,'Taschereau',8),(1187,'Tasiujaq',10),(1188,'Témiscaming',8),(1189,'Témiscouata-sur-le-Lac',1),(1190,'Terrasse-Vaudreuil',16),(1191,'Terrebonne',14),(1192,'Thetford Mines',12),(1193,'Thorne',7),(1194,'Thurso',7),(1195,'Timiskaming',8),(1196,'Tingwick',17),(1197,'Tourville',12),(1198,'Trécesson',8),(1199,'Très-Saint-Rédempteur',16),(1200,'Très-Saint-Sacrement',16),(1201,'Tring-Jonction',12),(1202,'Trois-Pistoles',1),(1203,'Trois-Rives',4),(1204,'Trois-Rivières',4),(1205,'Uashat',9),(1206,'Ulverton',5),(1207,'Umiujaq',10),(1208,'Upton',16),(1209,'Val-Alain',12),(1210,'Val-Brillant',1),(1211,'Valcourt',5),(1212,'Val-David',15),(1213,'Val-des-Bois',7),(1214,'Val-des-Lacs',15),(1215,'Val-des-Monts',7),(1216,'Val-des-Sources',5),(1217,'Val-d\'Or',8),(1218,'Val-Joli',5),(1219,'Vallée-Jonction',12),(1220,'Val-Morin',15),(1221,'Val-Racine',5),(1222,'Val-Saint-Gilles',8),(1223,'Varennes',16),(1224,'Vaudreuil-Dorion',16),(1225,'Vaudreuil-sur-le-Lac',16),(1226,'Venise-en-Québec',16),(1227,'Verchères',16),(1228,'Victoriaville',17),(1229,'Ville-Marie',8),(1230,'Villeroy',17),(1231,'Waltham',7),(1232,'Warden',16),(1233,'Warwick',17),(1234,'Waskaganish',10),(1235,'Waswanipi',10),(1236,'Waterloo',16),(1237,'Waterville',5),(1238,'Weedon',5),(1239,'Wemindji',10),(1240,'Wemotaci',4),(1241,'Wendake',3),(1242,'Wentworth',15),(1243,'Wentworth-Nord',15),(1244,'Westbury',5),(1245,'Westmount',6),(1246,'Whapmagoostui',10),(1247,'Wickham',17),(1248,'Windsor',5),(1249,'Winneway',8),(1250,'Wôlinak',17),(1251,'Wotton',5),(1252,'Yamachiche',4),(1253,'Yamaska',16);
/*!40000 ALTER TABLE `city` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employers`
--

DROP TABLE IF EXISTS `employers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `employers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `verified` tinyint(1) NOT NULL,
  `userId` int(11) DEFAULT NULL,
  `enterpriseId` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employers`
--

LOCK TABLES `employers` WRITE;
/*!40000 ALTER TABLE `employers` DISABLE KEYS */;
INSERT INTO `employers` VALUES (1,0,2,1);
/*!40000 ALTER TABLE `employers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employment_schedule`
--

DROP TABLE IF EXISTS `employment_schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `employment_schedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employment_schedule`
--

LOCK TABLES `employment_schedule` WRITE;
/*!40000 ALTER TABLE `employment_schedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `employment_schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `enterprise`
--

DROP TABLE IF EXISTS `enterprise`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `enterprise` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `cityId` int(11) NOT NULL,
  `isTemporary` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enterprise`
--

LOCK TABLES `enterprise` WRITE;
/*!40000 ALTER TABLE `enterprise` DISABLE KEYS */;
INSERT INTO `enterprise` VALUES (1,'Deuxieme Tech','Emploi@DT.ca','418-123-4567','80, Rue de la compagnie',0,1);
/*!40000 ALTER TABLE `enterprise` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `job_offer`
--

DROP TABLE IF EXISTS `job_offer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `job_offer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `dateEntryOffice` date NOT NULL,
  `deadlineApply` date NOT NULL,
  `email` varchar(255) NOT NULL,
  `hoursPerWeek` float NOT NULL,
  `compliantEmployer` tinyint(1) NOT NULL,
  `internship` tinyint(1) NOT NULL,
  `offerStatus` int(11) NOT NULL,
  `offerLink` varchar(255) DEFAULT NULL,
  `active` tinyint(1) NOT NULL,
  `employerId` int(11) DEFAULT NULL,
  `scheduleId` int(11) DEFAULT NULL,
  `offerDebut` date NOT NULL,
  `salary` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job_offer`
--

LOCK TABLES `job_offer` WRITE;
/*!40000 ALTER TABLE `job_offer` DISABLE KEYS */;
INSERT INTO `job_offer` VALUES (1,'Stagiaire en Génie Logiciel','123 Rue Principale, Ville, Pays','Nous recherchons un stagiaire talentueux en génie logiciel pour rejoindre notre équipe...','2024-04-01','2024-03-25','rh@exemple.com',20,1,1,1,'https://exemple.com/offre/stagiaire-genie-logiciel',1,1,1,'0000-00-00',''),(2,'Technicien en informatique','80 Rue de l\'entreprise','Le technicien en informatique est chargé de fournir un soutien technique et opérationnel aux utilisateurs','2024-04-19','2024-04-10','RH@DT.ca',35,0,0,0,'https://www.youtube.com/watch?v=xvFZjo5PgG0',1,1,2,'0000-00-00','');
/*!40000 ALTER TABLE `job_offer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `offer_program`
--

DROP TABLE IF EXISTS `offer_program`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `offer_program` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `programId` int(11) NOT NULL,
  `offerId` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offer_program`
--

LOCK TABLES `offer_program` WRITE;
/*!40000 ALTER TABLE `offer_program` DISABLE KEYS */;
INSERT INTO `offer_program` VALUES (1,5,2);
/*!40000 ALTER TABLE `offer_program` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `region`
--

DROP TABLE IF EXISTS `region`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `region` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `region` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `region`
--

LOCK TABLES `region` WRITE;
/*!40000 ALTER TABLE `region` DISABLE KEYS */;
INSERT INTO `region` VALUES (1,'Bas-Saint-Laurent'),(2,'Saguenay-Lac-Saint-Jean'),(3,'Capitale-Nationale'),(4,'Mauricie'),(5,'Estrie'),(6,'Montréal'),(7,'Outaouais'),(8,'Abitibi-Témiscamingue'),(9,'Côte-Nord'),(10,'Nord-du-Québec'),(11,'Gaspésie–Îles-de-la-Madeleine'),(12,'Chaudière-Appalaches'),(13,'Laval'),(14,'Lanaudière'),(15,'Laurentides'),(16,'Montérégie'),(17,'Centre-du-Québec');
/*!40000 ALTER TABLE `region` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `study_program`
--

DROP TABLE IF EXISTS `study_program`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `study_program` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `study_program`
--

LOCK TABLES `study_program` WRITE;
/*!40000 ALTER TABLE `study_program` DISABLE KEYS */;
INSERT INTO `study_program` VALUES (1,'Design d\'intérieur'),(2,'Éducation à l\'enfance'),(3,'Gestion et intervention en loisir'),(4,'Graphisme'),(5,'Informatique'),(6,'Inhalothérapie'),(7,'Pharmacie'),(8,'Soins infirmiers'),(9,'Arts visuels'),(10,'Sciences de la nature'),(11,'Sciences humaines');
/*!40000 ALTER TABLE `study_program` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `isModerator` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (2,'test@gmail.com','$argon2id$v=19$m=65536,t=3,p=4$Vx6PvMyAISxDC13nZYVBEg$4GbyZVkW8rXzD/Ah5axK1W17YM66JYCrLQQkPmUlKOU',1,0),(3,'admin@gmail.com','$argon2id$v=19$m=65536,t=3,p=4$Vx6PvMyAISxDC13nZYVBEg$4GbyZVkW8rXzD/Ah5axK1W17YM66JYCrLQQkPmUlKOU',1,1);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-15 20:29:43

CREATE DATABASE IF NOT EXISTS `crawler` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `crawler`;

DROP TABLE IF EXISTS noticias_g1;
CREATE TABLE noticias_g1 (
  id int NOT NULL AUTO_INCREMENT,
  titulo varchar(300) NOT NULL,
  subtitulo varchar(300) NOT NULL,
  datahora varchar(100),
  autor varchar(300) NOT NULL,
  texto TEXT,
  link varchar(1000) NOT NULL,
  legendas_imagens varchar(1000) NOT NULL,
  links_imagens TEXT NOT NULL,
  primary key (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

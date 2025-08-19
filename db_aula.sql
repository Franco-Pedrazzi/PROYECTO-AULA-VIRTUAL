DROP DATABASE IF EXISTS aula;
CREATE DATABASE aula;
USE aula;
		
CREATE TABLE `cursos` (
  `id_curso` int AUTO_INCREMENT,
  `nombre` VARCHAR(10) NULL DEFAULT '-',
   PRIMARY KEY (`id_equipo`)
);

CREATE TABLE `posts` (
  `id_post` int AUTO_INCREMENT,
  `id_curso` int NULL DEFAULT NULL,
  `titulo` VARCHAR(100) NULL DEFAULT '-',
  `contenido` TEXT NULL DEFAULT NULL,
  `autor` VARCHAR(50) NULL DEFAULT '-',
  `fecha_publicacion` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_post`)
  FOREIGN KEY (`id_curso`) REFERENCES `cursos`(`id_curso`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`autor`) REFERENCES `usuario`(`email`) ON DELETE SET NULL ON UPDATE CASCADE

);

CREATE TABLE `entrega` (
  `id_entrega` int AUTO_INCREMENT,
  `id_post` int NULL DEFAULT NULL,
  `autor` VARCHAR(50) NULL DEFAULT '-',
  `fecha_entrega` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_entrega`),
  FOREIGN KEY (`id_post`) REFERENCES `posts`(`id_post`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`autor`) REFERENCES `usuario`(`email`) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE `archivos` (
    `id_archivo` INT AUTO_INCREMENT PRIMARY KEY,
    `id_post` INT NULL,
    `id_entrega` INT NULL,
    `ruta_archivo` VARCHAR(255) NOT NULL,
    FOREIGN KEY (`id_post`) REFERENCES `posts`(`id_post`) ON DELETE CASCADE
    FOREIGN KEY (`id_entrega`) REFERENCES `entrega`(`id_entrega`) ON DELETE CASCADE
);

CREATE TABLE `comentario` (
  `id_comentario` int AUTO_INCREMENT,
  `id_post` int NULL DEFAULT NULL,
  `autor` VARCHAR(50) NULL DEFAULT '-',
  `contenido` TEXT NULL DEFAULT NULL,
  `fecha_comentario` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_comentario`),
  FOREIGN KEY (`id_post`) REFERENCES `posts`(`id_post`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`autor`) REFERENCES `usuario`(`email`) ON DELETE SET NULL ON UPDATE CASCADE
);

		
CREATE TABLE `usuario` (
  `nombre` VARCHAR(40) not NULL,
  `email` VARCHAR(40) not NULL,
  `contraseña` VARCHAR(200) not NULL,
  `rango`  VARCHAR(20) NULL DEFAULT NULL,
  PRIMARY KEY (`email`)
);


CREATE TABLE `verificacion` (
  `id` int not NULL auto_increment,
  `email` VARCHAR(40) not NULL,
  `codigo` VARCHAR(20) not NULL,
  `contra_codificada`  VARCHAR(200) not null,
  `nombre` VARCHAR(40) not NULL,
  `rango` VARCHAR(20) not NULL,
  PRIMARY KEY (`id`)
);
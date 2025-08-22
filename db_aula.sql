DROP DATABASE IF EXISTS aula;
CREATE DATABASE aula;
USE aula;

CREATE TABLE `usuario` (
  `nombre` VARCHAR(40) NOT NULL,
  `email` VARCHAR(40) NOT NULL,
  `contraseña` VARCHAR(200) NOT NULL,
  `rango`  VARCHAR(20) NULL DEFAULT NULL,
  PRIMARY KEY (`email`)
);

CREATE TABLE `cursos` (
  `id_curso` INT AUTO_INCREMENT,
  `nombre` VARCHAR(50) NULL DEFAULT '-',
  PRIMARY KEY (`id_curso`)
);

CREATE TABLE `posts` (
  `id_post` INT AUTO_INCREMENT,
  `id_curso` INT NULL,
  `titulo` VARCHAR(100) NULL DEFAULT '-',
  `contenido` TEXT NULL,
  `autor` VARCHAR(40) NULL,
  `fecha_publicacion` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_post`),
  FOREIGN KEY (`id_curso`) REFERENCES `cursos`(`id_curso`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`autor`) REFERENCES `usuario`(`email`) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE `entrega` (
  `id_entrega` INT AUTO_INCREMENT,
  `id_post` INT NULL,
  `autor` VARCHAR(40) NULL,
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
  FOREIGN KEY (`id_post`) REFERENCES `posts`(`id_post`) ON DELETE CASCADE,
  FOREIGN KEY (`id_entrega`) REFERENCES `entrega`(`id_entrega`) ON DELETE CASCADE
);

CREATE TABLE `comentario` (
  `id_comentario` INT AUTO_INCREMENT,
  `id_post` INT NULL,
  `autor` VARCHAR(40) NULL,
  `contenido` TEXT NULL,
  `fecha_comentario` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_comentario`),
  FOREIGN KEY (`id_post`) REFERENCES `posts`(`id_post`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`autor`) REFERENCES `usuario`(`email`) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE `verificacion` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(40) NOT NULL,
  `codigo` VARCHAR(20) NOT NULL,
  `contra_codificada` VARCHAR(200) NOT NULL,
  `nombre` VARCHAR(40) NOT NULL,
  `rango` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`id`)
);



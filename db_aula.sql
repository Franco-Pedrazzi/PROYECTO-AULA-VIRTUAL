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
  `codigo` VARCHAR(20),
  `nombre` VARCHAR(50) NULL DEFAULT '-',
  PRIMARY KEY (`codigo`)
);

CREATE TABLE `cursos_usuarios` (
  `id_conexion` INT AUTO_INCREMENT PRIMARY key,
  `codigo` VARCHAR(20) NULL,
   `email` VARCHAR(40) NULL,
  FOREIGN KEY (`codigo`) REFERENCES `cursos`(`codigo`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`email`) REFERENCES `usuario`(`email`) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE `posts` (
  `id_post` INT AUTO_INCREMENT,
  `codigo` VARCHAR(20) NULL,
  `titulo` VARCHAR(100) NULL DEFAULT '-',
  `contenido` TEXT NULL,
  `autor` VARCHAR(40) NULL,
  `fecha_publicacion` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_post`),
  FOREIGN KEY (`codigo`) REFERENCES `cursos`(`codigo`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`autor`) REFERENCES `usuario`(`email`) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE `Tarea` (
  `id_tarea` INT AUTO_INCREMENT,
  `codigo` VARCHAR(20) NULL,
  `titulo` VARCHAR(100) NULL DEFAULT '-',
  `contenido` TEXT NULL,
  `autor` VARCHAR(40) NULL,
  `fecha_publicacion` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_tarea`),
  FOREIGN KEY (`id_post`) REFERENCES `posts`(`id_post`) ON DELETE CASCADE,
  FOREIGN KEY (`codigo`) REFERENCES `cursos`(`codigo`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`autor`) REFERENCES `usuario`(`email`) ON DELETE SET NULL ON UPDATE CASCADE
);


CREATE TABLE `entrega` (
  `id_entrega` INT AUTO_INCREMENT,
  `id_tarea` INT NULL,
  `autor` VARCHAR(40) NULL,
  `fecha_entrega` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_entrega`),
  FOREIGN KEY (`id_tarea`) REFERENCES `Tarea`(`id_tarea`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`autor`) REFERENCES `usuario`(`email`) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE `archivos` (
  `id_archivo` INT AUTO_INCREMENT PRIMARY KEY,
  `id_post` INT NULL,
  `id_entrega` INT NULL,
  `tipo` VARCHAR(50),
  `tamano` BIGINT,
  `pixel` LONGBLOB,
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



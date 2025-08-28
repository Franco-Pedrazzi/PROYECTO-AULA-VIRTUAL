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

CREATE TABLE `cursos_usuarios` (
  `id_conexion` INT AUTO_INCREMENT PRIMARY key,
  `id_curso` INT NULL,
   `email` VARCHAR(40) NULL,
  FOREIGN KEY (`id_curso`) REFERENCES `cursos`(`id_curso`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`email`) REFERENCES `usuario`(`email`) ON DELETE SET NULL ON UPDATE CASCADE
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
  `tipo` VARCHAR(50),
  `tamano` BIGINT,
  `pixel` MEDIUMBLOB,
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

INSERT INTO usuario (nombre, email, contraseña, rango) VALUES
("Juan Pérez", "juan@example.com", "hash123", "alumno"),
('as', 'yuro2105@gmail.com', 'scrypt:32768:8:1$oLk5Wj771FNxoARs$dfa4cf846cdb225338b6de3013696c7cb5a694e9f6217ae10dc0c2a3c54d6ea6e8e7b281ef977161d95bff79bd18448ce076430500d628c808f941794834d625', 'Profe'),
('er', 'd48457362@alumnos.itr.edu.ar', 'scrypt:32768:8:1$Yu9uwpuSO93DECfb$dcc46ad60c57bd0f0526f81f1af234d6d9f5c6b556532b3f60de32aa8a6b71197a5b5b88a61a6bd4ea00b86420fc1082a4d796da35a3a84c61e228baac43e14e', 'A');

-- Cursos (ya insertaste algunos, agrego más)
INSERT INTO cursos (nombre) VALUES
("Matemáticas"),
("Historia"),
("Programación");

-- Posts (referencian cursos y usuarios)
INSERT INTO posts (id_curso, titulo, contenido, autor) VALUES
(1, "Bienvenida al curso", "Este es el post de bienvenida.", "yuro2105@gmail.com"),
(2, "Guía de estudio", "Aquí encontrarás materiales de Historia.", "juan@example.com"),
(3, "Ejercicios de práctica", "Resolver los siguientes problemas de código.", "d48457362@alumnos.itr.edu.ar");

-- Entregas (referencian posts y usuarios)
INSERT INTO entrega (id_post, autor) VALUES
(2, "juan@example.com"),
(3, "d48457362@alumnos.itr.edu.ar"),
(3, "juan@example.com");



-- Comentarios (referencian posts y usuarios)
INSERT INTO comentario (id_post, autor, contenido) VALUES
(1, "juan@example.com", "Gracias por la bienvenida!"),
(2, "yuro2105@gmail.com", "Buen aporte, Juan."),
(3, "juan@example.com", "Tengo dudas con el ejercicio 2.");



INSERT INTO cursos_usuarios (id_curso, email) VALUES
(2,"yuro2105@gmail.com"),
(1,"yuro2105@gmail.com"),
(1,"d48457362@alumnos.itr.edu.ar");

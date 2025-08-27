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

INSERT INTO usuario (nombre, email, contraseña, rango) VALUES
("Juan Pérez", "juan@example.com", "hash123", "alumno"),
("María Gómez", "maria@example.com", "hash456", "profesor"),
("Carlos Ruiz", "carlos@example.com", "hash789", "alumno");

-- Cursos (ya insertaste algunos, agrego más)
INSERT INTO cursos (nombre) VALUES
("Matemáticas"),
("Historia"),
("Programación");

-- Posts (referencian cursos y usuarios)
INSERT INTO posts (id_curso, titulo, contenido, autor) VALUES
(1, "Bienvenida al curso", "Este es el post de bienvenida.", "maria@example.com"),
(2, "Guía de estudio", "Aquí encontrarás materiales de Historia.", "juan@example.com"),
(3, "Ejercicios de práctica", "Resolver los siguientes problemas de código.", "carlos@example.com");

-- Entregas (referencian posts y usuarios)
INSERT INTO entrega (id_post, autor) VALUES
(2, "juan@example.com"),
(3, "carlos@example.com"),
(3, "juan@example.com");

-- Archivos (pueden estar ligados a posts o entregas)
INSERT INTO archivos (id_post, ruta_archivo) VALUES
(1, "/archivos/intro.pdf"),
(2, "/archivos/guia_historia.docx");

INSERT INTO archivos (id_entrega, ruta_archivo) VALUES
(1, "/archivos/tarea_historia_juan.pdf"),
(2, "/archivos/ejercicio_codigo_carlos.zip");

-- Comentarios (referencian posts y usuarios)
INSERT INTO comentario (id_post, autor, contenido) VALUES
(1, "juan@example.com", "Gracias por la bienvenida!"),
(2, "maria@example.com", "Buen aporte, Juan."),
(3, "juan@example.com", "Tengo dudas con el ejercicio 2.");

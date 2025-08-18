DROP database IF EXISTS Aula;
create database Aula;
use Aula;
DROP TABLE IF EXISTS `Equipo`;
		
CREATE TABLE `Cursos` (
  `id_curso` int AUTO_INCREMENT,
  `nombre` VARCHAR(10) NULL DEFAULT '-',
   PRIMARY KEY (`id_equipo`)
);

CREATE TABLE `jugador` (
  `id_jugador` int AUTO_INCREMENT,
  `id_equipo` int NULL DEFAULT NULL,
  `Nombre` VARCHAR(50) NULL DEFAULT '-',
  `DNI` Varchar(10) NULL DEFAULT NULL,
  `Telefono` Varchar(15) NULL DEFAULT NULL,
  `Email` VARCHAR(40) NULL DEFAULT NULL,
  `Comida_especial` VARCHAR(3) NULL DEFAULT 'N',
  `Fecha_nacimiento` DATE NULL DEFAULT NULL,
  `Infracciones` VARCHAR(10) NULL DEFAULT '0',
  PRIMARY KEY (`id_jugador`)
);
		

		

		
CREATE TABLE `Cuenta_habilitada` (
  `Nombre` VARCHAR(40) not NULL,
  `Email` VARCHAR(40) not NULL,
  `Contraseña` VARCHAR(200) not NULL,
  `rango`  VARCHAR(20) NULL DEFAULT NULL,
  PRIMARY KEY (`Email`)
);


CREATE TABLE `Verificacion` (
  `id` int not NULL auto_increment,
  `Email` VARCHAR(40) not NULL,
  `codigo` VARCHAR(20) not NULL,
  `contra_codificada`  VARCHAR(200) not null,
  `nombre` VARCHAR(40) not NULL,
  `rango` VARCHAR(20) not NULL,
  PRIMARY KEY (`id`)
);

-- ---
-- Table Properties
-- ---

-- ALTER TABLE `Equipo` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `jugador` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `Responsable` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `Partido` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `Resultado` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `Cuenta_habilitada` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `Staff` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ---
-- Test Data
-- ---

-- INSERT INTO `Equipo` (`id_equipo`,`Deporte`,`Categoria`,`Sexo`,`Colegio`) VALUES
-- ('','','','','');
-- INSERT INTO `jugador` (`id_jugador`,`id_equipo`,`Nombre`,`DNI`,`Telefono`,`Email`,`Comida_especial`,`Fecha_nacimiento`,`Infracciones`) VALUES
-- ('','','','','','','','','');
-- INSERT INTO `Responsable` (`id_profesor`,`id_equipo`,`Nombre`,`DNI`,`Telefono`,`Email`,`Comida_especial`) VALUES
-- ('','','','','','','');
-- INSERT INTO `Partido` (`id_partido`,`Deporte`,`Categoria`,`Sexo`,`id_staff`,`Planillero`,`Equipo_1`,`Equipo_2`,`Fase`,`Horario_inicio`,`Horario_final`) VALUES
-- ('','','','','','','','','','','');
-- INSERT INTO `Resultado` (`id_partido`,`Puntaje_e1`,`Puntaje_e2`,`Resultado`,`Infracciones_e1`,`Infracciones_e2`) VALUES
-- ('','','','','','');
-- INSERT INTO `Cuenta_habilitada` (`id_cuenta`,`Nombre`,`Email`,`Contraseña`) VALUES
-- ('','','','');
-- INSERT INTO `Staff` (`id_staff`,`Nombre`,`DNI`,`Telefono`,`Email`,`Trabajo`,`Sector`) VALUES
-- ('','','','','','','');


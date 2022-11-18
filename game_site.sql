-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema game_site
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `game_site` ;

-- -----------------------------------------------------
-- Schema game_site
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `game_site` DEFAULT CHARACTER SET utf8 ;
USE `game_site` ;

-- -----------------------------------------------------
-- Table `game_site`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `game_site`.`users` ;

CREATE TABLE IF NOT EXISTS `game_site`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `email` VARCHAR(100) NULL,
  `username` VARCHAR(45) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `game_site`.`games`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `game_site`.`games` ;

CREATE TABLE IF NOT EXISTS `game_site`.`games` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(100) NULL,
  `system` VARCHAR(45) NULL,
  `location` VARCHAR(100) NULL,
  `date` DATE NULL,
  `max_players` INT NULL,
  `description` TEXT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_games_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_games_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `game_site`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `game_site`.`players`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `game_site`.`players` ;

CREATE TABLE IF NOT EXISTS `game_site`.`players` (
  `user_id` INT NOT NULL,
  `game_id` INT NOT NULL,
  INDEX `fk_users_games_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_users_games_games1_idx` (`game_id` ASC) VISIBLE,
  CONSTRAINT `fk_users_games_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `game_site`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_games_games1`
    FOREIGN KEY (`game_id`)
    REFERENCES `game_site`.`games` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

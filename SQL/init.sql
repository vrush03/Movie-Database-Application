
--database

drop movieapp;
create database movieapp;

--User table

CREATE TABLE `movieapp`.`User` (
`UserId` BIGINT NULL AUTO_INCREMENT,
`UserName` VARCHAR(255) NULL,
`Useremail` VARCHAR(255) NULL,
`UserPassword` VARCHAR(255) NULL,
PRIMARY KEY (`UserId`));

--select database

use movieapp;

--User storedprocedure

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
    IN p_name VARCHAR(255),
    IN p_email VARCHAR(255),
    IN p_password VARCHAR(255)
)
BEGIN
    if ( select exists (select 1 from User where Useremail = p_email) ) THEN

        select 'User Exists !!';

    ELSE

        insert into User
        (
            UserName,
            Useremail,
            UserPassword
        )
        values
        (
            p_name,
            p_email,
            p_password
        );

    END IF;
END$$
DELIMITER ;

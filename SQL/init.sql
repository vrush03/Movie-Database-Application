
--database

drop database movieapp;
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

--User signin check

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_validateLogin`(
IN p_useremail VARCHAR(255)
)
BEGIN
    select * from User where Useremail = p_useremail;
END$$
DELIMITER ;

--Movie

CREATE TABLE Movie (
	MovieID INT AUTO_INCREMENT,
	Title VARCHAR(100) NOT NULL,
	ReleaseYear INT,
	Rating VARCHAR(3),
	Synopsis VARCHAR(100),
	MovieLength VARCHAR(5),
	GenreName VARCHAR(100),
    Image LONGBLOB  NULL,
    PRIMARY KEY(MovieID)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

CREATE TABLE Director (
	DirectorID INT AUTO_INCREMENT PRIMARY KEY,
	FirstName VARCHAR(10),
	LastName VARCHAR(10),
	Nationality VARCHAR(10),
	BirthPlace VARCHAR(20)
)ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

CREATE TABLE Actor (
	ActorID INT AUTO_INCREMENT PRIMARY KEY,
	FirstName VARCHAR(10),
	LastName VARCHAR(10),
	Nationality VARCHAR(10),
	BirthPlace VARCHAR(20)
)ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

CREATE TABLE MovieActor (
	ActorID INT ,
	MovieID INT,
	FOREIGN KEY(ActorID) REFERENCES Actor(ActorID),
	FOREIGN KEY(MovieID) REFERENCES Movie(MovieID)
	ON DELETE CASCADE
);

CREATE TABLE DirectedBy (
	DirectorID INT,
	MovieID INT,
	FOREIGN KEY(DirectorID) REFERENCES Director(DirectorID),
	FOREIGN KEY(MovieID) REFERENCES Movie(MovieID)
	ON DELETE CASCADE
);

--Add movie

DELIMITER $$
DROP procedure IF EXISTS `sp_addMovie`;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_addMovie`(
    IN p_title varchar(100),
    IN p_releaseyear INT,
    IN p_rating varchar(3),
    IN p_synopsis varchar(100),
    IN p_movielength VARCHAR(5),
    IN p_genrename VARCHAR(100)
)
BEGIN
    insert into Movie (
        Title,
        ReleaseYear,
        Rating,
	Synopsis,
	MovieLength,
	GenreName,
    Image
    )
    values
    (
        p_title,
    	p_releaseyear,
        p_rating,
        p_synopsis,
        p_movielength,
        p_genrename,
        NULL
    );
END$$
DELIMITER ;
;

--Add director
DROP procedure IF EXISTS `sp_addDirector`;
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_addDirector`(
    IN p_firstname varchar(10),
    IN p_lastname varchar(10),
    IN p_nationality VARCHAR(10),
    IN p_birthplace varchar(100)
)
BEGIN
    IF (SELECT count(*) FROM Director
	WHERE FirstName = p_firstname AND LastName = p_lastname
) <= 0 THEN
    insert into Director (
        FirstName,
	LastName,
	Nationality,
	BirthPlace
    )
    values
    (
        p_firstname,
    	p_lastname,
        p_nationality,
        p_birthplace
    );
     END IF;
END$$

DELIMITER ;
;

--Add director name
DROP procedure IF EXISTS `sp_addDirectorName`;
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_addDirectorName`(
    IN p_firstname varchar(10),
    IN p_lastname varchar(10)
)
BEGIN
    IF (SELECT count(*) FROM Director
	WHERE FirstName = p_firstname AND LastName = p_lastname
) <= 0 THEN
    insert into Director (
        FirstName,
	LastName,
	Nationality,
	BirthPlace
    )
    values
    (
        p_firstname,
    	p_lastname,
        null,
        null
    );
     END IF;
END$$

DELIMITER ;
;

--Add Actor
DROP procedure IF EXISTS `sp_addActor`;
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_addActor`(
    IN p_firstname varchar(10),
    IN p_lastname varchar(10),
    IN p_nationality VARCHAR(10),
    IN p_birthplace varchar(100)
)
BEGIN
    IF (SELECT count(*) FROM Actor
	WHERE FirstName = p_firstname AND LastName = p_lastname
) <= 0 THEN
    insert into Actor (
        FirstName,
	LastName,
	Nationality,
	BirthPlace
    )
    values
    (
        p_firstname,
    	p_lastname,
        p_nationality,
        p_birthplace
    );
     END IF;
END$$

DELIMITER ;
;

--Add actor name
DROP procedure IF EXISTS `sp_addActorName`;
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_addActorName`(
    IN p_firstname varchar(10),
    IN p_lastname varchar(10)
)
BEGIN
    IF (SELECT count(*) FROM Actor
	WHERE FirstName = p_firstname AND LastName = p_lastname
) <= 0 THEN
    insert into Actor (
        FirstName,
	LastName,
	Nationality,
	BirthPlace
    )
    values
    (
        p_firstname,
    	p_lastname,
        null,
        null
    );
     END IF;
END$$

DELIMITER ;
;

--Add MovieActor
DROP procedure IF EXISTS `sp_addMovieActor`;
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_addMovieActor`(
    IN p_actorid int,
    IN p_movieid int
)
BEGIN

    insert into MovieActor (
        ActorID,
	MovieID
    )
    values
    (
        p_actorid,
    	p_movieid
    );
END$$

DELIMITER ;
;

--Add DirectedBy
DROP procedure IF EXISTS `sp_addDirectedBy`;
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_addDirectedBy`(
    IN p_directorid int,
    IN p_movieid int
)
BEGIN

    insert into DirectedBy (
        DirectorID,
	MovieID
    )
    values
    (
        p_directorid,
    	p_movieid
    );
END$$

DELIMITER ;
;

-- Get Director associated with a movie;
SELECT firstname, lastname FROM Movie NATURAL JOIN DirectedBy, Director WHERE Director.DirectorID = DirectedBy.DirectorID and MovieID = 48;

-- Get Actor associated with a movie.
 SELECT firstname, lastname FROM Movie NATURAL JOIN MovieActor, Actor WHERE Actor.ActorID = MovieActor.ActorID and MovieID = 51;

 -- Review table

CREATE TABLE Review (
    ReviewID INT AUTO_INCREMENT PRIMARY KEY,
    MovieID INT,
    UserID BIGINT,
    Review VARCHAR(100),
    ReviewDate DATE,
    FOREIGN KEY(MovieID) REFERENCES Movie(MovieID)
    ON DELETE CASCADE,
    FOREIGN KEY(UserID) REFERENCES User(UserID)
    ON DELETE CASCADE
)ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

-- Add Review
DROP procedure IF EXISTS `sp_addReview`;
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_addReview`(
    IN p_movieid int,
    IN p_userid bigint,
    IN p_review varchar(100)
)
BEGIN

    insert into Review (
        MovieID,
        UserID,
        Review,
        ReviewDate
    )
    values
    (
    	p_movieid,
        p_userid,
        p_review,
        NOW()
    );
END$$

DELIMITER ;
;


--To add Images
update Movie set Image="/static/Images/<Image_name>" where MovieID=ID;--Change MovieID and Url Accordingly

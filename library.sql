DROP table IF EXISTS library;

CREATE TABLE library
(
 book_id INT AUTO_INCREMENT, 
 book_name varchar(50),
 author varchar(50),
 written char(4),
 book_language varchar(20),
 images	varchar(70),
 book_link varchar(70),
 PRIMARY KEY (book_id)
 
 );
   

INSERT INTO library
VALUES

("1","A Christmas Carol", "Charles Dickens", "1843", "english", "images/a_christmas_carol.jpg", "library/a_christmas_carol.txt"),
("2","A Portrait of the Artist as a Young Man", "James Joyce", "1916", "english", "images/a_portrait_of_the_artist_as_a_young_man.jpg", "library/a_portrait_of_the_artist_as_a_young_man.txt"),
("3","An American Tragedy", "Theodore Dreiser", "1925", "English", "images/an_american_tragedy.jpg", "library/an_american_tragedy.txt"),
("4", "Gullivers travels", "Jonathan Swift", "1726", "English", "images/gullivers_travels.jpg", "library/gullivers_travels.txt"),
("5", "Poems by Lord Byron", "Lord Byron", "1726", "English", "images/poems_by_lord_byron.jpg",	"library/poems_by_lord_byron.txt"),
("6","The Complete Work of William Shakespear", "William Shakespear", "1609", "English", "images/the_complete_works_of_william_shakespear.jpg", "library/the_complete_works_of_william_shakespear.txt"),
("7", "The Life and Adventures of Robinson Crusoe", "Daniel Defoe", "1719", "English", "images/the_life_and_adventures_of_robinson_crusoe.jpg", "library/the_life_and_adventures_of_robinson_crusoe.txt"),
("8","The Luncheon", "William Somerset Maugham", "1924", "english", "images/the_luncheon.jpg", "library/the_luncheon.txt"),
("9","Vanity Fair", "William Makepeace Thackeray", "1848", "english", "images/vanity_fair.jpg", "library/vanity_fair.txt");


CREATE TABLE comments_table
(
    comment_id INT AUTO_INCREMENT,
    username VARCHAR(255),
    comment TEXT,
    PRIMARY KEY (comment_id)
  
 );
 
 DROP TABLE If EXISTS users;

CREATE TABLE users
(
    username VARCHAR(255),
    password VARCHAR(255),
    PRIMARY KEY (username)
  
 );

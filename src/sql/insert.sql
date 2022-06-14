-- publishers
INSERT INTO publishers(publisher_id,name) values (1,'O Reilly Media');
INSERT INTO publishers(publisher_id,name) values (2,'A Book Apart');
INSERT INTO publishers(publisher_id,name) values (3,'A K PETERS');
INSERT INTO publishers(publisher_id,name) values (4,'Academic Press');
INSERT INTO publishers(publisher_id,name) values (5,'Addison Wesley');
INSERT INTO publishers(publisher_id,name) values (6,'Albert&Sweigart');
INSERT INTO publishers(publisher_id,name) values (7,'Alfred A. Knopf');

-- authors 
INSERT INTO authors (author_id, first_name, middle_name, last_name) VALUES (1,'Merritt',null,'Eric');
INSERT INTO authors (author_id, first_name, middle_name, last_name) VALUES (2,'Linda',null,'Mui');
INSERT INTO authors (author_id, first_name, middle_name, last_name) VALUES (3,'Alecos',null,'Papadatos');
INSERT INTO authors (author_id, first_name, middle_name, last_name) VALUES (4,'Anthony','Molinaro');
INSERT INTO authors (author_id, first_name, middle_name, last_name) VALUES (5,'David',null,'Cronin');
INSERT INTO authors (author_id, first_name, middle_name, last_name) VALUES (6,'Richard',null,'Blum');
INSERT INTO authors (author_id, first_name, middle_name, last_name) VALUES (7,'Yuval','Noah','Harari');
INSERT INTO authors (author_id, first_name, middle_name, last_name) VALUES (8,'Paul',null,'Albitz');


-- books
insert into books (book_id,title,total_pages,rating,isbn,published_date,publisher_id) values (1,'Lean Software Development: An Agile Toolkit',240,4.17,'9780320000000','2003-05-18',5);
insert into books (book_id,title,total_pages,rating,isbn,published_date,publisher_id) values (2,'Facing the Intelligence Explosion',91,3.87,null,'2013-02-01',7);
insert into books (book_id,title,total_pages,rating,isbn,published_date,publisher_id) values (3,'Scala in Action',419,3.74,'9781940000000','2013-04-10',1);
insert into books (book_id,title,total_pages,rating,isbn,published_date,publisher_id) values (4,'Patterns of Software: Tales from the Software Community',256,3.84,'9780200000000','1996-08-15',1);
insert into books (book_id,title,total_pages,rating,isbn,published_date,publisher_id) values (5,'Anatomy Of LISP',446,4.43,'9780070000000','1978-01-01',3);
insert into books (book_id,title,total_pages,rating,isbn,published_date,publisher_id) values (6,'Computing machinery and intelligence',24,4.17,null,'2009-03-22',4);
insert into books (book_id,title,total_pages,rating,isbn,published_date,publisher_id) values (7,'XML: Visual QuickStart Guide',269,3.66,'9780320000000','2009-01-01',5);
insert into books (book_id,title,total_pages,rating,isbn,published_date,publisher_id) values (8,'SQL Cookbook',595,3.95,'9780600000000','2005-12-01',7);
insert into books (book_id,title,total_pages,rating,isbn,published_date,publisher_id) values (9,'The Apollo Guidance Computer: Architecture And Operation (Springer Praxis Books / Space Exploration)',439,4.29,'9781440000000','2010-07-01',6);
insert into books (book_id,title,total_pages,rating,isbn,published_date,publisher_id) values (10,'Minds and Computers: An Introduction to the Philosophy of Artificial Intelligence',222,3.54,'9780750000000','2007-02-13',7);

-- book authors

INSERT INTO book_authors (book_id, author_id) values (8,4);
INSERT INTO book_authors (book_id, author_id) values (8,4);
INSERT INTO book_authors (book_id, author_id) values (8,4);
INSERT INTO book_authors (book_id, author_id) values (8,4);



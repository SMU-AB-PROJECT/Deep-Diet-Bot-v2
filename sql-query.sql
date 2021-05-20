-- mysql 처음 생성시
CREATE DATABASE study_db

USE db_diet;
CREATE TABLE history(
    id INT(11) NOT NULL AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL,
    userdate DATETIME NOT NULL,
    breakfast VARCHAR(30) NULL,
    lunch VARCHAR(100) NULL,
    dinner VARCHAR(100) NULL,
    PRIMARY KEY(id)
);

-- 데이터 삽입
INSERT INTO `history` (username, userdate, breakfast, lunch, dinner)
VALUES ('테스트', '2021-05-20', '샌드위치', '햄버거', '피자');
-- 데이터 수정
UPDATE history SET lunch='마이쮸' WHERE username = '테스트4' AND userdate = '2021-05-20';
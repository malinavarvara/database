import sqlite3

with sqlite3.connect("database.db") as db:
    cursor = db.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXIST users(
        user_id integer PRIMARY KEY AUTO_INCREMENT,
        username varchar(30),
        user_image varchar(50),
        description varchar(100),
        n_followers integer not null default 0
    );
    CREATE TABLE IF NOT EXIST links (
        id integer PRIMARY KEY AUTO_INCREMENT,
        user_id INTEGER,
        link_type_id INTEGER,
        url VARCHAR(50),
        FOREIGN KEY (link_type_id)  REFERENCES link_type (link_type_id),
        FOREIGN KEY (user_id)  REFERENCES user (user_id)
    );
    CREATE TABLE IF NOT EXIST link_type (
        link_type_id integer PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(20)
    );
    CREATE TABLE IF NOT EXIST posts (
        id integer PRIMARY KEY AUTO_INCREMENT,
        user_id integer,
        title VARCHAR(20),
        content text,
        n_likes INTEGER not null default 0,
        FOREIGN KEY (user_id)  REFERENCES user (user_id)

    );
    CREATE TABLE IF NOT EXIST comments (
        id integer PRIMARY KEY AUTO_INCREMENT,
        post_id integer,
        user_create_id integer,
        mother_comment_id integer,
        content text,
        n_likes INTEGER not null default 0,
        FOREIGN KEY (user_id)  REFERENCES user (user_id)
    );
    """)
import sqlite3
def DZEN_db_create():
    with sqlite3.connect("database.db") as db:
        cursor = db.cursor()

        cursor.executescript("""CREATE TABLE IF NOT EXISTS user(
            user_id integer PRIMARY KEY AUTOINCREMENT,
            username varchar,
            user_url varchar,
            user_image varchar,
            description varchar,
            n_followers integer not null default 0,
            flag_is_parsed bool not null default False
        );
        CREATE TABLE IF NOT EXISTS links (
            id integer PRIMARY KEY,
            user_id INTEGER,
            link_type_id INTEGER,
            url VARCHAR(50),
            FOREIGN KEY (link_type_id)  REFERENCES link_type (link_type_id),
            FOREIGN KEY (user_id)  REFERENCES user (user_id)
        );
        CREATE TABLE IF NOT EXISTS link_type (
            link_type_id integer PRIMARY KEY,
            name VARCHAR(20)
        );
        CREATE TABLE IF NOT EXISTS posts (
            id integer PRIMARY KEY AUTOINCREMENT,
            user_id integer,
            n_likes INTEGER not null default 0,
            n_comments INTEGER not null default 0,
            url_post varchar,
            type_id integer,
            FOREIGN KEY (user_id) REFERENCES user (user_id),
            FOREIGN KEY (type_id) REFERENCES post_type (type_id)
        );
        CREATE TABLE IF NOT EXISTS  comments (
            id integer PRIMARY KEY AUTOINCREMENT,
            post_id integer,
            user_create_id integer,
            content text,
            n_likes INTEGER not null default 0,
            FOREIGN KEY (post_id)  REFERENCES posts (id)
        );
        CREATE TABLE IF NOT EXISTS post_type (
            type_id integer PRIMARY KEY AUTOINCREMENT,
            name VARCHAR
        );
        INSERT INTO post_type (name) VALUES ('Статья');
        INSERT INTO post_type (name) VALUES ('Пост');
        INSERT INTO post_type (name) VALUES ('Видео');
        """)

def insert_user(username, user_url, user_image, description, n_followers, flag):
    with sqlite3.connect("database.db") as db:
        cursor = db.cursor()
        cursor.execute("""INSERT INTO 
        user (username, user_url, user_image, description, n_followers, flag_is_parsed) 
        VALUES (?,?,?,?,?,?);""", (username, user_url, user_image, description, n_followers, flag))
        db.commit()

def insert_post(user_url, n_likes, n_comments, url_post, type_txt):
    with sqlite3.connect("database.db") as db:
        cursor = db.cursor()
        cursor.execute("""INSERT INTO 
        posts (user_id, n_likes, n_comments, url_post, type_id) 
        VALUES (
        (SELECT user.user_id FROM user WHERE user.user_url = ?)
        ,?,?,?,
        (SELECT post_type.type_id FROM post_type WHERE post_type.name = ?));""",
                       (user_url, n_likes, n_comments, url_post, type_txt))
        db.commit()

def insert_comments(url_post, url_create, content, n_likes):
    with sqlite3.connect("database.db") as db:
        cursor = db.cursor()
        cursor.execute("""INSERT INTO 
        comments (post_id, user_create_id, content, n_likes) 
        VALUES (
        (SELECT posts.id FROM posts WHERE posts.url_post = ?),
        (SELECT user.user_id FROM user WHERE user.user_url = ?),
        ?,?);""", (url_post, url_create, content, n_likes))
        db.commit()

def delete_repeat():
    with sqlite3.connect("database.db") as db:
        cursor = db.cursor()
        cursor.execute("""DELETE FROM user 
        where user_id NOT IN (
        SELECT MIN(user_id) 
        FROM user 
        GROUP BY user_url)""")
        db.commit()

if __name__ == '__main__':
    DZEN_db_create()
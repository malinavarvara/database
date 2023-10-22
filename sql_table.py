import sqlite3

with sqlite3.connect("database.db") as db:
    cursor = db.cursor()

    cursor.executescript("""CREATE TABLE IF NOT EXISTS user(
        user_id integer PRIMARY KEY AUTOINCREMENT,
        username varchar,
        user_url varchar,
        user_image varchar,
        description varchar,
        n_followers integer not null default 0
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
        FOREIGN KEY (user_id) REFERENCES user (user_id)
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
        name VARCHAR(20)
    );
    CREATE TABLE IF NOT EXISTS media_type (
        type_id integer PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(20)
    );
    """)

def insert_user(username, user_url, user_image, description, n_followers):
    cursor.execute("""INSERT INTO 
    user (username, user_url, user_image, description, n_followers) 
    VALUES (?,?,?,?,?);""", (username, user_url, user_image, description, n_followers))
    db.commit()

def insert_post(user_url, n_likes, n_comments, url_post):
    cursor.execute("""INSERT INTO 
    posts (user_id, n_likes, n_comments, url_post) 
    VALUES (
    (SELECT user.user_id FROM user WHERE user.user_url = ?)
    ,?,?,?);""", (user_url, n_likes, n_comments, url_post))
    db.commit()

def insert_comments(post_id, user_create_id, content, n_likes):
    cursor.execute("""INSERT INTO 
    posts (post_id, user_create_id, content, n_likes) 
    VALUES (
    (SELECT user.user_id FROM user WHERE user.user_url = ?)
    ,?,?);""", (post_id, user_create_id, content, n_likes))
    db.commit()

def delete_repeat():
    cursor.execute("""DELETE FROM user 
    where user_id NOT IN (
    SELECT MIN(user_id) 
    FROM user 
    GROUP BY user_url)""")
    db.commit()
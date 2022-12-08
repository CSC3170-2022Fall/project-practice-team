from schema import Game
import pickle
import mysql.connector

import re


game_pickle_file = '../../scrap/game.pickle'
pub_dict_file    = '../../scrap/dict/pub_dict.pickle'
dev_dict_file    = '../../scrap/dict/dev_dict.pickle'
cate_dict_file   = '../../scrap/dict/cate_dict.pickle'





with open(game_pickle_file, 'rb') as handler:
    res = pickle.load(handler)

with open(pub_dict_file, 'rb') as handler:
    pub_name2id = pickle.load(handler)
    
with open(dev_dict_file, 'rb') as handler:
    dev_name2id = pickle.load(handler)
    
with open(cate_dict_file, 'rb') as handler:
    cate_name2id = pickle.load(handler)


TABLES = {}
TABLES['game'] = (
    "CREATE TABLE IF NOT EXISTS `game` ("
    "   `ID`            int(7) not null,"
    "   `name`          varchar(70) not null,"
    "   `price`         numeric(5,2) not null,"
    "   `pub_id`        int(7) not null,"
    "   `release_date`  varchar(20) not null,"
    "   primary key (ID) )"
)

TABLES['consumer'] = (
    "CREATE TABLE `consumer` ("
    "`ID`       int(7) not null,"
    "`name`     varchar(70) not null,"
    "primary key (ID))"
)

TABLES['publisher'] = (
    "CREATE TABLE `publisher` ("
    "`ID`       int(7) not null,"
    "`name`     varchar(70) not null,"
    "primary key (ID))"
)


TABLES['developer'] = (
    "CREATE TABLE `developer` ("
    "`ID`       int(7) not null,"
    "`name`     varchar(70) not null,"
    "primary key (ID))"
)


TABLES['category'] = (
    "CREATE TABLE `category` ("
    "`ID`       int(7) not null,"
    "`name`     varchar(70) not null,"
    "primary key (ID))"
)

TABLES['web_section'] = (
    "CREATE TABLE `web_section` ("
    "`ID`           int(7) not null,"
    "`position`     int(2) not null,"
    "`price`        numeric(6,2) not null,"
    "primary key (ID))"
)


TABLES['develop'] = (
    "CREATE TABLE `develop` ("
    "`dev_id`   int(7) not null,"
    "`game_id`  int(7) not null,"
    "primary key (dev_id, game_id))"
)

TABLES['game_type'] = (
    "CREATE TABLE `game_type` ("
    "`game_id`    int(7) not null,"
    "`cate_id`    int(7) not null,"
    "primary key (game_id, cate_id))"
)



TABLES['prefer'] = (
    "CREATE TABLE `prefer` ("
    "`con_id`    int(7) not null,"
    "`cate_id`    int(7) not null,"
    "primary key (con_id, cate_id))"
)

TABLES['rate'] = (
    "CREATE TABLE `rate` ("
    "con_id     int(7) not null,"
    "game_id    int(7) not null,"
    "score      numeric(2,1) not null,"
    "primary key (con_id, game_id))"
)


TABLES['purchase'] = (
    "CREATE TABLE `purchase` ("
    "`con_id`     int(7) not null,"
    "`game_id`    int(7) not null,"
    "`date`       varchar(20) not null,"
    "primary key (con_id, game_id))"
)

TABLES['barter'] = (
    "CREATE TABLE `barter` ("
    "`con_id`     int(7) not null,"
    "`sell_id`    int(7) not null,"
    "`wish_id`    int(7) not null,"
    "primary key (con_id, sell_id, wish_id))"
)

TABLES['purchase'] = (
    "CREATE TABLE `purchase` ("
    "`con_id`     int(7) not null,"
    "`game_id`    int(7) not null,"
    "`date`       varchar(20) not null,"
    "primary key (con_id, game_id))"
)


TABLES['promote'] = (
    "CREATE TABLE `promote` ("
    "`pub_id`     int(7) not null,"
    "`sec_id`     int(7) not null,"
    "`game_id`    int(7) not null,"
    "primary key (pub_id, sec_id, game_id))"
)






db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'root',
    auth_plugin = 'mysql_native_password',
    port = 3306,
    database = 'AGDP'
)

cursor = db.cursor()

# initialize game table

cursor.execute("DROP TABLE IF EXISTS `game`;")
db.commit()
cursor.execute(TABLES["game"])

game_insert_template = (
    "INSERT INTO game (`ID`, `name`, `price`, `pub_id`, `release_date`) "
    "VALUES ("
    "'{0}',"
    "'{1}',"
    "'{2}',"
    "'{3}',"
    "'{4}');"
)

for game in res:
    script = game_insert_template.format(
        game.id,
        game.name if "'" not in game.name else game.name.replace("'", r"\'"),
        re.search(r'\$(\d*[.]\d*)', game.price).group(1),
        pub_name2id[game.publisher],
        game.release_date   
    )
    try:
        cursor.execute(script)
    except:
        print(script)
        break
    
db.commit()



# init publisher table

cursor.execute("DROP TABLE IF EXISTS `publisher`;")
db.commit()
cursor.execute(TABLES["publisher"])

pub_insert_template = (
    "INSERT INTO publisher (`ID`, `name`) "
    "VALUES ("
    "'{0}',"
    "'{1}')"
)
for (name, id) in pub_name2id.items():
    script = pub_insert_template.format(
        id,
        name.replace("'", r"\'")
    )
    cursor.execute(script)

db.commit()





# init developer table
cursor.execute('DROP TABLE IF EXISTS `developer`;')
db.commit()
cursor.execute(TABLES["developer"])


dev_insert_template = (
    "INSERT INTO developer (`ID`, `name`) "
    "VALUES ("
    "'{0}',"
    "'{1}')"
)

for (name, id) in dev_name2id.items():
    script = dev_insert_template.format(
        id,
        name.replace("'", r"\'")
    )

db.commit()


cursor.execute('DROP TABLE IF EXISTS `category`;')
db.commit()
cursor.execute(TABLES["category"])

cate_insert_template = (
    "INSERT INTO category (`ID`, `name`) "
    "VALUES ("
    "'{0}',"
    "'{1}')"
)

for (name, id) in cate_name2id.items():
    script = cate_insert_template.format(
        id,
        name.replace("'", r"\'")
    )
    cursor.execute(script)

db.commit()


# init develop table
cursor.execute("DROP TABLE IF EXISTS `develop`;")
db.commit()
cursor.execute(TABLES["develop"])

_dev_insert_template = (
    "INSERT INTO develop (`dev_id`, `game_id`) "
    "VALUES ("
    "'{0}',"
    "'{1}')"
)

for game in res:
    if not isinstance(game.developer, list):
        script = _dev_insert_template.format(
            dev_name2id[game.developer],
            game.id
        )
        cursor.execute(script)
    else:
        for dev in game.developer:
            script = _dev_insert_template.format(
                dev_name2id[dev],
                game.id
            )
            cursor.execute(script)
            
db.commit()


# init game_type table
cursor.execute("DROP TABLE IF EXISTS `game_type`;")
db.commit()
cursor.execute(TABLES["game_type"])

game_type_insert_template = (
    "INSERT INTO game_type (`game_id`, `cate_id`) "
    "VALUES ("
    "'{0}',"
    "'{1}')"
)

for game in res:
    for cate in game.user_tag:
        script = game_type_insert_template.format(
            game.id,
            cate_name2id[cate]
        )
        cursor.execute(script)
        
            
db.commit()



# init other empty tables
cursor.execute("DROP TABLE IF EXISTS `purchase`;")
db.commit()
cursor.execute(TABLES["purchase"])

cursor.execute("DROP TABLE IF EXISTS `barter`;")
db.commit()
cursor.execute(TABLES["barter"])

cursor.execute("DROP TABLE IF EXISTS `prefer`;")
db.commit()
cursor.execute(TABLES["prefer"])

cursor.execute("DROP TABLE IF EXISTS `promote`;")
db.commit()
cursor.execute(TABLES["promote"])

cursor.execute("DROP TABLE IF EXISTS `promote`;")
db.commit()
cursor.execute(TABLES["promote"])


cursor.execute("DROP TABLE IF EXISTS `rate`")
db.commit()
cursor.execute(TABLES["rate"])

db.commit()



USER_MODE = ['consumer', 'saler', 'super']

create_user_template = (
    "CREATE USER `{0}`@`localhost` IDENTIFIED WITH mysql_native_password;"
)

for mode in USER_MODE:
    cursor.execute("DROP USER IF EXISTS `{}`@`localhost`".format(mode))
    db.commit()
    cursor.execute(create_user_template.format(mode))



db.commit()


'''
    privilege granting
    
    consumer:
    INSERT: purchase, rate, barter
    DELETE: barter
    
    saler:
    UPDATE: promote
    
    super: all privilege

'''

    
consumer_grant = (
    "GRANT SELECT ON AGDP.barter TO `consumer`@`localhost`",
    "GRANT INSERT ON AGDP.purchase TO `consumer`@`localhost`",
    "GRANT INSERT ON AGDP.rate TO `consumer`@`localhost`",
    "GRANT INSERT ON AGDP.barter TO `consumer`@`localhost`",
    "GRANT SELECT ON AGDP.purchase TO `consumer`@`localhost`"
)



saler_grant = (
    "GRANT INSERT ON AGDP.promote TO `saler`@`localhost` "
)

super_grant= (
    "GRANT ALL PRIVILEGES ON AGDP.* TO `super`@`localhost` "
)


for script in consumer_grant:
    cursor.execute(script)

cursor.execute(saler_grant)
cursor.execute(super_grant)
db.commit()

cursor.close()



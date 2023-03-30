from threading import Thread
from threading import Condition, Lock

import mysql.connector

class buffer:
    def __init__(self):
        self.queue = []
    def is_empty(self):
        return len(self.queue) == 0
    def __len__(self):
        return len(self.queue)
    def pop(self):
        item = self.queue[0]
        self.queue = self.queue[1:]
        return item
    def push(self, item):
        self.queue.append(item)
    def len(self):
        return len(self.queue)

class query:
    def __init__(self, script, res_buffer, interrupt):
        self.script = script
        self.res_buffer = res_buffer
        self.interrupt = interrupt
        
        if script.strip().startswith('SELECT'):
            self.op_type = 'retrieve'
        else:
            self.op_type = 'update'
        


USER_MODE = ['consumer', 'saler', 'super']

LOG_FILE = './database.log'

interrupt_vector = {
    mode : Condition() for mode in USER_MODE
}

job_queue = {
    mode : buffer() for mode in USER_MODE
}

job_queue_mutex = {
    mode : Lock() for mode in USER_MODE
}


def run(db, query_to_serve):
    cursor = db.cursor()
    wait_cond = query_to_serve.interrupt
    cursor.execute(query_to_serve.script)
    
    wait_cond.acquire()
    
    if query_to_serve.op_type == 'retrieve':
        query_to_serve.res_buffer.append(cursor.fetchall())
    else:
        try:
            db.commit()
        except:
            db.rollback()
            
    wait_cond.notify()
    wait_cond.release()
    
    


def record():
    with open(LOG_FILE, 'w') as log_file:
        pass


def handler_init(mode):
    def handler():
        wait_cond = interrupt_vector[mode]
        handler_buffer = job_queue[mode]
        handler_mutex = job_queue_mutex[mode]

        db = mysql.connector.connect(
            host = 'localhost',
            user = mode,
            port = 3306,
            database = 'AGDP'
        )
        
        
        while True:
            wait_cond.acquire()
            while len(handler_buffer) == 0:
                wait_cond.wait()
            handler_mutex.acquire()
            query_to_serve = handler_buffer.pop()
            handler_mutex.release()
            
            run(db, query_to_serve)
            wait_cond.release()
                
    return Thread(target=handler)

handler_pool = {
    mode : handler_init(mode) for mode in USER_MODE
}

def handler(mode):
    assert mode in USER_MODE, 'wrong user mode identifier'
    
    wait_cond = interrupt_vector[mode]
    handler_buffer = job_queue[mode]
    handler_mutex = job_queue_mutex[mode]
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            script = func(*args, **kwargs)
            res_buffer = []
            __query = query(script, res_buffer, Condition())
            
            
            wait_cond.acquire()
            handler_mutex.acquire()
            if len(handler_buffer) == 0:
                wait_cond.notify()
            
            handler_buffer.push(__query)
            handler_mutex.release()
            wait_cond.release()
            
            __query.interrupt.acquire()
            if len(__query.res_buffer) == 0:
                __query.interrupt.wait()
            __query.interrupt.release()
            
            
            if __query.op_type == 'retrieve':
                return __query.res_buffer[0]
            else:
                pass
            
                     
        return wrapper
    
    return decorator



'''
    game table
'''
@handler('super')
def game_select(id):
    script = (
        "SELECT * FROM game "
        "WHERE id = {}"
    ).format(id)
    return script

@handler('super')
def __get_game_info():
    script = (
        "SELECT * FROM game "
    ).format(id)
    return script

def get_game_info():
    res = dict()
    for (id, name) in __get_game_info():
        res[name] = str(id)
    return res
    
    
    


@handler('super')
def game_insert(id, name, price, pub_id, release_date):
    script = (
        "INSERT INTO game (`ID`, `name`, `price`, `pub_id`, `release_date`) "
        "VALUES ("
        "'{}', "
        "\"{}\","
        "'{}', "
        "'{}', "
        "\"{}\")"
    ).format(
        id, name, price, pub_id, release_date
    )
    return script


'''
    purchase table
'''
@handler('consumer')
def purchase_insert(con_id, game_id, date):
    script = (
        "INSERT INTO purchase (`con_id`, `game_id`, `date`) "
        "VALUES ("
        "'{}',"
        "'{}',"
        "\"{}\")").format(con_id, game_id, date)
    return script    

@handler('consumer')
def purchase_select(con_id):
    script = (
        "SELECT game.ID, game.name, purchase.date, game.price "
        "FROM purchase INNER JOIN game "
        "ON purchase.game_id = game.ID "
        "WHERE purchase.con_id = '{}'"
    ).format(con_id)
    return script

@handler('consumer')
def purchase_delete(con_id, game_id):
    script = (
        "DELETE FROM purchase "
        "WHERE con_id = {} and game_id = {}"
    ).format(con_id, game_id)
    
    return script
    
def get_lib_info(con_id):
    res = purchase_select(con_id)
    
    return len(res), res


'''
    barter table
'''
@handler('consumer')
def barter_insert(con_id, sell_id, wish_id, status):
    script = (
        "INSERT INTO barter (`con_id`, `sell_id`, `wish_id`, `status`) "
        "VALUES ("
        "'{}',"
        "'{}',"
        "'{}',"
        "\"{}\")").format(con_id, sell_id, wish_id, status)
    return script



@handler('consumer')
def __barter_update_deal(con_id, sell_id, wish_id):
    deal_update_script = (
       "UPDATE barter "
       "SET `status` = \"deal\" "
       "WHERE con_id  = {} and sell_id = {} and wish_id = {}" 
    ).format(con_id, sell_id, wish_id)
    
    return deal_update_script

@handler('consumer')
def __barter_update_closed(con_id, sell_id, wish_id):
    closed_update_script = (
        "UPDATE barter "
        "SET `status` = \"closed\" "
        "WHERE con_id = {} and sell_id = {} and wish_id != {}"
    ).format(con_id, sell_id, wish_id)
    
    return closed_update_script
    

def barter_update(seller_con_id, buyer_con_id, sell_id, wish_id, date):
    __barter_update_deal(seller_con_id, sell_id, wish_id)
    __barter_update_closed(seller_con_id, sell_id, wish_id)
    
    # exchange game
    purchase_insert(con_id=buyer_con_id,  game_id=sell_id, date=date)
    purchase_insert(con_id=seller_con_id, game_id=wish_id, date=date)
    
    purchase_delete(con_id=seller_con_id, game_id=sell_id)
    purchase_delete(con_id=buyer_con_id,  game_id=wish_id)
    




@handler('consumer')
def __barter_select_con():
    
    
    script = (
        "SELECT barter.con_id, sell_id, game.name, game.price, purchase.date " 
        "FROM barter INNER JOIN ("
        "     game INNER JOIN purchase "
        "     ON game.ID = purchase.game_id "
        ") ON barter.sell_id = game.ID "
        "WHERE status = \"open\" "
        "GROUP BY barter.con_id, sell_id, purchase.date"
    )
    return script

@handler('consumer')
def __barter_select_wish_by_con(con_id, sell_id):
    script = (
        "SELECT wish_id, game.name "
        "FROM barter INNER JOIN game "
        "ON barter.wish_id = game.ID "
        "WHERE con_id = {} and sell_id = {} and status = \"open\""
    ).format(con_id, sell_id)
    
    return script
    
def barter_select():
    res = []
    con_sell_list = __barter_select_con()
    for (con_id, sell_id, sell_name, price, date) in con_sell_list:
        wish_list = __barter_select_wish_by_con(con_id, sell_id)
        res.append(
            [con_id, [sell_id, sell_name, price, date] , wish_list]
        )
    return res


'''

    meta table

'''

@handler('super')
def meta_select():
    script = (
        "SELECT * FROM meta "
    )
    return script


@handler('super')
def meta_con_update(con_cnt, pub_cnt):
    script = (
        "UPDATE meta "
        "SET `con_cnt` = {} "
        "WHERE `stub` = 0").format(con_cnt, pub_cnt)
    return script

@handler('super')
def meta_all_update(**kwargs):
    script = (
        "UPDATE meta "
        "SET `con_cnt` = {}, "
        "    `pub_cnt` = {}, "
        "    `dev_cnt` = {}, "
        "    `cate_cnt` = {}, "
        "    `game_cnt` = {} "
        "WHERE `stub` = 0").format(
            kwargs['con_cnt'],
            kwargs['pub_cnt'],
            kwargs['dev_cnt'],
            kwargs['cate_cnt'],
            kwargs['game_cnt']
        )
    return script
    



'''
    consumer table

'''

@handler('super')
def consumer_select(**kwargs):
    k, v = list(kwargs.items())[0]
    script = (
        "SELECT * FROM consumer "
        "WHERE {} = \"{}\""
    ).format(k, v)
    
    return script

@handler('super')
def consumer_insert(id, username, pwd):
    script = (
        "INSERT INTO consumer (`id`, `name`, `password`)"
        "VALUES ("
        "'{}',"
        "\"{}\","
        "\"{}\")"
    ).format(id, username, pwd)
    
    return script


def duplicate_name(username):
    res = consumer_select(name=username)
    return len(res) != 0



@handler('consumer')
def matched_game_name(substr):
    script = (
        "SELECT name "
        "FROM game "
        "WHERE name LIKE '%{}%'"
    ).format(substr)
    
    return script


@handler('consumer')
def game_select_id_by_name(name):
    script = (
        "SELECT ID FROM game "
        "WHERE name = \"{}\""
    ).format(name)
    return script




'''
    publisher table operation
'''
@handler('super')
def pub_select(id):
    script = (
        "SELECT * FROM publisher "
        "WHERE ID = {}"
    ).format(id)
    
    return script

# get publisher dict
@handler('super')
def __get_pub_info():
    script = (
        "SELECT * FROM publisher "
    )
    return script

def get_pub_info():
    res = dict()
    for (id, name) in __get_pub_info():
        res[name] = str(id)
    return res


@handler('super')
def pub_insert(id, name):
    script = (
        "INSERT INTO publisher (`ID`, `name`) "
        "VALUES ("
        "'{}',"
        "\"{}\")"
    ).format(id, name)
    return script
    

'''
    developer table operation
'''
@handler('super')
def developer_select(id):
    script = (
        "SELECT D.name "
        "FROM develop as DEV INNER JOIN developer as D "
        "on DEV.dev_id = D.ID "
        "WHERE DEV.game_id = {}"      
    ).format(id)
    return script


# get publisher dict
@handler('super')
def __get_dev_info():
    script = (
        "SELECT * FROM developer "
    )
    return script

def get_dev_info():
    res = dict()
    for (id, name) in __get_dev_info():
        res[name] = str(id)
    return res


@handler('super')
def developer_insert(id, name):
    script = (
        "INSERT INTO developer (`ID`, `name`) "
        "VALUES ("
        "'{}',"
        "\"{}\")"
    ).format(id, name)
    return script
    






'''
    cate table operation
'''
# get cate dict
@handler('super')
def __get_cate_info():
    script = (
        "SELECT * FROM category "
    )
    return script

def get_cate_info():
    res = dict()
    for (id, name) in __get_cate_info():
        res[name] = str(id)
    return res

@handler('super')
def cate_insert(id, name):
    script = (
        "INSERT INTO category (`ID`, `name`) "
        "VALUES ("
        "'{}',"
        "\"{}\")"
    ).format(id, name)
    return script
    


@handler('super')
def cate_id_select(id):
    script = (
        "SELECT cate_id FROM game_type "
        "WHERE game_id = {}"
    ).format(id)
    
    return script

@handler('super')
def cate_recommand_select(cate_id, game_id):
    script = (
        "SELECT DISTINCT game_id FROM game_type "
        "WHERE cate_id = {} and game_id != {}"
    ).format(cate_id, game_id)
    return script


from random import shuffle

def cate_select(id):
    res = []
    cate_id = cate_id_select(id)
    for cate in cate_id:
        res.extend(
            [i[0] for i in cate_recommand_select(cate[0], id)]
        )
    shuffle(res)
    return res[:3]


    

@handler('super')
def tags_select(id):
    script = (
        "SELECT C.name "
        "FROM game_type as G INNER JOIN category as C "
        "on G.cate_id = C.ID "
        "WHERE G.game_id = {}"        
    ).format(id)
    
    return script      

    
'''
    API required by market
'''
@handler('saler')
def select_game_by_cate_name(cate_name):
    script = (
        "SELECT game.ID, game.name, game.release_date, game.price "
        "       FROM category INNER JOIN( "
        "           (game INNER JOIN game_type"
        "            ON game.ID = game_type.game_id)"
        "       )"
        "       ON category.ID = game_type.cate_id"
        "       WHERE category.name = \"{}\""
    ).format(cate_name)

    return script


@handler('super')
def get_con_name(con_id):
    script = (
        "SELECT name "
        "FROM consumer "
        "WHERE ID = {}"
    ).format(con_id)
    
    return script

# def get_con_name(con_id):
#     return __get_con_name(con_id)[0][0]


'''
    game_type operation
'''

@handler('super')
def game_type_insert(game_id, cate_id):
    script = (
        "INSERT INTO game_type (`game_id`, `cate_id`) "
        "VALUES ("
        "'{}',"
        "'{}')"
    ).format(game_id, cate_id)
    return script
    


''' develop operation '''

@handler('super')
def develop_insert(dev_id, game_id):
    script = (
        "INSERT INTO develop (`dev_id`, `game_id`) "
        "VALUES ("
        "'{}',"
        "'{}')"
    ).format(dev_id, game_id)
    return script
    
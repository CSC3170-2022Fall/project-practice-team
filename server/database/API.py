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


# @handler('consumer')
# def consumer_purchase(id,game_id,date):
#     script = (
#         "INSERT INTO purchase (`con_id`,`game_id`,date)"
#         "VALUES ("
#         "'{}',"
#         "\"{}\","
#         "\"{}\")"
#     ).format(id, game_id, date)
#     return script

# @handler('consumer')
# def consumer_barter(id,sell_id,wish_id):
#     script = (
#         "INSERT INTO barter (`con_id`,`sell_id`,`wish_id`)"
#         "VALUES ("
#         "'{}',"
#         "\"{}\","
#         "\"{}\")"
#     ).format(id,sell_id,wish_id)
#     return script

# @handler('consumer')
# def consumer_rate(id,game_id,score):
#     script = (
#         "INSERT INTO rate (`con_id`,`game_id`,`score`)"
#         "VALUES ("
#         "'{}',"
#         "\"{}\","
#         "\"{}\")"
#     ).format(id,game_id,score)
#     return script

# @handler('consumer')
# def consumer_library(id):
#     script = (
#         "SELECT 'game_id' AS game from purchase "
#         "WHERE id = {}"
#         "UNION"
#         "SELECT 'wish_id' from barter "
#         "WHERE id = {}"
#         "MINUS"
#         "SELECT 'sell_id' from barter "
#         "WHERE id = {}"
#     ).format(id)
#     return script



# @handler('super')
# def game_type_insert():
#     script = (
#         "SELECT * from publisher"
#     )
#     return script

@handler('super')
def game_select(id):
    script = (
        "SELECT * FROM game "
        "WHERE id = {}"
    ).format(id)
    return script

def game_rate(id):
    script = (
        "SELECT AVG(score)"
        "FROM rate"
        "WHERE id = {}"
    ).format(id)
    return script


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
def meta_update(con_cnt, pub_cnt):
    script = (
        "UPDATE meta "
        "SET `con_cnt` = {}, "
        "    `pub_cnt` = {} "
        "WHERE `stub` = 0").format(con_cnt, pub_cnt)
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









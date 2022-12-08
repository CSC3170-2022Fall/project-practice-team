from wrapper import handler
from handler_init import handler_pool

@handler('super')
def game_type_insert():
    script = (
        "INSERT INTO prefer (`con_id`, `cate_id`)"
        "VALUES ("
        "'10',"
        "'20')"
    )
    return script












if __name__ == '__main__':
    for handler_thread in handler_pool.values():
        handler_thread.start()
    res = game_type_insert()
    



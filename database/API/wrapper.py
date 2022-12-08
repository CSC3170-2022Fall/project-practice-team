from handler_init import (
    interrupt_vector,
    USER_MODE,
    job_queue,
    job_queue_mutex
)

from handler_init import query
from threading import Condition





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
            while len(__query.res_buffer) == 0:
                __query.interrupt.wait()
            __query.interrupt.release()
            
            return __query.res_buffer[0]
                     
        return wrapper
    
    return decorator



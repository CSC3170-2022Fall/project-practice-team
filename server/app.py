from database.API import handler_pool

from flask import Flask, render_template, request
from flask import redirect

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    for handler_thread in handler_pool.values():
        handler_thread.start()
    
    app.run()
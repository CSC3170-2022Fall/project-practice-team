from database.API import handler_pool

from database.API import *

from flask import Flask, render_template, request
from flask import redirect

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/game')
def game():
    id = request.args.get('game_id')
    game_info = game_select(id)
    return render_template('game.html', id=id, info=game_info)





if __name__ == '__main__':
    for handler_thread in handler_pool.values():
        handler_thread.start()
    
    app.run()
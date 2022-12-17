from database.API import handler_pool

from database.API import *

from flask import Flask, render_template, request, redirect
from flask import jsonify


app = Flask(__name__)
meta = dict()


@app.route('/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        form_type = request.form['form_type']
        username  = request.form['username']
        password  = request.form['password']
        
        
        if form_type == 'register':
            if duplicate_name(username):
                pass
            else:
                meta['con_cnt'] += 1;
                meta_update(meta['con_cnt'], meta['pub_cnt'])
                consumer_insert(meta['con_cnt'], username, password)
                return render_template('index.html')
        
        
        elif form_type == 'login':
            res = consumer_select(name=username)[0]
            # if password is correct
            if password == res[2]:
                print('password correct')
                # redirect('/consumer?id={}'.format(res[0]))
                return render_template('index.html')
            # in correct password
            else:
                pass
        
            

    
    return render_template('login.html')



@app.route('/consumer')
def consumer():
    # id = request.args.get('id')
    
    
    return render_template('consumer.html', games=None, username=None, purchase_date=None)



@app.route('/game')
def game():
    id = request.args.get('id')
    game_info = game_select(id)
    return render_template('game.html', id=id, info=game_info)


@app.route('/game/search/by_name')
def game_search_id_by_name():
    name = request.args.get('name')
    print(name)
    res = game_select_id_by_name(name)

    
    return jsonify(res)

@app.route('/game/search/name_contain')
def game_search_name_contain():
    substr = request.args.get('substr')
    res = [i[0] for i in matched_game_name(substr)]
    return jsonify(res)
    


if __name__ == '__main__':
    for handler_thread in handler_pool.values():
        handler_thread.start()
    
    
    init_meta = meta_select()
    meta['con_cnt'] = init_meta[0][1]
    meta['pub_cnt'] = init_meta[0][2]
    
    app.run()
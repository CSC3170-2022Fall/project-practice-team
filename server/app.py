from database.API import handler_pool

from database.API import *

from flask import Flask, render_template, request, redirect
from flask import jsonify

import os
from io import BytesIO




app = Flask(__name__)
meta = dict()

# path where the uploaded game pictures are stored on the server
UPLOAD_FOLDER = '/static/tmp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/validate', methods=['POST'])
def validate():
    form_type = request.form['form_type']
    username  = request.form['username']
    password  = request.form['password']
    
    
    if form_type == 'register':
        if duplicate_name(username):
            return jsonify({
                'state' : 'duplicate_name'
            })

        else:
            meta['con_cnt'] += 1;
            
            meta_update(meta['con_cnt'], meta['pub_cnt'])
            consumer_insert(meta['con_cnt'], username, password)
            
            print(username, password)
            
            
            return jsonify({
                'state' : 'successful'
            })
            

    
    elif form_type == 'login':
        res = consumer_select(name=username)
        
        if len(res) == 0:
            return jsonify({
                'state' : 'wrong_username'
            })
        
        res = res[0]
        print(password, res[2])
        print(type(password), type(res[2]))
        
        # if password is correct
        if password == res[2]:
            return jsonify({
                'state' : 'successful',
                'id' : res[0]
            })
        
        # incorrect password
        else:
            return jsonify({
                'state' : 'wrong_password'
            })
    

from random import shuffle

@app.route('/market')
def market():
    con_id  = request.args.get('con_id')
    game_info = []
    cate_list = [
        'strategy', 'action', 'card game', 'first-person', 'open world', 'adventure'
    ]
    order_list=[]
    name=get_con_name(con_id)
    for i in range(6):
        order_list.append(i)
    for cate in cate_list:
        res = select_game_by_cate_name(cate)
        shuffle(res)
        game_info.append(
            res[:4]
        )
    return render_template('index.html',cate_list=cate_list,game_info=game_info,order_list=order_list,name=name)



@app.route('/consumer')
def consumer():
    return render_template('consumer.html', games=None, username=None, purchase_date=None)



@app.route('/game')
def game():
    ID = 0; NAME = 1; PRICE = 2; PUB_ID = 3; R_DATE = 4
    id = request.args.get('game_id')
    
    '''
        retrieve game basic info from game table, including:
        name; price; publisher id; release data
    '''
    game_info = game_select(id)[0]
    
    
    '''
        retrieve developer name
    '''
    dev_name = [i[0] for i in developer_select(game_info[ID])]
    
    '''
        retrieve publisher name from publisher table using pub_id
    '''
    pub_id = game_info[PUB_ID]
    pub_info = pub_select(pub_id)[0]
    
    
    '''
        retrieve game category from category table
    '''
    recommand_ids = cate_select(game_info[ID])
    recommands = []
    for recommand_id in recommand_ids:
        recommands.append(game_select(recommand_id)[0])

    
    '''
        retrieve tag from game_type and category table
    '''
    
    tags = tags_select(game_info[ID])
    tags = [tag[0] for tag in tags][:10]

    

    return render_template('gamepage.html',
                           id=game_info[ID], name=game_info[NAME],
                           release_date=game_info[R_DATE], price=game_info[PRICE],
                           pub_name=pub_info[NAME],
                           dev_name=dev_name,
                           tags=tags,
                           recommands=recommands
                        )


@app.route('/game/search/by-name')
def game_search_id_by_name():
    name = request.args.get('name')
    res = game_select_id_by_name(name)

    
    return jsonify(res)

@app.route('/game/search/name-contain')
def game_search_name_contain():
    substr = request.args.get('substr')
    res = [i[0] for i in matched_game_name(substr)]
    return jsonify(res)

@app.route('/barter')
def barter():
    return render_template('barter.html')



'''
   handle uploaded game picture
'''

def valid_filename(filename):
    extension = filename.rsplit('.')[0]
    return extension.lower() == '.jpg'

@app.route('/publisher/add-game', methods=['POST'])
def pub_add_game():
    print('hello')
    file = request.files['file']
    print(file.filename)
    if valid_filename(file.filename):
        file.save(
            os.path.join(app.config['UPLOAD_FOLDER'], 'test.jpg')
        )     
        return jsonify({
            'state' : 'successful'
        })
        
    else:
        return jsonify({
            'state' : 'wrong_extension'
        })
    
    
@app.route('/consumer/purchase', methods=['POST'])
def purchase():
    con_id  = request.form['con_id']
    game_id = request.form['game_id']
    date    = request.form['date']
    
    from calendar import month_name
    name2mon_name = {
        str(k) : v for (k, v) in enumerate(month_name) if k != 0
    }
    
    # parse date
    mm, dd, yyyy = date.split(' ')
    mm = name2mon_name[mm]
    
    date = dd + ' ' + mm + ' ' + yyyy
    
    purchase_insert(
        con_id=con_id, game_id=game_id, date=date
    )
    
    return jsonify({
        'state' : 'successful'
    })


@app.route('/library', methods = ['GET'])
def library():
    con_id = request.args.get('con_id')
    name=get_con_name(con_id)
    num, lib_info = get_lib_info(con_id)
    
    return render_template('consumer.html')



if __name__ == '__main__':
    for handler_thread in handler_pool.values():
        handler_thread.start()
    
    
    init_meta = meta_select()
    meta['con_cnt']  = init_meta[0][1]
    meta['pub_cnt']  = init_meta[0][2]
    meta['game_cnt'] = init_meta[0][3]
    
    app.run()
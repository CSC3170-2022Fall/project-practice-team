from database.API import handler_pool

from database.API import *

from flask import Flask, render_template, request, redirect
from flask import jsonify

import os
from io import BytesIO
from PIL import Image


from calendar import month_name
name2mon_name = {
    str(k) : v for (k, v) in enumerate(month_name) if k != 0
}



app = Flask(__name__)
meta = dict()

# path where the uploaded game pictures are stored on the server
UPLOAD_FOLDER = 'static/pics'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
DEFAULT_IMAGE_SIZE = (460, 215)

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
            
            meta_con_update(meta['con_cnt'], meta['pub_cnt'])
            consumer_insert(meta['con_cnt'], username, password)
            
            
            
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
    return render_template('index.html', con_id=con_id, cate_list=cate_list, game_info=game_info, order_list=order_list, name=name)



@app.route('/consumer')
def consumer():
    con_id = request.args.get('con_id')
    username = get_con_name(con_id)[0][0]
    game_num, game_list = get_lib_info(con_id)
    return render_template('consumer.html', con_id=con_id, game_num=game_num, game_list=game_list, games=None, username=username, purchase_date=None)



@app.route('/game')
def game():
    ID = 0; NAME = 1; PRICE = 2; PUB_ID = 3; R_DATE = 4
    id = request.args.get('game_id')
    con_id = request.args.get('con_id')

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
                            con_id=con_id,
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
    con_id = request.args.get('con_id')
    barter_tuples = barter_select()
    print(barter_tuples)
    return render_template('barter.html', con_id=con_id, barter_tuples=barter_tuples)


@app.route('/consumer/barter-issue', methods=['POST'])
def barter_issue():
    con_id = request.form['con_id']
    sell_id = request.form['sell_id']
    wish_id = request.form['wish_id']
    status = 'open'
    
    barter_insert(
        con_id=con_id, sell_id=sell_id, wish_id=wish_id, status=status
    )
    
    return jsonify({
        'state' : 'successful'
    })


@app.route('/consumer/barter-deal', methods=['POST'])
def barter_deal():
    buyer_id  = request.form['buyer_id']
    seller_id = request.form['seller_id']
    sell_id   = request.form['sell_id']
    wish_id   = request.form['wish_id']
    date      = request.form['date']
    
    mm, dd, yyyy = date.replace('/', ' ').split(' ')
    mm = name2mon_name[mm]
    
    date = dd + ' ' + mm + ' ' + yyyy
    
    _, owned_games = get_lib_info(buyer_id)
    owned_games = [int(i[0]) for i in owned_games]
    
    
    if buyer_id == seller_id:
        return jsonify({
            'state' : 'recursive'
        })
        
    if int(wish_id) not in owned_games:
        return jsonify({
            'state' : 'not_own'
        })
        

    print(date)
    print(buyer_id, seller_id, sell_id, wish_id)
    
    barter_update(
        seller_con_id=seller_id, buyer_con_id=buyer_id,
        sell_id=sell_id, wish_id=wish_id,
        date=date
    )
    
    return jsonify({
        'state' : 'successful'
    })


'''
   handle uploaded game picture
'''

def valid_filename(filename):
    extension = filename.split('.')[1]
    print(extension)
    return extension.lower() == 'jpeg' or extension.lower() == 'jpg'

@app.route('/publisher/add-game', methods=['POST'])
def pub_add_game():
    file = request.files['file']
    
    upload_form = request.form.to_dict()
    
    meta['game_cnt'] += 1
    game_id = meta['game_cnt']
    game_name = upload_form['game_name']
    dev_name  = upload_form['dev_name']
    pub_name  = upload_form['pub_name']
    price     = upload_form['price']
    
    date      = upload_form['date']
    mm, dd, yyyy = date.replace('/', ' ').split(' ')
    mm = name2mon_name[mm]
    
    date = dd + ' ' + mm + ' ' + yyyy
    
    tag       = upload_form['tags']
    
    exist_pub = get_pub_info()
    if pub_name in exist_pub.keys():
        pub_id = exist_pub[pub_name]
    else:
        meta['pub_cnt'] += 1
        pub_id = meta['pub_cnt']
        pub_insert(id=pub_id, name=pub_name)
        
    exist_dev = get_dev_info()
    if dev_name in exist_dev.keys():
        dev_id = exist_dev[dev_name]
    else:
        meta['dev_cnt'] += 1
        dev_id = meta['dev_cnt']
        developer_insert(id=dev_id, name=dev_name)
        
    exist_cate = get_cate_info()
    if tag in exist_cate.keys():
        cate_id = exist_cate[tag]
    else:
        meta['cate_cnt'] += 1
        cate_id = meta['cate_cnt']
        cate_insert(id=cate_id, name=tag)
    

    
    develop_insert(dev_id=dev_id, game_id=game_id)
    game_type_insert(game_id=game_id, cate_id=cate_id)
    
    
    game_insert(
        id=game_id, name=game_name,
        price=price, pub_id=pub_id,
        release_date=date
    )
    
    meta_all_update(**meta)
    
    
    print(file.filename)
    if valid_filename(file.filename):
        
        buffer = BytesIO(file.read())
        image = Image.open(buffer)
        resized_img = image.resize(DEFAULT_IMAGE_SIZE)
        basedir = os.path.abspath(os.path.dirname(__file__))
        
        resized_img.save(
            os.path.join(basedir, app.config['UPLOAD_FOLDER'], f'{game_id}.jpg'),
            format='jpeg'
        )     
        return 'Successful!'
        
    else:
        return 'Invalid Upload!'
    
    
    
@app.route('/consumer/purchase', methods=['POST'])
def purchase():
    con_id  = request.form['con_id']
    game_id = request.form['game_id']
    date    = request.form['date']
    
    _, owned_games = get_lib_info(con_id)
    owned_games = [int(i[0]) for i in owned_games]
    
    if int(game_id) in owned_games:
        return jsonify({
            'state' : 'duplicate'
        })
    
    
    
    # parse date
    mm, dd, yyyy = date.replace('/', ' ').split(' ')
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
    
    return redirect(f'/consumer?con_id={con_id}')




if __name__ == '__main__':
    for handler_thread in handler_pool.values():
        handler_thread.start()
    
    
    init_meta = meta_select()
    meta['con_cnt']  = init_meta[0][1]
    meta['pub_cnt']  = init_meta[0][2]
    meta['dev_cnt']  = init_meta[0][3]
    meta['cate_cnt']  = init_meta[0][4]
    meta['game_cnt'] = init_meta[0][5]
    
    app.run()
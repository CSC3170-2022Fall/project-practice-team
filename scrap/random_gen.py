import pickle
import random

random.seed(42)

pickle_path = '../scrap/game_raw.pickle'

with open(pickle_path, 'rb') as handler:
    res = pickle.load(handler)

publishers = {}
            

for game in res:
    if not isinstance(game.publisher, list):
        publishers[game.publisher] = publishers.get(game.publisher, 0) + 1
    else:
        for comp in game.publisher:
            publishers[comp] = publishers.get(comp, 0) + 1


'''
    318 games in total
    150 publisher (one game can only have one publisher)
'''


selected_publisher = [pub for (pub, _) in sorted(publishers.items(), key=lambda x: x[1], reverse=True)[:150]]

for game in res:
    game.publisher = random.choice(selected_publisher)
    
    
with open('game.pickle', 'wb') as handler:
    pickle.dump(res, handler)
class Game:
    def __init__(self, **kwargs):
        self.id        = kwargs.get('id')
        self.name      = kwargs.get('name')
        self.developer = kwargs.get('developer')
        self.price     = kwargs.get('price')
        self.pic_url   = kwargs.get('pic_url')
        
        self.release_date = kwargs.get('release_date')
        
        '''
            advanced attributes of a game app:
         1. stats
            including '24 hour peek' and 'all time peek'
            which specify the largest number of active players in the past 24 hours and since the releases
        
        2.  user_tags
            categorical info
        
        '''
        self.stats = {
            '24_hour_peek'  : kwargs.get('24_hour_peek', None),
            'all_time_peek' : kwargs.get('all_time_peek', None)   
        }
        self.user_tag = kwargs.get('user_tag', [])
        
        
        
    # formatted output
    def __repr__(self):
        
        sep = '-'*80 + '\n'
        basics = f'ID: {self.id}\t NAME: {self.name}\t PRICE : {self.price}\n'
        
        if (type(self.developer) is list):
            developer = 'DEVELOPER:\n {}\n'.format(
                ('\n').join(
                    '\t'.join(j.strip() for j in self.developer[4*i:4*i+4]) 
                        for i in range(int(len(self.developer)/4))
                )
            )
        else:
            developer = f'DEVELOPER: {self.developer}\n'
        
        user_tag = 'USER TAG:\n {}\n'.format(
            ('\n').join(
                '\t'.join(j.strip() for j in self.user_tag[4*i:4*i+4]) 
                    for i in range(int(len(self.user_tag)/4))
            )
        )

        return sep + basics + sep + developer + sep + user_tag + sep

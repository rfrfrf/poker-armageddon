class Bot(object):
    def __init__(self, id, credits, *args, **kwargs):
        self.id = id
        self.credits = credits
        self.event_queue = []
    
    def turn(self):
        raise NotImplementedError
        
    def __str__(self):
        return "<Bot player_id=%d>" % (self.id)
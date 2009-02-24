class Bot(object):
    def __init__(self, id, credits, big_blind_amount, small_blind_amount, *args, **kwargs):
        self.id = id
        self.initial_credits = credits
        self.credits = self.initial_credits
        self.big_blind_amount = big_blind_amount
        self.small_blind_amount = small_blind_amount
        self.event_queue = []
    
    def turn(self):
        raise NotImplementedError
        
    def __str__(self):
        return "<Bot player_id=%d>" % (self.id)
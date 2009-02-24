class KeywordObject(object):
    def __init__(self, type, **kwargs):
        self.type = type
        for k,v in kwargs.iteritems():
            setattr(self, k, v)
        #print "created: %s" % self.__str__()
            
    def __str__(self):
        result = "<%s type=%s%s>"
        attributes = ""
        for k,v in sorted(self.__dict__.iteritems()):
            if k.startswith('_') or k == 'type':
                continue
            attributes += " %s=%s" % (k, v)
        return result % (self.__class__.__name__, self.type, attributes)

# event format:
# <type> <properties>
# 'join' player_id credits
# 'new_round'
# 'button' player_id
# 'big_blind' player_id
# 'small_blind' player_id
# 'deal' cards
# 'flop' cards
# 'turn' card  # fourth community card
# 'river' card # fifth community card
# 'action' player <Action>
# 'adjust_credits'  player (+/-)amount
# 'win' player rank amount -> there is also an adjust_credits event for this
#                             in the case that there are multiple winners
#                             the rank will indicate who won first, second etc (int)
# 'end_of_round'
# 'quit' player_id
# 'bad_bot' message <Action> -> last action by your bot was determined to be invalid
# 
class Event(KeywordObject):
    pass

# action format:
# 'fold',
#    fold means you quit this round
# 'call', 
#    call means you match the current high bet
# 'raise' amount
#    raise means you match the current high bet and add some amount to it
# 'check' (not available on first round, except for the big blind)
#    a check is just a pass
        
class Action(KeywordObject):
    pass
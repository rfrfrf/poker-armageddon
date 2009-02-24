class BotWrapper(object):
    def __init__(self, bot, *args, **kwargs):
        self.id = kwargs['id']
        self.credits = kwargs['credits']
        self.bot = bot(*args, **kwargs)
        
    @staticmethod
    def filter_action(input_action):
        return input_action
        
    def turn(self):
        return self.bot.turn()
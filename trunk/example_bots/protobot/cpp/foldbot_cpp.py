import os
this_dir = os.path.dirname(os.path.realpath( __file__ ))

from proto_bot import ProtoBot

class FoldBot(ProtoBot):
    command = [os.path.join(this_dir, 'foldbot/foldbot')]
    output_stderr = True
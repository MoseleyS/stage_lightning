import sys
from pynput.keyboard import Key, Listener

class HumanInterface():
    def __init__(self, key_file=False, key_dict=False, log=None):
        """Load key mapping"""
        if key_file:
            with open(key_file, 'r') as flh:
                self.key_dict = yaml.load(flh)
        elif key_dict:
            self.key_dict = key_dict.copy()
        else:
            print('No dictionary supplied, will only echo key presses')
            self.key_dict = {}
        if log:
            self.log = open(log, 'w')
        else:
            self.log = sys.stdout

    def listen(self):
        """Get keyboard and touchpad input"""
        with Listener(
                on_press=self.process_key,
                on_release=self.check_esc) as listener:
            listener.join()

    def process_key(self, key):
        self.log.write(f'{key} pressed; type {type(key)}')
        if hasattr(key, 'char'):
            key_char = key.char
        else:
            key_char = key
        action = self.key_dict.get(key_char, False)
        if action:
            self.log.write(f'Running action {action}')
            action(key_char)

    def check_esc(self, key):
        self.log.write(f'{key} release')
        if key == Key.esc:
            # close log
            self.log.close()
            # Stop listener
            return False

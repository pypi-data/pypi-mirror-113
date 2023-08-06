import os, sys


class SelectOS:
    def __init__(self):
        self.platform = None
        self.the_path = None
        self.cwd = os.path.dirname(os.path.abspath(__file__))
        self.define_route()
        self.change_permission()

    def define_route(self):
        self.platform = sys.platform

        if self.platform == 'linux':
            self.the_path = self.cwd + '/dummy_binary.linux'
        elif self.platform == 'darwin':
            self.the_path = self.cwd + '/dummy_binary.mac'
        elif self.platform == 'win32':
            self.the_path = self.cwd + '/dummy_binary.exe'
        else:
            raise Exception('This is not a valid operating system')

    def change_permission(self):
        if os.path.exists(self.the_path):
            os.chmod(self.the_path, int('777', 8))
        else:
            raise Exception('File not found {0}'.format(self.the_path))

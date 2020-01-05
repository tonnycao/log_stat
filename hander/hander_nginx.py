from hander.hander import Hander


class HanderNginx(Hander):

    def __init__(self, path):
        self.target = path

    def parse(self, content):
        with open(self.target, mode='a+', encoding='utf-8') as fd2:
            fd2.write(content + "\n")

    def notify(self):
        pass
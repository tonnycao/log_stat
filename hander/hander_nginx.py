import re
from hander.hander import Hander


class HanderNginx(Hander):

    def __init__(self, path):
        self.target = path

    def parse(self, content):
        with open(self.target, mode='a+', encoding='utf-8') as fd2:
            fd2.write(content + "\n")

    def split_nginx_log(content):
        """
        分析ngixn访问日志
        :param log_path:日志文件
        :return: []
        """
        url_list = []
        content = content.strip()
        p1 = content.index(']') + 1
        ip_time = content[0:p1]
        left_part = content[p1 + 1:].strip()
        left_parts = left_part.split('"')
        method = left_parts[1]
        status = left_parts[2].strip()
        user_agent = left_parts[5]
        ip_times = ip_time.split(' ')
        ip = ip_times[0]
        time_str = ip_times[3].strip('[')
        url = ''
        mac = ''
        p2 = user_agent.find('MAC')
        if p2 > 0:
            mac = user_agent[p2 + 4:]
        methods = method.split(' ')
        device = ''
        reg1 = re.compile(r'[(](.*?)[)]', re.S)
        devices = re.findall(reg1, user_agent)
        if len(devices) > 0:
            device = devices[0]
        data = {
            'ip': ip,
            'time': time_str,
            'method': methods[0],
            'url': methods[1].strip(),
            'status': status,
            'user_agent': user_agent,
            'mac': mac,
            'device': device
        }
        url_list.append(data)
        return url_list

    def notify(self):
        pass
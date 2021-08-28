import requests
import json
import os
import time

from qqbot import QQBot


class LiveChecker:
    '''Bilibili 直播检测'''

    def __init__(self, uids: list, bot: QQBot, group: int):

        self.uids = uids

        self.bot = bot

        self.group = group

        self.state = dict.fromkeys(self.uids, False)

    def check(self):
        '''获取直播间信息'''

        post_data = {
            'uids': self.uids
        }

        res = json.loads(requests.post(
            url='https://api.live.bilibili.com/room/v1/Room/get_status_info_by_uids', data=json.dumps(post_data)).text)

        if res['code'] != 0:
            return False

        for i in range(len(self.uids)):
            if res['data'][str(self.uids[i])]['live_status'] == 1:
                if self.state[self.uids[i]] == False:
                    print(time.strftime(
                        "[%Y-%m-%d %H:%M:%S]", time.localtime()), str(self.uids[i]), '正在直播！')

                    self.state[self.uids[i]] = True

                    messageChain_group = [
                        {'type': 'AtAll'},
                        {'type': 'Plain', 'text': '\n主播 ' +
                         res['data'][str(self.uids[i])]['uname'] + ' 开播啦！\n'},
                        {'type': 'Plain', 'text': '房间标题：' +
                         res['data'][str(self.uids[i])]['title'] + '\n'},
                        {'type': 'Plain', 'text': '直播分区：' +
                         res['data'][str(self.uids[i])]['area_v2_name'] + '\n'},
                        {'type': 'Plain', 'text': '快去 https://live.bilibili.com/' +
                         str(res['data'][str(self.uids[i])]['room_id']) + ' 围观吧！\n'},
                        {'type': 'Image', 'url': res['data'][str(
                            self.uids[i])]['cover_from_user']}
                    ]

                    print(messageChain_group)

                    if bot.send_group_msg(self.group, messageChain_group) == False:
                        bot.bind_bot()
                        bot.send_group_msg(self.group, messageChain_group)

            else:
                if self.state[self.uids[i]] == True:
                    print(time.strftime(
                        "[%Y-%m-%d %H:%M:%S]", time.localtime()), str(self.uids[i]), '直播结束！')

                    self.state[self.uids[i]] = False

        return True


if __name__ == '__main__':

    # 读取配置文件
    if os.path.exists('./config.json'):
        configs = json.loads(open('./config.json', 'r').read())

        host = configs['QQBot']['host']
        port = configs['QQBot']['port']
        verifyKey = configs['QQBot']['verifyKey']
        qq = configs['QQBot']['qq']

        uids = configs['LiveChecker']['uids']
        group = configs['LiveChecker']['group']

    else:
        print('配置文件 config.json 不存在！')

    bot = QQBot(host, port, verifyKey, qq)
    live_checker = LiveChecker(uids, bot, group)

    try:
        while True:
            live_checker.check()
            time.sleep(10)

    except:
        bot.release_bot()

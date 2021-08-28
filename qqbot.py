import requests
import json


class QQBot:
    '''mirai-api-http QQ 机器人'''

    def __init__(self, host: str, port: str, verifyKey: str, qq: int):

        # mirai-api-http 地址
        self.host = host

        # 端口
        self.port = port

        # 密钥
        self.verifyKey = verifyKey

        # QQ 号
        self.qq = qq

        # 调用接口
        self.url = 'http://' + host + ':' + port

        # sessionKey
        self.sessionKey = ''

        # requests 请求 session
        self.sess = requests.Session()

    def bind_bot(self):
        '''绑定机器人'''

        data = {
            'verifyKey': self.verifyKey
        }

        res = json.loads(self.sess.post(
            url=(self.url + '/verify'), data=json.dumps(data)).text)

        if res['code'] == 0:
            self.sessionKey = res['session']

            data = {
                'sessionKey': self.sessionKey,
                'qq': self.qq
            }

            res = json.loads(self.sess.post(
                url=(self.url + '/bind'), data=json.dumps(data)).text)

            if res['code'] == 0:
                return True

        return False

    def release_bot(self):
        '''释放机器人'''

        data = {
            'sessionKey': self.sessionKey,
            'qq': self.qq
        }

        res = json.loads(self.sess.post(
            url=(self.url + '/release'), data=json.dumps(data)).text)

        if res['code'] == 0:
            return True

        return False

    def get_friend_list(self):
        '''查看好友列表'''

        res = json.loads(self.sess.get(
            self.url + '/friendList?sessionKey=' + self.sessionKey).text)

        if res['code'] == 0:
            return res['data']

        return False

    def get_group_list(self):
        '''查看群列表'''

        res = json.loads(self.sess.get(
            self.url + '/groupList?sessionKey=' + self.sessionKey).text)

        if res['code'] == 0:
            return res['data']

        return False

    def get_groupmember_list(self, group: int):
        '''查看群成员列表'''

        res = json.loads(self.sess.get(self.url + '/botProfile' +
                         self.sessionKey + '&target=' + str(group)).text)

        if res['code'] == 0:
            return res['data']

        return False

    def get_bot_profile(self):
        '''查看机器人资料'''

        return json.loads(self.sess.get(self.url + '/botProfile?sessionKey=' + self.sessionKey).text)

    def get_friend_profile(self, qq: int):
        '''查看好友资料'''

        return json.loads(self.sess.get(self.url + '/friendProfile?sessionKey=' + self.sessionKey + '&target=' + str(qq)).text)

    def get_groupmember_profile(self, group: int, qq: int):
        '''查看群成员资料'''

        return json.loads(self.sess.get(self.url + '/memberProfile?sessionKey=' + self.sessionKey + '&target=' + str(group) + '&memberId=' + str(qq)).text)

    def send_friend_msg(self, qq: int, messageChain):
        '''发送好友消息'''

        data = {
            'sessionKey': self.sessionKey,
            'target': str(qq),
            'messageChain': messageChain
        }

        res = json.loads(self.sess.post(
            url=(self.url + '/sendFriendMessage'), data=json.dumps(data)).text)

        if res['code'] == 0:
            return res['messageId']

        return False

    def send_group_msg(self, group: int, messageChain: list):
        '''发送群消息'''

        data = {
            'sessionKey': self.sessionKey,
            'target': str(group),
            'messageChain': messageChain
        }

        res = json.loads(self.sess.post(
            url=(self.url + '/sendGroupMessage'), data=json.dumps(data)).text)

        if res['code'] == 0:
            return res['messageId']

        return False

    def send_groupmember_msg(self, group: int, qq: int, messageChain: list):
        '''发送群临时对话消息'''

        data = {
            'sessionKey': self.sessionKey,
            'qq': str(qq),
            'group': str(group),
            'messageChain': messageChain
        }

        res = json.loads(self.sess.post(
            url=(self.url + '/sendGroupMessage'), data=json.dumps(data)).text)

        if res['code'] == 0:
            return res['messageId']

        return False

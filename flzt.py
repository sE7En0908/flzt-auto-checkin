import requests
from notification import TelegramNotification
from env import EMAIL, PASSWORD, LOGIN_URL, USER_INFO_URL, CONVERT_TRAFFIC_URL, CHECK_IN_URL
from loguru import logger


def format_traffic(traffic, s='MB'):
    if s == 'KB':
        return str(round(traffic / 1024, 2)) + 'KB'
    elif s == 'MB':
        return str(round(traffic / 1024 / 1024, 2)) + 'MB'
    elif s == 'GB':
        return str(round(traffic / 1024 / 1024 / 1024, 2)) + 'GB'
    else:
        return str(traffic)


class FLZT:
    def __init__(self, email=None, password=None):
        self.email = email if email else EMAIL
        self.password = password if password else PASSWORD
        self.s = requests.Session()
        self.s.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
        })

    def run(self):
        # 登录
        try:
            r = self.s.post(url=LOGIN_URL, data={
                'email': self.email, 'password': self.password})
            data = r.json()
            token = data['data']['auth_data']
            self.s.headers.update({'Authorization': token})
            logger.info('登录成功')
        except Exception as e:
            logger.error('登录失败', e)
            return
        # 签到
        try:
            r = self.s.get(url=CHECK_IN_URL)
            logger.info(f'签到成功：{r.json()}')
        except Exception as e:
            logger.error('签到失败', e)
            return
        traffic = 0
        # 获取用户信息
        try:
            r = self.s.get(url=USER_INFO_URL)
            data = r.json()
            traffic = int(data['data']['checkin_reward_traffic'])
            logger.info(f'获取用户信息成功，剩余签到流量：{format_traffic(traffic)}')
        except Exception as e:
            logger.error('获取用户信息失败', e)
            return
        # 转换流量
        try:
            r = self.s.post(url=CONVERT_TRAFFIC_URL,
                            data={'transfer': traffic})
            logger.info(f'转换流量: {r.json()}')
        except Exception as e:
            logger.error('转换流量失败', e)
            return
        
        # 触发 Telegram 通知
        notification = TelegramNotification(
            title='FLZT 签到任务', 
            content=f'流量转换成功！\n已转换签到流量：{format_traffic(traffic)}'
        )
        notification.notify()

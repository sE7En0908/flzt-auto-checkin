import requests
from env import TG_BOT_TOKEN, TG_USER_ID
from loguru import logger


class Notification:
    def notify(self):
        pass


class TelegramNotification(Notification):
    def __init__(self, title, content):
        super().__init__()
        self.title = title
        self.content = content

    def notify(self):
        if TG_BOT_TOKEN and TG_USER_ID:
            url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
            # 组合标题和内容，支持 HTML 格式
            text = f"<b>{self.title}</b>\n\n{self.content}"
            payload = {
                'chat_id': TG_USER_ID,
                'text': text,
                'parse_mode': 'HTML'
            }
            try:
                response = requests.post(url, data=payload, timeout=10)
                if response.status_code == 200:
                    logger.info("Telegram 通知发送成功")
                else:
                    logger.error(f"Telegram 通知发送失败: {response.text}")
            except Exception as e:
                logger.error(f"Telegram 通知请求出错: {e}")
        else:
            logger.warning('未设置 TG_BOT_TOKEN 或 TG_USER_ID，跳过通知')

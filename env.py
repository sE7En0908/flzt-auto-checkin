import os
from dotenv import load_dotenv


load_dotenv()
env = os.environ
LOGIN_URL = env['BASE_URL'] + '/api/v1/passport/auth/login'
CHECK_IN_URL = env['BASE_URL'] + '/api/v1/user/checkIn'
USER_INFO_URL = env['BASE_URL'] + '/api/v1/user/info'
CONVERT_TRAFFIC_URL = env['BASE_URL'] + '/api/v1/user/checkIn'
EMAIL = env['EMAIL']
PASSWORD = env['PASSWORD']

# Telegram 配置
TG_BOT_TOKEN = env.get('TG_BOT_TOKEN')
TG_USER_ID = env.get('TG_USER_ID')

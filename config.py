# API_TOKEN тут надо добавить токен бота

URL="212.8.247.152"
PORT="8443"


WEBHOOK_URL_BASE = f'https://{URL}:{PORT}'
WEBHOOK_PATH = f'/{API_TOKEN}/'
WEBHOOK_URL_PATH = f'/{API_TOKEN}/'

WEBHOOK_SSL_CERT = './webhook_cert.pem'
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'

WEBAPP_HOST = f'{URL}' # 127.0.0.1'
WEBAPP_PORT = '8443'

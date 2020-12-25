Телеграм бот на webhook


Можно использовать самоподписанные сертификаты SSL

sudo apt-get install openssl

Cгенерируем приватный и публичный ключи:
openssl genrsa -out webhook_pkey.pem 2048
openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem

Прежде чем стартовать веб хук с веб сервером:
context = ssl.SSLContext()
context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)

Передаём параметрами в метод start_webhook:
start_webhook(..., host=WEBAPP_HOST, port=WEBAPP_PORT, ssl_context=context)

метод стартует и бота на вебхуке и веб сервер.

Всё! Пара-пара-пам!

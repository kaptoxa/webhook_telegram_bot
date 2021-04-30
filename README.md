## Telegram bot via webhook on aiogram without nginx or apache



1). Generate SSL keys:

sudo apt-get install openssl

openssl genrsa -out webhook_pkey.pem 2048

openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem

ACHTUNG! To create a certificate we have to point domain name or ip address

2). Before start webhook:

context = ssl.SSLContext()

context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)

3). Pass as the argument:

start_webhook(..., host=WEBAPP_HOST, port=WEBAPP_PORT, ssl_context=context)


FIN!

4) Maybe it need to load certificate to telegram server

curl -F "url=https://YOU_MEGA_URL" -F "certificate=@bot.pem" https://api.telegram.org/botYOU_TOKEN/setWebhook

## Telegram bot via webhook on aiogram without nginx or apache



1). Generate SSL keys:
sudo apt-get install openssl
openssl genrsa -out webhook_pkey.pem 2048
openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem

2). Before start webhook:
context = ssl.SSLContext()
context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)

3). Pass as the argument:
start_webhook(..., host=WEBAPP_HOST, port=WEBAPP_PORT, ssl_context=context)

FIN!

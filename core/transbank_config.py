# payments/transbank_config.py
from transbank.webpay.webpay_plus.transaction import Transaction

# Configurar el código de comercio y la API key para pruebas
Transaction.commerce_code = "597055555532"
Transaction.api_key_secret = "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C"
Transaction.environment = "TEST"  # Usamos el entorno de pruebas
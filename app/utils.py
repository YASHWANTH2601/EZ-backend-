import jwt
import datetime

def generate_token(data, secret):
    return jwt.encode({'data': data, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, secret, algorithm='HS256')

def decode_token(token, secret):
    try:
        return jwt.decode(token, secret, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

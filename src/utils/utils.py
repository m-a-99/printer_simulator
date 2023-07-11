import jwt
import os
class utils:
    def __init__(self):
        self.__secret_key=os.getenv("JWT_PASSWORD")
    def signjwt(self,payload):
        jwt_token = jwt.encode(payload, self.__secret_key, algorithm='HS256')
        return {"jwt":jwt_token}
    def verify(self,jwt_token):
        try:
            decoded_payload = jwt.decode(jwt_token, self.__secret_key, algorithms=['HS256'])
            # print(decoded_payload)
            return decoded_payload
        except Exception as e:
            raise e
        
            
    
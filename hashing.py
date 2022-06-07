from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class Hash:
    @staticmethod
    def get_hash_password(plain_password):
        pass

    @staticmethod
    def verify_password(plain_password, hashed_password):
        pass

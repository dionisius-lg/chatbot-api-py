from starlette.config import Config

__config = Config(".env")

app = {
    "name": __config("APP_NAME") or "chatbot-api",
    "version": __config("APP_VERSION") or "1.0.0",
    "port": __config("APP_PORT", cast=int, default=9000),
    "reload": True if __config("APP_RELOAD") and __config("APP_RELOAD") == "1" else False
}

database = {
    "host": __config("DB_HOST", default="localhost"),
    "port": __config("DB_PORT", cast=int, default=3306),
    "user": __config("DB_USER", default="root"),
    "password": __config("DB_PASSWORD", default=""),
    "database": __config("DB_NAME", default="test")
}

jwt = {
    "key": __config("JWT_KEY", default=""),
    "expire": __config("JWT_EXPIRE", cast=int, default=0),
    "refresh_key": __config("JWT_REFRESH_KEY", default=""),
    "refresh_expire": __config("JWT_REFRESH_EXPIRE", cast=int, default=0),
    "algorithm": __config("JWT_ALGORITHM", default=""),
    "live": __config("JWT_LIVE", cast=int, default=0)
}

file_dir = __config("FILE_DIR", default="/files")

secret = __config("SECRET", default="")
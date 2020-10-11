from lws_backend.core.config import Config


def get_config() -> Config:
    c = Config(__file__)
    c.setup()
    return c


config = get_config()

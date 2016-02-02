import os
from sonic_app.factory import AppFactory
from sonic_app.settings import DevelopmentConfig,\
    TestConfig, ProductionConfig

configs = {'development': DevelopmentConfig,
           'test': TestConfig,
           'prod': ProductionConfig,
}

config = configs[os.environ.get("ENV", "development")]
app = AppFactory(config=config, name=__name__).get_app()

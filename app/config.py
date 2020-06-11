class Config:
    '''
    General configuration parent class
    '''
    pass



class ProdConfig(Config):
    '''
    Production  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
    QUOTE_API_BASE_URL = 'http://quotes.stormconsultancy.co.uk/random.json'
    pass


class DevConfig(Config):
    '''
    Development  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''

    DEBUG = True
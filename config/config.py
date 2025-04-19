import os
from dotenv import load_dotenv

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        load_dotenv()
        self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
        self.wp_username = os.getenv('WP_USERNAME')
        self.wp_app_pass = os.getenv('WP_APP_PASS')
        self.wp_url = os.getenv('WP_URL')

    def validate_config(self):
        required_vars = [
            ('DEEPSEEK_API_KEY', self.deepseek_api_key),
            ('WP_USERNAME', self.wp_username),
            ('WP_APP_PASS', self.wp_app_pass),
            ('WP_URL', self.wp_url)
        ]
        
        missing_vars = [var for var, value in required_vars if not value]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}") 
import os
from dotenv import load_dotenv
import time

class Config:
    _instance = None

    def __new__(cls):
        if not isinstance(cls._instance, cls):
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        load_dotenv()
        # DeepSeek configuration (optional)
        self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
        
        # Blog platform selection
        self.blog_platform = os.getenv('BLOG_PLATFORM', 'ghost')  # Default to Ghost
        
        # WordPress configuration
        self.wp_username = os.getenv('WP_USERNAME')
        self.wp_app_pass = os.getenv('WP_APP_PASS')
        self.wp_url = os.getenv('WP_URL')
        self.wp_client_id = os.getenv('WP_CLIENT_ID')
        self.wp_client_secret = os.getenv('WP_CLIENT_SECRET')
        
        # Ghost configuration
        self.ghost_url = os.getenv('GHOST_URL')
        self.ghost_api_key = os.getenv('GHOST_API_KEY')
        
        # Schedule configuration
        self.cron_schedule = os.getenv('CRON_SCHEDULE', '00:00')  # Default to midnight UTC if not set
        self.cron_schedules = [time.strip() for time in self.cron_schedule.split(',')]
        
        # Validate time format
        for time_str in self.cron_schedules:
            try:
                hours, minutes = time_str.split(':')
                if not (0 <= int(hours) <= 23 and 0 <= int(minutes) <= 59):
                    raise ValueError(f"Invalid time format in CRON_SCHEDULE: {time_str}")
            except ValueError as e:
                raise ValueError(f"Invalid time format in CRON_SCHEDULE: {time_str}. Expected format: HH:MM in 24-hour format")

    def validate_config(self):
        required_vars = [
            ('BLOG_PLATFORM', self.blog_platform)
        ]
        
        # Add platform-specific required variables
        if self.blog_platform.lower() == 'wordpress':
            # Check if URL is WordPress.org
            is_wordpress_org = '.wordpress.com' in (self.wp_url or '')
            if is_wordpress_org:
                required_vars.extend([
                    ('WP_URL', self.wp_url),
                    ('WP_CLIENT_ID', self.wp_client_id),
                    ('WP_CLIENT_SECRET', self.wp_client_secret)
                ])
            else:
                required_vars.extend([
                    ('WP_USERNAME', self.wp_username),
                    ('WP_APP_PASS', self.wp_app_pass),
                    ('WP_URL', self.wp_url)
                ])
        elif self.blog_platform.lower() == 'ghost':
            required_vars.extend([
                ('GHOST_URL', self.ghost_url),
                ('GHOST_API_KEY', self.ghost_api_key)
            ])
        else:
            raise ValueError(f"Unsupported blog platform: {self.blog_platform}")
        
        missing_vars = [var for var, value in required_vars if not value]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    @classmethod
    def reset_instance(cls):
        """Reset the singleton instance (for testing purposes)"""
        cls._instance = None 
import schedule
import time
import asyncio
from server import run_async_task
from config.config import Config

def main():
    # Initialize configuration
    config = Config()
    config.validate_config()
    
    # Schedule the blog generator for each configured time
    for schedule_time in config.cron_schedules:
        schedule.every().day.at(schedule_time).do(run_async_task)
        print(f"Scheduled task for {schedule_time} UTC")
    
    # Run the scheduler
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
        except Exception as e:
            print(f"Error in scheduler: {str(e)}")
            raise  # Re-raise the exception to propagate it

if __name__ == '__main__':
    main()

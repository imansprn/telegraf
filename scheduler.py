import schedule
import time
import asyncio
import logging
from datetime import datetime, timezone
from server import run_async_task
from config.config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('telegraf-scheduler')

def main():
    try:
        # Initialize configuration
        logger.info("Initializing scheduler...")
        config = Config()
        config.validate_config()
        
        # Schedule the blog generator for each configured time
        for schedule_time in config.cron_schedules:
            schedule.every().day.at(schedule_time).do(run_async_task)
            logger.info(f"Scheduled task for {schedule_time} UTC")
        
        logger.info("Scheduler started successfully")
        
        # Run the scheduler
        while True:
            try:
                now = datetime.now(timezone.utc)
                schedule.run_pending()
                
                # Log next run time
                next_runs = sorted([job.next_run for job in schedule.jobs])
                if next_runs:
                    next_run = next_runs[0]
                    logger.debug(f"Next run scheduled for {next_run} UTC")
                
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"Error in scheduler loop: {str(e)}")
                # Don't raise, just log and continue
                time.sleep(60)  # Wait before retrying
                
    except Exception as e:
        logger.critical(f"Fatal error in scheduler: {str(e)}")
        raise  # Re-raise fatal errors

if __name__ == '__main__':
    main()

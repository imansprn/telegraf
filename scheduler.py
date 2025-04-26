import schedule
import time
import asyncio
import logging
import signal
import sys
from datetime import datetime, timezone
from server import run_async_task
from config.config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('telegraf-scheduler')

def signal_handler(signum, frame):
    logger.info(f"Received signal {signum}. Shutting down gracefully...")
    sys.exit(0)

def main():
    # Set up signal handlers
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

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
                schedule.run_pending()
                
                # Log next run time
                next_runs = sorted([job.next_run for job in schedule.jobs])
                if next_runs:
                    next_run = next_runs[0]
                    logger.debug(f"Next run scheduled for {next_run} UTC")
                
                # Use a shorter sleep interval to be more responsive to signals
                for _ in range(60):
                    time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error in scheduler loop: {str(e)}")
                time.sleep(60)  # Wait before retrying
                
    except Exception as e:
        logger.critical(f"Fatal error in scheduler: {str(e)}")
        sys.exit(1)  # Exit with error code instead of raising

if __name__ == '__main__':
    main()

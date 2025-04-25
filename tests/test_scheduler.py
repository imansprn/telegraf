import pytest
from unittest.mock import Mock, patch, call
import schedule
from scheduler import main
from config.config import Config

@pytest.fixture
def mock_config():
    config = Mock(spec=Config)
    config.cron_schedules = ["00:00", "12:00", "18:00"]
    config.validate_config.return_value = None
    return config

@pytest.fixture
def mock_schedule():
    with patch('scheduler.schedule') as mock_schedule:
        mock_schedule.every.return_value.day.at.return_value.do.return_value = None
        yield mock_schedule

@pytest.fixture
def mock_time():
    with patch('scheduler.time') as mock_time:
        yield mock_time

@pytest.fixture
def mock_run_async_task():
    with patch('scheduler.run_async_task') as mock_task:
        yield mock_task

def test_scheduler_initialization(mock_config, mock_schedule, mock_time, mock_run_async_task):
    """Test that scheduler initializes with correct schedule times"""
    with patch('scheduler.Config', return_value=mock_config):
        # Set up time.sleep to raise exception after first call
        mock_time.sleep.side_effect = [None, Exception("Stop infinite loop")]
        
        with pytest.raises(Exception, match="Stop infinite loop"):
            main()

        # Verify config was validated
        mock_config.validate_config.assert_called_once()

        # Verify schedules were set up correctly
        assert mock_schedule.every.return_value.day.at.call_count == 3
        
        # Verify each schedule time was set
        schedule_calls = [
            call_args[0][0] 
            for call_args in mock_schedule.every.return_value.day.at.call_args_list
        ]
        assert set(schedule_calls) == set(["00:00", "12:00", "18:00"])

        # Verify run_async_task was set as the callback
        assert mock_schedule.every.return_value.day.at.return_value.do.call_count == 3
        for call in mock_schedule.every.return_value.day.at.return_value.do.call_args_list:
            assert call[0][0] == mock_run_async_task

def test_scheduler_error_handling(mock_config, mock_schedule, mock_time):
    """Test that scheduler handles errors gracefully"""
    mock_schedule.run_pending.side_effect = Exception("Test error")
    
    with patch('scheduler.Config', return_value=mock_config):
        with pytest.raises(Exception, match="Test error"):
            main()

        # Verify that the error was logged
        assert mock_time.sleep.call_count == 0  # Should not sleep after error

@pytest.mark.asyncio
async def test_scheduler_integration(mock_config):
    """Test scheduler integration with actual schedule library"""
    with patch('scheduler.Config', return_value=mock_config):
        with patch('scheduler.run_async_task') as mock_task:
            with patch('scheduler.time.sleep') as mock_sleep:
                mock_sleep.side_effect = Exception("Stop infinite loop")
                
                with pytest.raises(Exception, match="Stop infinite loop"):
                    main()
                
                # Verify schedule was created
                jobs = schedule.get_jobs()
                assert len(jobs) == 3
                
                # Clean up schedules
                schedule.clear()

"""
Logging and observability module for KYC Bot.

This module provides structured logging, performance tracking, and observability
features for the multi-agent system.
"""

import logging
import time
import json
from datetime import datetime
from typing import Dict, Any, Optional
from functools import wraps
from contextlib import contextmanager


# Configure structured logging
# Create logs directory if it doesn't exist
import os
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)

# Configure root logger with both file and console handlers
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

# Remove existing handlers to avoid duplicates
root_logger.handlers = []

# Console handler (for immediate feedback)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
console_handler.setFormatter(console_formatter)

# File handler (for persistent logs)
log_file = os.path.join(log_dir, f'kyc_bot_{datetime.now().strftime("%Y%m%d")}.log')
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)  # More detailed logging to file
file_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(file_formatter)

# Add handlers to root logger
root_logger.addHandler(console_handler)
root_logger.addHandler(file_handler)

# Create logger instances for different components
search_logger = logging.getLogger('kyc_bot.search_agent')
watchlist_logger = logging.getLogger('kyc_bot.watchlist_agent')
analysis_logger = logging.getLogger('kyc_bot.analysis_agent')
workflow_logger = logging.getLogger('kyc_bot.workflow')
api_logger = logging.getLogger('kyc_bot.api')


class PerformanceTracker:
    """Track performance metrics for agents and operations."""
    
    def __init__(self):
        self.metrics: Dict[str, Any] = {
            'agent_executions': {},
            'api_calls': {},
            'total_execution_time': 0,
            'start_time': None,
            'end_time': None
        }
    
    def start_investigation(self, customer_name: str):
        """Start tracking a new investigation."""
        self.metrics['start_time'] = time.time()
        self.metrics['customer_name'] = customer_name
        self.metrics['agent_executions'] = {}
        self.metrics['api_calls'] = {}
        workflow_logger.info(f"Starting investigation for: {customer_name}")
    
    def end_investigation(self):
        """End tracking and calculate total time."""
        self.metrics['end_time'] = time.time()
        if self.metrics['start_time']:
            self.metrics['total_execution_time'] = (
                self.metrics['end_time'] - self.metrics['start_time']
            )
            workflow_logger.info(
                f"Investigation completed in {self.metrics['total_execution_time']:.2f} seconds"
            )
    
    def track_agent_execution(self, agent_name: str, execution_time: float, 
                             success: bool = True, error: Optional[str] = None):
        """Track agent execution time and status."""
        if agent_name not in self.metrics['agent_executions']:
            self.metrics['agent_executions'][agent_name] = {
                'executions': [],
                'total_time': 0,
                'success_count': 0,
                'error_count': 0
            }
        
        execution_data = {
            'timestamp': datetime.now().isoformat(),
            'execution_time': execution_time,
            'success': success,
            'error': error
        }
        
        self.metrics['agent_executions'][agent_name]['executions'].append(execution_data)
        self.metrics['agent_executions'][agent_name]['total_time'] += execution_time
        
        if success:
            self.metrics['agent_executions'][agent_name]['success_count'] += 1
        else:
            self.metrics['agent_executions'][agent_name]['error_count'] += 1
    
    def track_api_call(self, api_name: str, endpoint: str, success: bool = True,
                      response_time: Optional[float] = None, error: Optional[str] = None):
        """Track API calls and their performance."""
        if api_name not in self.metrics['api_calls']:
            self.metrics['api_calls'][api_name] = {
                'calls': [],
                'total_calls': 0,
                'success_count': 0,
                'error_count': 0,
                'total_response_time': 0
            }
        
        call_data = {
            'timestamp': datetime.now().isoformat(),
            'endpoint': endpoint,
            'success': success,
            'response_time': response_time,
            'error': error
        }
        
        self.metrics['api_calls'][api_name]['calls'].append(call_data)
        self.metrics['api_calls'][api_name]['total_calls'] += 1
        
        if success:
            self.metrics['api_calls'][api_name]['success_count'] += 1
        else:
            self.metrics['api_calls'][api_name]['error_count'] += 1
        
        if response_time:
            self.metrics['api_calls'][api_name]['total_response_time'] += response_time
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of all metrics."""
        summary = {
            'customer_name': self.metrics.get('customer_name'),
            'total_execution_time': self.metrics.get('total_execution_time', 0),
            'agents': {},
            'apis': {}
        }
        
        # Agent summaries
        for agent_name, data in self.metrics['agent_executions'].items():
            summary['agents'][agent_name] = {
                'total_executions': len(data['executions']),
                'total_time': data['total_time'],
                'average_time': (
                    data['total_time'] / len(data['executions']) 
                    if data['executions'] else 0
                ),
                'success_count': data['success_count'],
                'error_count': data['error_count']
            }
        
        # API summaries
        for api_name, data in self.metrics['api_calls'].items():
            summary['apis'][api_name] = {
                'total_calls': data['total_calls'],
                'success_count': data['success_count'],
                'error_count': data['error_count'],
                'average_response_time': (
                    data['total_response_time'] / data['total_calls']
                    if data['total_calls'] > 0 else 0
                )
            }
        
        return summary
    
    def log_summary(self):
        """Log a formatted summary of all metrics."""
        summary = self.get_summary()
        workflow_logger.info("=" * 60)
        workflow_logger.info("PERFORMANCE METRICS SUMMARY")
        workflow_logger.info("=" * 60)
        workflow_logger.info(f"Customer: {summary['customer_name']}")
        workflow_logger.info(f"Total Execution Time: {summary['total_execution_time']:.2f}s")
        workflow_logger.info("")
        workflow_logger.info("Agent Performance:")
        for agent_name, data in summary['agents'].items():
            workflow_logger.info(
                f"  {agent_name}: "
                f"{data['total_executions']} executions, "
                f"{data['average_time']:.2f}s avg, "
                f"{data['success_count']} success, "
                f"{data['error_count']} errors"
            )
        workflow_logger.info("")
        workflow_logger.info("API Performance:")
        for api_name, data in summary['apis'].items():
            workflow_logger.info(
                f"  {api_name}: "
                f"{data['total_calls']} calls, "
                f"{data['average_response_time']:.2f}s avg, "
                f"{data['success_count']} success, "
                f"{data['error_count']} errors"
            )
        workflow_logger.info("=" * 60)
        
        # Also print to console for visibility
        print("\n[PERFORMANCE METRICS]")
        print(f"  Total Time: {summary['total_execution_time']:.2f}s")
        for agent_name, data in summary['agents'].items():
            print(f"  {agent_name}: {data['average_time']:.2f}s avg")
        for api_name, data in summary['apis'].items():
            print(f"  {api_name}: {data['average_response_time']:.2f}s avg")
        print(f"  Log file: {log_file}")


# Global performance tracker instance
performance_tracker = PerformanceTracker()


@contextmanager
def track_execution(agent_name: str, logger: logging.Logger):
    """Context manager to track agent execution time."""
    start_time = time.time()
    logger.info(f"{agent_name} execution started")
    try:
        yield
        execution_time = time.time() - start_time
        performance_tracker.track_agent_execution(agent_name, execution_time, success=True)
        logger.info(f"{agent_name} execution completed in {execution_time:.2f}s")
    except Exception as e:
        execution_time = time.time() - start_time
        performance_tracker.track_agent_execution(
            agent_name, execution_time, success=False, error=str(e)
        )
        logger.error(f"{agent_name} execution failed after {execution_time:.2f}s: {str(e)}")
        raise


@contextmanager
def track_api_call(api_name: str, endpoint: str, logger: logging.Logger):
    """Context manager to track API calls."""
    start_time = time.time()
    logger.info(f"API call started: {api_name} - {endpoint}")
    try:
        yield
        response_time = time.time() - start_time
        performance_tracker.track_api_call(
            api_name, endpoint, success=True, response_time=response_time
        )
        logger.info(f"API call completed: {api_name} - {endpoint} ({response_time:.2f}s)")
    except Exception as e:
        response_time = time.time() - start_time
        performance_tracker.track_api_call(
            api_name, endpoint, success=False, 
            response_time=response_time, error=str(e)
        )
        logger.error(f"API call failed: {api_name} - {endpoint} ({response_time:.2f}s): {str(e)}")
        raise


def log_search_query(logger: logging.Logger, customer_name: str, query: str):
    """Log a search query."""
    logger.info(f"Search query for '{customer_name}': {query}")


def log_search_results(logger: logging.Logger, query: str, result_count: int, 
                      is_real: bool = True):
    """Log search results."""
    result_type = "real" if is_real else "simulated"
    logger.info(f"Search query '{query}' returned {result_count} {result_type} results")


def log_watchlist_check(logger: logging.Logger, customer_name: str, 
                       watchlists_checked: list, matches: list):
    """Log watchlist check results."""
    logger.info(
        f"Watchlist check for '{customer_name}': "
        f"{len(watchlists_checked)} watchlists checked, "
        f"{len(matches)} matches found"
    )
    if matches:
        logger.warning(f"Watchlist matches found: {matches}")


def log_report_generation(logger: logging.Logger, customer_name: str, 
                         report_length: int, risk_level: Optional[str] = None):
    """Log report generation."""
    logger.info(
        f"Report generated for '{customer_name}': "
        f"{report_length} characters"
    )
    if risk_level:
        logger.info(f"Risk level assessed: {risk_level}")


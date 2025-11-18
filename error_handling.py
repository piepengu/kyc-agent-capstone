"""
Error handling utilities for the KYC Bot system.

Provides retry logic, error classification, and user-friendly error messages.
"""

import time
import logging
from typing import Callable, Any, Optional, Tuple
from functools import wraps
from googleapiclient.errors import HttpError

logger = logging.getLogger('kyc_bot.error_handling')


class RetryableError(Exception):
    """Exception that indicates an operation can be retried."""
    pass


class NonRetryableError(Exception):
    """Exception that indicates an operation should not be retried."""
    pass


def classify_error(error: Exception) -> Tuple[bool, str]:
    """
    Classify an error to determine if it's retryable and provide a user-friendly message.
    
    Args:
        error: The exception that occurred
        
    Returns:
        Tuple of (is_retryable, user_message)
    """
    error_str = str(error).lower()
    error_type = type(error).__name__
    
    # HTTP errors from Google APIs
    if isinstance(error, HttpError):
        status_code = error.resp.status if hasattr(error, 'resp') else None
        
        # Rate limiting (429) - retryable
        if status_code == 429:
            return True, "API rate limit exceeded. Please wait a moment and try again."
        
        # Server errors (5xx) - retryable
        if status_code and 500 <= status_code < 600:
            return True, f"Server error (HTTP {status_code}). The service may be temporarily unavailable."
        
        # Client errors (4xx) - mostly non-retryable
        if status_code and 400 <= status_code < 500:
            if status_code == 403:
                return False, "API access denied. Please check your API key permissions and restrictions."
            elif status_code == 404:
                return False, "Resource not found. Please verify your configuration."
            elif status_code == 401:
                return False, "Authentication failed. Please check your API key."
            else:
                return False, f"Client error (HTTP {status_code}). Please check your request."
    
    # Network/timeout errors - retryable
    if any(keyword in error_str for keyword in ['timeout', 'connection', 'network', 'unreachable']):
        return True, "Network error. Please check your internet connection and try again."
    
    # Rate limit keywords - retryable
    if any(keyword in error_str for keyword in ['rate limit', 'quota', 'too many requests']):
        return True, "API rate limit exceeded. Please wait a moment and try again."
    
    # Permission/authentication errors - non-retryable
    if any(keyword in error_str for keyword in ['permission', 'unauthorized', 'forbidden', 'api key']):
        return False, "Authentication or permission error. Please check your API key and permissions."
    
    # Default: non-retryable
    return False, f"An error occurred: {str(error)}"


def retry_with_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    max_delay: float = 10.0,
    retryable_exceptions: tuple = (Exception,)
):
    """
    Decorator to retry a function with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        backoff_factor: Multiplier for delay after each retry
        max_delay: Maximum delay between retries
        retryable_exceptions: Tuple of exception types that should be retried
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            delay = initial_delay
            last_error = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except retryable_exceptions as e:
                    last_error = e
                    is_retryable, user_message = classify_error(e)
                    
                    if not is_retryable or attempt >= max_retries:
                        # Don't retry or out of retries
                        logger.error(f"{func.__name__} failed after {attempt + 1} attempts: {user_message}")
                        raise NonRetryableError(user_message) from e
                    
                    # Log retry attempt
                    logger.warning(
                        f"{func.__name__} failed (attempt {attempt + 1}/{max_retries + 1}): {user_message}. "
                        f"Retrying in {delay:.1f}s..."
                    )
                    
                    time.sleep(delay)
                    delay = min(delay * backoff_factor, max_delay)
            
            # Should not reach here, but just in case
            if last_error:
                raise NonRetryableError(f"Operation failed after {max_retries + 1} attempts: {str(last_error)}") from last_error
            
        return wrapper
    return decorator


def handle_api_error(operation_name: str, error: Exception, fallback_value: Any = None) -> Tuple[Any, str]:
    """
    Handle an API error and return a fallback value with a user-friendly message.
    
    Args:
        operation_name: Name of the operation that failed
        error: The exception that occurred
        fallback_value: Value to return if error is handled gracefully
        
    Returns:
        Tuple of (result, error_message)
    """
    is_retryable, user_message = classify_error(error)
    
    logger.error(f"{operation_name} failed: {user_message}")
    
    if fallback_value is not None:
        logger.info(f"Using fallback value for {operation_name}")
        return fallback_value, user_message
    
    raise error


def validate_customer_name(name: str) -> Tuple[bool, Optional[str]]:
    """
    Validate a customer name input.
    
    Args:
        name: Customer name to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name or not isinstance(name, str):
        return False, "Customer name must be a non-empty string."
    
    name = name.strip()
    
    if len(name) < 2:
        return False, "Customer name must be at least 2 characters long."
    
    if len(name) > 200:
        return False, "Customer name must be less than 200 characters."
    
    # Check for potentially dangerous characters (basic sanitization)
    dangerous_chars = ['<', '>', '{', '}', '[', ']', '|', '\\', '/', '\0']
    if any(char in name for char in dangerous_chars):
        return False, "Customer name contains invalid characters."
    
    return True, None


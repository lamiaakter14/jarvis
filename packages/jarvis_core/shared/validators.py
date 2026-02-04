"""Shared validators for the JARVIS application."""

from typing import Any, Optional
import re
from jarvis_core.shared.exceptions import ValidationError


def validate_not_empty(value: Any, field_name: str) -> None:
    """Validate that a value is not empty.
    
    Args:
        value: Value to validate
        field_name: Name of the field for error messages
        
    Raises:
        ValidationError: If value is empty
    """
    if not value:
        raise ValidationError(f"{field_name} cannot be empty")


def validate_string_length(
    value: str, 
    field_name: str, 
    min_length: Optional[int] = None, 
    max_length: Optional[int] = None
) -> None:
    """Validate string length.
    
    Args:
        value: String to validate
        field_name: Name of the field for error messages
        min_length: Minimum allowed length
        max_length: Maximum allowed length
        
    Raises:
        ValidationError: If string length is invalid
    """
    if min_length is not None and len(value) < min_length:
        raise ValidationError(
            f"{field_name} must be at least {min_length} characters long"
        )
    if max_length is not None and len(value) > max_length:
        raise ValidationError(
            f"{field_name} must be at most {max_length} characters long"
        )


def validate_positive_number(value: float, field_name: str) -> None:
    """Validate that a number is positive.
    
    Args:
        value: Number to validate
        field_name: Name of the field for error messages
        
    Raises:
        ValidationError: If number is not positive
    """
    if value <= 0:
        raise ValidationError(f"{field_name} must be positive")


def validate_range(
    value: float, 
    field_name: str, 
    min_value: Optional[float] = None, 
    max_value: Optional[float] = None
) -> None:
    """Validate that a number is within a range.
    
    Args:
        value: Number to validate
        field_name: Name of the field for error messages
        min_value: Minimum allowed value
        max_value: Maximum allowed value
        
    Raises:
        ValidationError: If number is out of range
    """
    if min_value is not None and value < min_value:
        raise ValidationError(
            f"{field_name} must be at least {min_value}"
        )
    if max_value is not None and value > max_value:
        raise ValidationError(
            f"{field_name} must be at most {max_value}"
        )


def validate_email(email: str) -> None:
    """Validate email format.
    
    Args:
        email: Email address to validate
        
    Raises:
        ValidationError: If email format is invalid
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationError("Invalid email format")


def validate_enum(value: str, enum_class: type, field_name: str) -> None:
    """Validate that a value is a valid enum member.
    
    Args:
        value: Value to validate
        enum_class: Enum class to check against
        field_name: Name of the field for error messages
        
    Raises:
        ValidationError: If value is not a valid enum member
    """
    valid_values = [e.value for e in enum_class]
    if value not in valid_values:
        raise ValidationError(
            f"{field_name} must be one of: {', '.join(valid_values)}"
        )

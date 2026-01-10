import re
from typing import Tuple

class ValidationHelper:
    """Helper class for input validation"""
    
    # Email regex pattern (RFC 5322 simplified)
    EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    @staticmethod
    def is_valid_email(email: str) -> Tuple[bool, str]:
        """
        Validate email format.
        
        Args:
            email: Email address to validate
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not email or len(email.strip()) == 0:
            return False, "Email address cannot be empty"
        
        email = email.strip()
        
        if len(email) > 150:
            return False, "Email address too long (maximum 150 characters)"
        
        if not re.match(ValidationHelper.EMAIL_PATTERN, email):
            return False, "Invalid email format. Please provide a valid email address"
        
        return True, ""
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        """
        Validate password strength.
        
        Args:
            password: Password to validate
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not password:
            return False, "Password cannot be empty"
        
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        # Check for at least one uppercase letter
        if not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"
        
        # Check for at least one lowercase letter
        if not any(c.islower() for c in password):
            return False, "Password must contain at least one lowercase letter"
        
        # Check for at least one digit
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one digit"
        
        return True, ""

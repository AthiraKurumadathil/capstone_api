import hashlib
import secrets
import string
from typing import Tuple

class PasswordHelper:
    """Helper class for password generation, hashing, and validation"""
    
    @staticmethod
    def generate_random_password(length: int = 12) -> str:
        """
        Generate a random secure password.
        
        Args:
            length: Length of password (default: 12)
        
        Returns:
            Random password string containing uppercase, lowercase, digits, and special chars
        """
        # Define character sets
        uppercase = string.ascii_uppercase
        lowercase = string.ascii_lowercase
        digits = string.digits
        special_chars = "!@#$%^&*-_=+"
        
        # Ensure at least one character from each set
        password_chars = [
            secrets.choice(uppercase),
            secrets.choice(lowercase),
            secrets.choice(digits),
            secrets.choice(special_chars)
        ]
        
        # Fill remaining length with random characters from all sets
        all_chars = uppercase + lowercase + digits + special_chars
        for _ in range(length - 4):
            password_chars.append(secrets.choice(all_chars))
        
        # Shuffle to avoid predictable patterns
        secrets.SystemRandom().shuffle(password_chars)
        
        return ''.join(password_chars)
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash password using SHA256.
        
        Args:
            password: Plain text password
        
        Returns:
            SHA256 hashed password
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify if plain password matches hashed password.
        
        Args:
            plain_password: Plain text password to verify
            hashed_password: SHA256 hashed password from database
        
        Returns:
            True if password matches, False otherwise
        """
        return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password
    
    @staticmethod
    def generate_and_hash_password(length: int = 12) -> Tuple[str, str]:
        """
        Generate a random password and return both plain and hashed versions.
        
        Args:
            length: Length of password to generate (default: 12)
        
        Returns:
            Tuple of (plain_password, hashed_password)
        """
        plain_password = PasswordHelper.generate_random_password(length)
        hashed_password = PasswordHelper.hash_password(plain_password)
        return plain_password, hashed_password

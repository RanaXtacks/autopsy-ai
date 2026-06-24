import logging
from typing import Optional, Tuple
from werkzeug.security import generate_password_hash, check_password_hash
from app.repositories import UserRepository
from app.validators import AuthValidator
from app.models import User
from flask_jwt_extended import create_access_token, create_refresh_token
from app import db
from app.models import TokenBlocklist

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.validator = AuthValidator()
    
    def register_user(self, username: str, email: str, password: str) -> Tuple[Optional[User], Optional[str]]:
        """
        Register a new user
        Returns (user, error_message)
        """
        username = username.strip()
        email = email.strip()
        
        # Check for duplicate username
        if self.user_repo.get_by_username(username):
            logger.warning(f"Registration failed: username {username} already exists")
            return None, "Username already exists"
        
        # Check for duplicate email
        if self.user_repo.get_by_email(email):
            logger.warning(f"Registration failed: email {email} already exists")
            return None, "Email already exists"
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        
        try:
            self.user_repo.create(user)
            logger.info(f"User registered successfully: {username}")
            return user, None
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}", exc_info=True)
            return None, "Failed to create user"
    
    def login_user(self, email: str, password: str) -> Tuple[Optional[str], Optional[str], Optional[User], Optional[str]]:
        """
        Login a user with email and password
        Returns (access_token, refresh_token, user, error_message)
        """
        email = email.strip()
        
        # Get user by email (non-informative error to prevent enumeration)
        user = self.user_repo.get_by_email(email)
        
        # Constant-time comparison check
        if user and user.check_password(password):
            access_token = create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))
            logger.info(f"User logged in successfully: {email}")
            return access_token, refresh_token, user, None
        else:
            logger.warning(f"Failed login attempt for email: {email}")
            return None, None, None, "Invalid credentials"
    
    def get_user_profile(self, user_id: int) -> Optional[User]:
        """Get user profile by ID"""
        return self.user_repo.get_by_id(user_id)

    def revoke_token(self, jti: str, token_type: str, user_id: int, expires) -> bool:
        """Add a token to the blocklist"""
        try:
            blocklist_entry = TokenBlocklist(
                jti=jti,
                token_type=token_type,
                user_id=user_id,
                expires=expires
            )
            db.session.add(blocklist_entry)
            db.session.commit()
            logger.info(f"Token revoked successfully for user_id: {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error revoking token: {str(e)}", exc_info=True)
            db.session.rollback()
            return False

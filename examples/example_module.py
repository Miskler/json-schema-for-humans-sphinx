"""
Example module demonstrating the Sphinx extension.
"""

from typing import Dict, Any, List, Optional


class User:
    """User management class."""
    
    def __init__(self, name: str, email: str):
        """Initialize a new user."""
        self.name = name
        self.email = email
        self.active = True
        self.roles = []
    
    def create(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new user.
        
        This method creates a new user with the provided data.
        The schema for this method is automatically loaded from
        ``User.create.schema.json``.
        
        Args:
            user_data: User data dictionary
            
        Returns:
            Created user information
        """
        return {
            "id": 1,
            "name": user_data["name"],
            "email": user_data["email"],
            "active": user_data.get("active", True),
            "roles": user_data.get("roles", [])
        }
    
    def update(self, user_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing user.
        
        This method updates user information with the provided data.
        The schema for this method is automatically loaded from
        ``User.update.schema.json``.
        
        Args:
            user_id: ID of the user to update
            update_data: Data to update
            
        Returns:
            Updated user information
        """
        return {
            "id": user_id,
            "updated_fields": list(update_data.keys())
        }


    def example(self) -> Dict[str, Any]:
        """
        Get an example user object.
        
        This method returns an example user object structure.
        The example data is automatically loaded from
        ``User.example.json``.
        
        Returns:
            Example user object
        """
        return {
            "id": 123,
            "name": "John Doe",
            "email": "john.doe@example.com",
            "active": True,
            "roles": ["user", "admin"]
        }


def process_data(data: List[Dict[str, Any]], options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Process input data according to specified options.
    
    This function processes input data and returns the results.
    The schema for this function is automatically loaded from
    ``process_data.schema.json``.
    
    Args:
        data: Input data to process
        options: Processing options
        
    Returns:
        Processing results
    """
    if options is None:
        options = {}
    
    return {
        "processed_count": len(data),
        "format": options.get("format", "json"),
        "validated": options.get("validate", True)
    }

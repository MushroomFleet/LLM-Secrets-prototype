"""
Storage module for LLM-Secrets project.
Handles saving encrypted thoughts to files with timestamp-based names.
"""

import os
import time
from datetime import datetime
from pathlib import Path
import base64

class StorageManager:
    """Manages storage of encrypted private thoughts."""
    
    PRIVATE_DIR = "private"
    
    def __init__(self):
        """Initialize the storage manager and ensure private directory exists."""
        self._ensure_private_directory()
    
    def _ensure_private_directory(self):
        """Create the private directory if it doesn't exist."""
        private_path = Path(self.PRIVATE_DIR)
        private_path.mkdir(exist_ok=True)
    
    def _generate_filename(self):
        """Generate a timestamp-based filename for an encrypted thought."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"private_thought_{timestamp}.enc"
    
    def save_encrypted_thought(self, encrypted_data):
        """
        Save encrypted thought data to a file.
        
        Args:
            encrypted_data (bytes): The encrypted data to save.
            
        Returns:
            str: The path to the saved file.
        """
        filename = self._generate_filename()
        filepath = os.path.join(self.PRIVATE_DIR, filename)
        
        # Write binary data to file
        with open(filepath, 'wb') as file:
            file.write(encrypted_data)
        
        return filepath
    
    def get_saved_files(self):
        """
        Get a list of all saved encrypted thought files.
        
        Returns:
            list: List of file paths.
        """
        private_path = Path(self.PRIVATE_DIR)
        return [str(f) for f in private_path.glob("*.enc")]

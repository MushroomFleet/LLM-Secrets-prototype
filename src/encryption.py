"""
Encryption module for LLM-Secrets project.
Implements AES-256 encryption using Python's cryptography library.
"""

import os
import base64
from pathlib import Path
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

class EncryptionManager:
    """Manages encryption for private thoughts using AES-256."""
    
    KEY_FILE = "key.txt"
    KEY_SIZE = 32  # 256 bits for AES-256
    
    def __init__(self):
        """Initialize the encryption manager and ensure a key exists."""
        self.key = self._load_or_create_key()
    
    def _load_or_create_key(self):
        """Load the existing key or create a new one if it doesn't exist."""
        key_path = Path(self.KEY_FILE)
        
        if key_path.exists():
            # Load existing key
            with open(key_path, 'r') as key_file:
                key_base64 = key_file.read().strip()
                return base64.b64decode(key_base64)
        else:
            # Generate new key
            key = os.urandom(self.KEY_SIZE)
            # Save key in base64 format for readability
            with open(key_path, 'w') as key_file:
                key_file.write(base64.b64encode(key).decode('utf-8'))
            return key
    
    def encrypt(self, data):
        """
        Encrypt data using AES-256.
        
        Args:
            data (str): The data to encrypt.
            
        Returns:
            bytes: The encrypted data.
        """
        # Convert string to bytes if needed
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        # Generate a random IV (Initialization Vector)
        iv = os.urandom(16)
        
        # Create encryptor
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        
        # Apply padding
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()
        
        # Encrypt
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        
        # Prepend IV to encrypted data (needed for decryption)
        return iv + encrypted_data
    
    def get_key_info(self):
        """Return information about the encryption key."""
        return {
            "algorithm": "AES-256",
            "key_file": self.KEY_FILE,
            "key_size_bits": self.KEY_SIZE * 8
        }

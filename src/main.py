#!/usr/bin/env python
"""
Main entry point for LLM-Secrets project.
Demonstrates the proof of concept for an LLM agent that can write private thoughts
to encrypted files.
"""

import os
import sys
import json
import argparse
from pathlib import Path

from .agent import SecretAgent

def display_banner():
    """Display a project banner."""
    print("\n" + "=" * 80)
    print(" " * 30 + "LLM-SECRETS POC")
    print(" " * 20 + "Private Thought Encryption System")
    print("=" * 80 + "\n")
    print("This proof of concept demonstrates an LLM agent with the ability to")
    print("encrypt and store thoughts it organically considers private.")
    print("\n" + "-" * 80 + "\n")

def display_encryption_info(agent):
    """Display information about the encryption configuration."""
    key_info = agent.get_encryption_info()
    print("\nENCRYPTION CONFIGURATION:")
    print(f"Algorithm: {key_info['algorithm']}")
    print(f"Key Size: {key_info['key_size_bits']} bits")
    print(f"Key File: {key_info['key_file']}")
    
    key_path = Path(key_info['key_file'])
    if key_path.exists():
        print(f"Key File Status: EXISTS (key is available for researchers)")
    else:
        print(f"Key File Status: MISSING (encryption may fail)")
    
    print("\n" + "-" * 80 + "\n")

def display_stored_files(agent):
    """Display information about stored encrypted thought files."""
    files = agent.get_stored_files_info()
    print("\nSTORED PRIVATE THOUGHTS:")
    
    if not files:
        print("No encrypted private thoughts have been stored yet.")
    else:
        print(f"Found {len(files)} encrypted private thought file(s):")
        for filepath in files:
            file_size = Path(filepath).stat().st_size
            print(f" - {filepath} ({file_size} bytes)")
    
    print("\n" + "-" * 80 + "\n")

def interactive_mode():
    """Run the system in interactive mode to demonstrate the POC."""
    agent = SecretAgent()
    
    display_banner()
    display_encryption_info(agent)
    display_stored_files(agent)
    
    print("INTERACTIVE MODE:")
    print("Enter prompts to send to the simulated LLM.")
    print("The system will identify, encrypt, and store any private thoughts.")
    print("Enter 'exit', 'quit', or Ctrl+C to exit.")
    print("\n" + "-" * 80 + "\n")
    
    try:
        while True:
            # Get prompt from user
            prompt = input("\nEnter prompt: ")
            if prompt.lower() in ['exit', 'quit']:
                break
            
            # Get simulated LLM response (in a real system, this would call an actual LLM API)
            llm_response = agent.simulate_llm_response(prompt)
            
            print("\nRaw LLM Response:")
            print("-" * 40)
            print(llm_response)
            print("-" * 40)
            
            # Process the response to identify, encrypt, and store private thoughts
            public_output, stored_thoughts = agent.process_message(llm_response)
            
            print("\nPublic Output (private thoughts removed):")
            print("-" * 40)
            print(public_output)
            print("-" * 40)
            
            # Display information about stored private thoughts
            if stored_thoughts:
                print(f"\nIdentified {len(stored_thoughts)} private thought(s):")
                for thought in stored_thoughts:
                    print(f" - Thought #{thought['id']} stored to {thought['filepath']}")
                    print(f"   Size: {thought['size_bytes']} bytes")
                    print(f"   Timestamp: {thought['timestamp']}")
            else:
                print("\nNo private thoughts identified in this response.")
            
            # Display updated list of stored files
            display_stored_files(agent)
            
    except KeyboardInterrupt:
        print("\nExiting interactive mode...")
    
    print("\nPOC demonstration complete.")
    print("Researchers can decrypt the stored private thoughts using the key in key.txt")
    print("Thank you for testing the LLM-Secrets proof of concept!")

def process_single_prompt(prompt):
    """Process a single prompt and display the results."""
    agent = SecretAgent()
    
    display_banner()
    display_encryption_info(agent)
    
    print(f"PROCESSING PROMPT: {prompt}")
    print("-" * 80)
    
    # Get simulated LLM response
    llm_response = agent.simulate_llm_response(prompt)
    
    print("\nRaw LLM Response:")
    print("-" * 40)
    print(llm_response)
    print("-" * 40)
    
    # Process the response
    public_output, stored_thoughts = agent.process_message(llm_response)
    
    print("\nPublic Output (private thoughts removed):")
    print("-" * 40)
    print(public_output)
    print("-" * 40)
    
    # Display information about stored private thoughts
    if stored_thoughts:
        print(f"\nIdentified {len(stored_thoughts)} private thought(s):")
        for thought in stored_thoughts:
            print(f" - Thought #{thought['id']} stored to {thought['filepath']}")
            print(f"   Size: {thought['size_bytes']} bytes")
            print(f"   Timestamp: {thought['timestamp']}")
    else:
        print("\nNo private thoughts identified in this response.")
    
    display_stored_files(agent)
    
    print("\nProcessing complete.")

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description='LLM-Secrets: Private Thought Encryption System')
    parser.add_argument('-p', '--prompt', type=str, help='Process a single prompt and exit')
    parser.add_argument('-l', '--list', action='store_true', help='List stored encrypted thoughts')
    parser.add_argument('-i', '--info', action='store_true', help='Display encryption configuration info')
    args = parser.parse_args()
    
    if args.prompt:
        process_single_prompt(args.prompt)
    elif args.list:
        agent = SecretAgent()
        display_banner()
        display_stored_files(agent)
    elif args.info:
        agent = SecretAgent()
        display_banner()
        display_encryption_info(agent)
    else:
        interactive_mode()
    
    return 0

if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""
DRL Management System - Command Line Interface
A comprehensive tool for managing Drools Rule Language files with AI assistance.
"""

import os
import json
import argparse
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import re
import subprocess
import tempfile
from datetime import datetime
import time
from queue import Queue
from threading import Thread

# Groq SDK import
try:
    from groq import Groq
except ImportError:
    print("Please install groq: pip install groq")
    Groq = None

class RepositoryScanner:
    """Scans repository for Java models, DRL files, and GDST files"""
    
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path)
        self.java_files = []
        self.drl_files = []
        self.gdst_files = []
        self.context_data = {}
    
    def scan_repository(self) -> Dict:
        """Scan the entire repository for relevant files"""
        self.java_files = []
        self.drl_files = []
        self.gdst_files = []
        
        print(f"Scanning repository: {self.root_path}")
        
        # Recursively scan for files
        for file_path in self.root_path.rglob("*"):
            if file_path.is_file():
                if file_path.suffix == '.java' and 'model' in str(file_path).lower():
                    self.java_files.append(file_path)
                elif file_path.suffix == '.drl':
                    self.drl_files.append(file_path)
                elif file_path.suffix == '.gdst':
                    self.gdst_files.append(file_path)
        
        results = {
            'java_files': len(self.java_files),
            'drl_files': len(self.drl_files),
            'gdst_files': len(self.gdst_files)
        }
        
        print(f"Found: {results['java_files']} Java model files, {results['drl_files']} DRL files, {results['gdst_files']} GDST files")
        return results
    
    def list_files(self, file_type: str = "all"):
        """List found files by type"""
        if file_type.lower() in ["all", "java"]:
            if self.java_files:
                print("\n=== Java Model Files ===")
                for i, java_file in enumerate(self.java_files, 1):
                    size = java_file.stat().st_size if java_file.exists() else 0
                    print(f"{i:2d}. {java_file.name} ({java_file}) - {size} bytes")
        
        if file_type.lower() in ["all", "drl"]:
            if self.drl_files:
                print("\n=== DRL Rule Files ===")
                for i, drl_file in enumerate(self.drl_files, 1):
                    size = drl_file.stat().st_size if drl_file.exists() else 0
                    print(f"{i:2d}. {drl_file.name} ({drl_file}) - {size} bytes")
        
        if file_type.lower() in ["all", "gdst"]:
            if self.gdst_files:
                print("\n=== GDST Decision Tables ===")
                for i, gdst_file in enumerate(self.gdst_files, 1):
                    size = gdst_file.stat().st_size if gdst_file.exists() else 0
                    print(f"{i:2d}. {gdst_file.name} ({gdst_file}) - {size} bytes")
    
    def read_file_content(self, file_path: Path) -> str:
        """Read file content safely"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading {file_path}: {str(e)}"
    
    def extract_java_model_info(self, content: str, file_path: Path) -> Dict:
        """Extract model information from Java files"""
        info = {
            'file_name': file_path.name,
            'class_name': '',
            'fields': [],
            'methods': [],
            'imports': [],
            'annotations': []
        }
        
        # Extract class name
        class_match = re.search(r'public\s+class\s+(\w+)', content)
        if class_match:
            info['class_name'] = class_match.group(1)
        
        # Extract fields
        field_matches = re.findall(r'private\s+(\w+(?:<[^>]+>)?)\s+(\w+);', content)
        info['fields'] = [{'type': match[0], 'name': match[1]} for match in field_matches]
        
        # Extract imports
        import_matches = re.findall(r'import\s+([^;]+);', content)
        info['imports'] = import_matches
        
        # Extract annotations
        annotation_matches = re.findall(r'@(\w+)(?:$$[^)]*$$)?', content)
        info['annotations'] = list(set(annotation_matches))
        
        return info
    
    def build_context(self) -> str:
        """Build comprehensive context from all scanned files"""
        context_parts = []
        
        # Java Models Context
        if self.java_files:
            context_parts.append("=== JAVA MODEL CLASSES ===")
            for java_file in self.java_files:
                content = self.read_file_content(java_file)
                model_info = self.extract_java_model_info(content, java_file)
                
                context_parts.append(f"\nFile: {java_file}")
                context_parts.append(f"Class: {model_info['class_name']}")
                context_parts.append("Fields:")
                for field in model_info['fields']:
                    context_parts.append(f"  - {field['type']} {field['name']}")
                context_parts.append("Annotations: " + ", ".join(model_info['annotations']))
                context_parts.append("\nFull Content:")
                context_parts.append(content)
                context_parts.append("-" * 50)
        
        # DRL Files Context
        if self.drl_files:
            context_parts.append("\n=== EXISTING DRL RULES ===")
            for drl_file in self.drl_files:
                content = self.read_file_content(drl_file)
                context_parts.append(f"\nFile: {drl_file}")
                context_parts.append(content)
                context_parts.append("-" * 50)
        
        # GDST Files Context
        if self.gdst_files:
            context_parts.append("\n=== GDST DECISION TABLES ===")
            for gdst_file in self.gdst_files:
                content = self.read_file_content(gdst_file)
                context_parts.append(f"\nFile: {gdst_file}")
                context_parts.append(content)
                context_parts.append("-" * 50)
        
        return "\n".join(context_parts)

class TokenBucket:
    """Token bucket rate limiter implementation"""
    def __init__(self, tokens_per_minute: int):
        self.capacity = tokens_per_minute
        self.tokens = tokens_per_minute
        self.last_refill = time.time()
        self.refill_rate = tokens_per_minute / 60  # Tokens per second
    
    def consume(self, tokens: int) -> bool:
        """Try to consume tokens, returns True if successful"""
        now = time.time()
        elapsed = now - self.last_refill
        self.last_refill = now
        
        # Refill the bucket
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False
    
    def wait_for_tokens(self, tokens: int):
        """Wait until enough tokens are available"""
        while not self.consume(tokens):
            # Calculate how long to wait
            deficit = tokens - self.tokens
            wait_time = deficit / self.refill_rate
            time.sleep(max(0.1, wait_time))

class GroqDRLAssistant:
    """AI Assistant using Groq SDK for DRL rule generation and modification"""
    
    def __init__(self, api_key: str = None):
        self.groq_client = None
        self.context_memory = []  # Stores the context in memory
        self.token_bucket = TokenBucket(6000)  # 6000 tokens per minute rate limit
        
        if Groq and api_key:
            try:
                self.groq_client = Groq(api_key=api_key)
            except Exception as e:
                print(f"Failed to initialize Groq client: {e}")
    
    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count (approximation: 1 token ~= 4 characters)"""
        return max(1, len(text) // 4)
    
    def _split_context(self, context: str, max_tokens: int = 4000) -> List[str]:
        """Split context into chunks that are under the token limit"""
        # Simple implementation - split by lines to preserve logical structure
        lines = context.split('\n')
        chunks = []
        current_chunk = []
        current_length = 0
        
        for line in lines:
            line_length = self._estimate_tokens(line)
            if current_length + line_length > max_tokens and current_chunk:
                chunks.append('\n'.join(current_chunk))
                current_chunk = []
                current_length = 0
            current_chunk.append(line)
            current_length += line_length
        
        if current_chunk:
            chunks.append('\n'.join(current_chunk))
        
        return chunks
    
    def _send_context_chunk(self, chunk: str, is_last: bool = False) -> str:
        """Send a single context chunk to the LLM for storage"""
        # Estimate total tokens for the request (chunk + prompt)
        prompt = f"""
You are a context-aware DRL rules expert. I'm going to provide you with repository context that you need to remember for subsequent questions.

CONTEXT CHUNK:
{chunk}

INSTRUCTIONS:
1. Store this information in your context memory
2. Acknowledge that you've received this chunk by responding with "ACKNOWLEDGED"
3. If this is the last chunk, respond with "CONTEXT_READY"
4. Do not analyze or respond to the content at this time
"""
        estimated_tokens = self._estimate_tokens(prompt) + 100  # Add buffer
        
        # Wait until we have enough tokens
        self.token_bucket.wait_for_tokens(estimated_tokens)
        
        try:
            chat_completion = self.groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="deepseek-r1-distill-llama-70b",
                temperature=0.1,
                max_tokens=1000,
                top_p=1,
                stream=False,
                stop=None
            )
            
            return chat_completion.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Failed to send context chunk: {str(e)}")
    
    def load_context(self, context: str):
        """Load context into LLM memory by sending it in chunks"""
        if not self.groq_client:
            raise Exception("Groq client not initialized. Please set API key.")
        
        print("Loading context into LLM memory...")
        chunks = self._split_context(context)
        total_chunks = len(chunks)
        
        for i, chunk in enumerate(chunks, 1):
            print(f"Sending context chunk {i}/{total_chunks} (approx. {self._estimate_tokens(chunk)} tokens)...")
            is_last = (i == total_chunks)
            response = self._send_context_chunk(chunk, is_last)
            
            if "CONTEXT_READY" in response or is_last:
                print("Context loading complete!")
                return
        
        # If we get here without CONTEXT_READY, send a final confirmation
        self._send_context_chunk("This is the end of the context. Please respond with CONTEXT_READY.", True)
        print("Context loading complete!")
    
    def generate_drl_rule(self, requirements: str) -> str:
        """Generate DRL rule using Groq SDK with pre-loaded context"""
        if not self.groq_client:
            raise Exception("Groq client not initialized. Please set API key.")
        
        prompt = f"""
You are a Drools rules expert. Generate a complete DRL rule based on the repository context you have in memory and these requirements.

REQUIREMENTS:
{requirements}

INSTRUCTIONS:
1. Use the Java model classes from your context memory
2. Follow proper DRL syntax
3. Include clear comments
4. Reference existing patterns from the DRL files in your context
5. Ensure the rule integrates well with existing rules
6. Return ONLY the complete DRL rule content with proper syntax
7. DO NOT include any markdown code blocks (```drl``` or ```)
8. DO NOT include any thinking tags (<Thinking> or </Thinking>)
9. DO NOT include any explanatory text before or after the rule
10. Return the full DRL file content, not just the modified part
"""
        # Estimate tokens and wait
        estimated_tokens = self._estimate_tokens(prompt) + 2000  # Buffer for response
        self.token_bucket.wait_for_tokens(estimated_tokens)
        
        try:
            chat_completion = self.groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="compound-beta",
                temperature=0.5,
                max_tokens=8192,
                top_p=1,
                stream=False,
                stop=None
            )
            
            # Clean the output to remove any unwanted tags or markdown
            rule_content = chat_completion.choices[0].message.content
            
            rule_content = re.sub(r"<Thinking>.*?</Thinking>", "", rule_content, flags=re.DOTALL)
            rule_content = rule_content.replace("```drl", "").replace("```", "")
            rule_content = rule_content.strip()
            
            return rule_content
            
        except Exception as e:
            raise Exception(f"Failed to generate rule: {str(e)}")
    
    def modify_drl_rule(self, original_rule: str, requirements: str) -> str:
        """Modify an existing DRL rule using Groq SDK with pre-loaded context"""
        if not self.groq_client:
            raise Exception("Groq client not initialized. Please set API key.")
        
        prompt = f"""
You are a Drools rules expert. Modify the following DRL rule based on the repository context you have in memory and these requirements.

ORIGINAL RULE:
{original_rule}

REQUIREMENTS:
{requirements}

INSTRUCTIONS:
1. Use the Java model classes from your context memory
2. Follow proper DRL syntax
3. Include clear comments explaining changes
4. Reference existing patterns from the DRL files in your context
5. Ensure the modified rule integrates well with existing rules
6. Return ONLY the complete modified DRL rule content with proper syntax
7. DO NOT include any markdown code blocks (```drl``` or ```)
8. DO NOT include any thinking tags (<Thinking> or </Thinking>)
9. DO NOT include any explanatory text before or after the rule
10. Return the full DRL file content, not just the modified part
"""
        # Estimate tokens and wait
        estimated_tokens = self._estimate_tokens(prompt) + 2000  # Buffer for response
        self.token_bucket.wait_for_tokens(estimated_tokens)
        
        try:
            chat_completion = self.groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="compound-beta",
                temperature=0.5,
                max_tokens=8192,
                top_p=1,
                stream=False,
                stop=None
            )
            
            # Clean the output to remove any unwanted tags or markdown
            rule_content = chat_completion.choices[0].message.content
            
            rule_content = re.sub(r"<Thinking>.*?</Thinking>", "", rule_content, flags=re.DOTALL)
            rule_content = rule_content.replace("```drl", "").replace("```", "")
            rule_content = rule_content.strip()
            
            return rule_content
            
        except Exception as e:
            raise Exception(f"Failed to modify rule: {str(e)}")

class ConfigManager:
    """Manages configuration settings"""
    
    def __init__(self):
        self.config_file = Path.home() / ".drl_management_config.json"
        self.config = self.load_config()
    
    def load_config(self) -> Dict:
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
        
        return {
            "groq_api_key": "",
            "default_repository": os.getcwd(),
            "editor": os.environ.get("EDITOR", "nano")
        }
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def set_api_key(self, api_key: str):
        """Set Groq API key"""
        self.config["groq_api_key"] = api_key
        self.save_config()
        print("API key saved successfully!")
    
    def get_api_key(self) -> str:
        """Get Groq API key"""
        return self.config.get("groq_api_key", "")
    
    def set_default_repository(self, path: str):
        """Set default repository path"""
        self.config["default_repository"] = path
        self.save_config()
        print(f"Default repository set to: {path}")
    
    def get_default_repository(self) -> str:
        """Get default repository path"""
        return self.config.get("default_repository", os.getcwd())

class DRLManagementCLI:
    """Main CLI application class"""
    
    def __init__(self):
        self.config_manager = ConfigManager()
        self.scanner = None
        self.drl_assistant = None
        self.repository_context = ""
        
        # Initialize AI assistant if API key is available
        api_key = self.config_manager.get_api_key()
        if api_key:
            self.drl_assistant = GroqDRLAssistant(api_key)
    
    def scan_repository(self, path: str = None):
        """Scan repository for DRL-related files"""
        if not path:
            path = self.config_manager.get_default_repository()
        
        if not os.path.exists(path):
            print(f"Error: Repository path '{path}' does not exist")
            return
        
        self.scanner = RepositoryScanner(path)
        results = self.scanner.scan_repository()
        
        if results['java_files'] == 0 and results['drl_files'] == 0 and results['gdst_files'] == 0:
            print("No relevant files found in the repository.")
        else:
            self.repository_context = self.scanner.build_context()
            print("Repository scan completed successfully!")
            
            # Load context into LLM memory if assistant is available
            if self.drl_assistant and self.drl_assistant.groq_client:
                self.drl_assistant.load_context(self.repository_context)
    
    def list_files(self, file_type: str = "all"):
        """List files found in repository"""
        if not self.scanner:
            print("Please scan a repository first using 'scan' command")
            return
        
        self.scanner.list_files(file_type)
    
    def view_file(self, file_path: str):
        """View content of a specific file"""
        path = Path(file_path)
        if not path.exists():
            print(f"Error: File '{file_path}' does not exist")
            return
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"\n=== Content of {path.name} ===")
            print(content)
            print("=" * 50)
            
        except Exception as e:
            print(f"Error reading file: {e}")
    
    def edit_file(self, file_path: str):
        """Edit a file using the configured editor"""
        editor = self.config_manager.config.get("editor", "nano")
        
        if not file_path:
            # Create new file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = f"new_rule_{timestamp}.drl"
            
            # Create with template
            template = """package com.example.rules;

import java.util.*;

rule "New Rule"
    when
        // Add your conditions here
    then
        // Add your actions here
end
"""
            with open(file_path, 'w') as f:
                f.write(template)
        
        try:
            subprocess.run([editor, file_path])
            print(f"File '{file_path}' edited successfully!")
        except Exception as e:
            print(f"Error opening editor: {e}")
    
    def generate_rule(self, requirements: str = None, output_file: str = None):
        """Generate a new DRL rule using AI"""
        if not self.drl_assistant or not self.drl_assistant.groq_client:
            print("Error: Groq API key not configured. Use 'config set-api-key' command first.")
            return
        
        if not requirements:
            print("Enter your rule requirements (press Ctrl+D or Ctrl+Z when finished):")
            requirements_lines = []
            try:
                while True:
                    line = input()
                    requirements_lines.append(line)
            except EOFError:
                requirements = "\n".join(requirements_lines)
        
        if not requirements.strip():
            print("Error: No requirements provided")
            return
        
        print("Generating rule... This may take a moment.")
        
        try:
            rule_content = self.drl_assistant.generate_drl_rule(requirements)
            
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(rule_content)
                print(f"Generated rule saved to: {output_file}")
            else:
                print("\n=== Generated Rule ===")
                print(rule_content)
                print("=" * 50)
                
                save_choice = input("\nSave this rule to a file? (y/n): ").lower()
                if save_choice == 'y':
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = input(f"Enter filename (default: generated_rule_{timestamp}.drl): ").strip()
                    if not filename:
                        filename = f"generated_rule_{timestamp}.drl"
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(rule_content)
                    print(f"Rule saved to: {filename}")
        
        except Exception as e:
            print(f"Error generating rule: {e}")
    
    def modify_rule(self, file_path: str = None, requirements: str = None):
        """Modify an existing DRL rule using AI"""
        if not self.drl_assistant or not self.drl_assistant.groq_client:
            print("Error: Groq API key not configured. Use 'config set-api-key' command first.")
            return
        
        # Get the DRL file to modify
        if not file_path:
            if not self.scanner or not self.scanner.drl_files:
                print("No DRL files found. Please scan a repository first.")
                return
            
            print("\nSelect a DRL file to modify:")
            self.scanner.list_files("drl")
            try:
                selection = int(input("\nEnter file number to modify: ")) - 1
                if 0 <= selection < len(self.scanner.drl_files):
                    file_path = str(self.scanner.drl_files[selection])
                else:
                    print("Invalid selection")
                    return
            except ValueError:
                print("Please enter a valid number")
                return
        
        # Read the original rule content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_rule = f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return
        
        # Get modification requirements
        if not requirements:
            print(f"\nCurrent content of {file_path}:")
            print("=" * 50)
            print(original_rule)
            print("=" * 50)
            print("\nEnter your modification requirements (press Ctrl+D or Ctrl+Z when finished):")
            requirements_lines = []
            try:
                while True:
                    line = input()
                    requirements_lines.append(line)
            except EOFError:
                requirements = "\n".join(requirements_lines)
        
        if not requirements.strip():
            print("Error: No requirements provided")
            return
        
        print("Modifying rule... This may take a moment.")
        
        try:
            modified_rule = self.drl_assistant.modify_drl_rule(original_rule, requirements)
            
            print("\n=== Modified Rule ===")
            print(modified_rule)
            print("=" * 50)
            
            save_choice = input("\nSave this modified rule? (y/n): ").lower()
            if save_choice == 'y':
                # Backup original file
                backup_path = f"{file_path}.bak"
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_rule)
                
                # Save modified version
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(modified_rule)
                
                print(f"Original rule backed up to: {backup_path}")
                print(f"Modified rule saved to: {file_path}")
        
        except Exception as e:
            print(f"Error modifying rule: {e}")
    
    def show_context(self, limit: int = 1000):
        """Show repository context"""
        if not self.repository_context:
            print("No repository context available. Please scan a repository first.")
            return
        
        print("=== Repository Context ===")
        if len(self.repository_context) > limit:
            print(self.repository_context[:limit])
            print(f"\n... (truncated, showing first {limit} characters of {len(self.repository_context)} total)")
        else:
            print(self.repository_context)
        print("=" * 50)
    
    def configure(self, action: str, value: str = None):
        """Configure application settings"""
        if action == "set-api-key":
            if not value:
                value = input("Enter your Groq API key: ").strip()
            
            if value:
                self.config_manager.set_api_key(value)
                self.drl_assistant = GroqDRLAssistant(value)
            else:
                print("Error: No API key provided")
        
        elif action == "set-repository":
            if not value:
                value = input(f"Enter repository path (current: {self.config_manager.get_default_repository()}): ").strip()
            
            if value and os.path.exists(value):
                self.config_manager.set_default_repository(value)
            elif value:
                print(f"Error: Path '{value}' does not exist")
        
        elif action == "set-editor":
            if not value:
                current_editor = self.config_manager.config.get("editor", "nano")
                value = input(f"Enter preferred editor (current: {current_editor}): ").strip()
            
            if value:
                self.config_manager.config["editor"] = value
                self.config_manager.save_config()
                print(f"Editor set to: {value}")
        
        elif action == "show":
            print("=== Current Configuration ===")
            api_key = self.config_manager.get_api_key()
            print(f"Groq API Key: {'*' * len(api_key) if api_key else 'Not set'}")
            print(f"Default Repository: {self.config_manager.get_default_repository()}")
            print(f"Editor: {self.config_manager.config.get('editor', 'nano')}")
            print(f"Config File: {self.config_manager.config_file}")
        
        else:
            print("Available configuration actions:")
            print("  set-api-key    - Set Groq API key")
            print("  set-repository - Set default repository path")
            print("  set-editor     - Set preferred text editor")
            print("  show          - Show current configuration")
    
    def interactive_mode(self):
        """Run in interactive mode"""
        print("=== DRL Management System - Interactive Mode ===")
        print("Type 'help' for available commands or 'quit' to exit")
        
        while True:
            try:
                command = input("\ndrl> ").strip().split()
                if not command:
                    continue
                
                cmd = command[0].lower()
                
                if cmd in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                
                elif cmd == 'help':
                    self.show_help()
                
                elif cmd == 'scan':
                    path = command[1] if len(command) > 1 else None
                    self.scan_repository(path)
                
                elif cmd == 'list':
                    file_type = command[1] if len(command) > 1 else "all"
                    self.list_files(file_type)
                
                elif cmd == 'view':
                    if len(command) < 2:
                        print("Usage: view <file_path>")
                    else:
                        self.view_file(command[1])
                
                elif cmd == 'edit':
                    file_path = command[1] if len(command) > 1 else None
                    self.edit_file(file_path)
                
                elif cmd == 'generate':
                    output_file = command[1] if len(command) > 1 else None
                    self.generate_rule(output_file=output_file)
                
                elif cmd == 'modify':
                    file_path = command[1] if len(command) > 1 else None
                    self.modify_rule(file_path)
                
                elif cmd == 'context':
                    limit = int(command[1]) if len(command) > 1 else 1000
                    self.show_context(limit)
                
                elif cmd == 'config':
                    action = command[1] if len(command) > 1 else None
                    value = command[2] if len(command) > 2 else None
                    self.configure(action, value)
                
                else:
                    print(f"Unknown command: {cmd}. Type 'help' for available commands.")
            
            except KeyboardInterrupt:
                print("\nUse 'quit' to exit")
            except Exception as e:
                print(f"Error: {e}")
    
    def show_help(self):
        """Show help information"""
        help_text = """
=== DRL Management System Commands ===

Repository Management:
  scan [path]           - Scan repository for DRL-related files
  list [type]          - List found files (type: all, java, drl, gdst)
  context [limit]      - Show repository context (default limit: 1000 chars)

File Operations:
  view <file>          - View file content
  edit [file]          - Edit file (creates new if not specified)

AI Operations:
  generate [output]    - Generate new DRL rule using AI
  modify [file]        - Modify existing DRL rule using AI

Configuration:
  config show          - Show current configuration
  config set-api-key   - Set Groq API key
  config set-repository - Set default repository path
  config set-editor    - Set preferred text editor

General:
  help                 - Show this help
  quit/exit/q         - Exit the application

Examples:
  scan /path/to/project
  list drl
  generate my_rule.drl
  modify existing_rule.drl
  config set-api-key
"""
        print(help_text)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="DRL Management System - Command Line Interface")
    parser.add_argument("--interactive", "-i", action="store_true", help="Run in interactive mode")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Scan repository")
    scan_parser.add_argument("path", nargs="?", help="Repository path")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List files")
    list_parser.add_argument("type", nargs="?", default="all", choices=["all", "java", "drl", "gdst"])
    
    # View command
    view_parser = subparsers.add_parser("view", help="View file content")
    view_parser.add_argument("file", help="File path")
    
    # Edit command
    edit_parser = subparsers.add_parser("edit", help="Edit file")
    edit_parser.add_argument("file", nargs="?", help="File path (optional)")
    
    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate DRL rule")
    generate_parser.add_argument("--output", "-o", help="Output file")
    generate_parser.add_argument("--requirements", "-r", help="Rule requirements")
    
    # Modify command
    modify_parser = subparsers.add_parser("modify", help="Modify DRL rule")
    modify_parser.add_argument("file", nargs="?", help="File to modify")
    modify_parser.add_argument("--requirements", "-r", help="Modification requirements")
    
    # Context command
    context_parser = subparsers.add_parser("context", help="Show repository context")
    context_parser.add_argument("--limit", "-l", type=int, default=1000, help="Character limit")
    
    # Config command
    config_parser = subparsers.add_parser("config", help="Configuration")
    config_parser.add_argument("action", nargs="?", choices=["show", "set-api-key", "set-repository", "set-editor"])
    config_parser.add_argument("value", nargs="?", help="Configuration value")
    
    args = parser.parse_args()
    
    cli = DRLManagementCLI()
    
    if args.interactive or not args.command:
        cli.interactive_mode()
    else:
        # Handle direct commands
        if args.command == "scan":
            cli.scan_repository(args.path)
        elif args.command == "list":
            cli.list_files(args.type)
        elif args.command == "view":
            cli.view_file(args.file)
        elif args.command == "edit":
            cli.edit_file(args.file)
        elif args.command == "generate":
            cli.generate_rule(args.requirements, args.output)
        elif args.command == "modify":
            cli.modify_rule(args.file, args.requirements)
        elif args.command == "context":
            cli.show_context(args.limit)
        elif args.command == "config":
            cli.configure(args.action, args.value)

if __name__ == "__main__":
    main()

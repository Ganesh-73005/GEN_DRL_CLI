
# DRL Management System

A comprehensive command-line tool for managing Drools Rule Language (DRL) files with AI assistance, featuring intelligent context management and rate limiting for the Groq API.

## Features

- **Repository Scanning**: Automatically scans for Java models, DRL files, and GDST files
- **AI-Powered Rule Generation**: Generate new DRL rules using Groq's LLM
- **Rule Modification**: Modify existing DRL rules with precise requirements
- **Context-Aware**: Maintains full repository context (Java models, existing rules, GDST tables)
- **Rate Limiting**: Strict 6000 tokens/minute enforcement for Groq API
- **Chunk Optimization**: Intelligent context splitting for large repositories
- **Interactive CLI**: User-friendly command-line interface
- **File Management**: View, edit, and manage DRL files

## Token Management & Chunking Optimization

The system implements several advanced features to work within Groq's limits:

- **Token Bucket Algorithm**: Strict 6000 tokens/minute rate limiting
- **Smart Chunking**: 
  - Splits large context into optimally sized chunks (~4000 tokens)
  - Preserves logical file structure when splitting
  - Progress tracking during context loading
- **Token Estimation**: 
  - Uses 1 token ≈ 4 characters approximation
  - Includes buffers for prompt overhead
- **Efficient Loading**: 
  - Parallel processing where possible
  - Visual progress indicators

## Quick Start

### Installation

1. Ensure Python 3.8+ is installed
2. Install required packages:
   ```bash
   pip install groq python-dotenv
   ```
3. Set your Groq API key:
   ```bash
   drl config set-api-key YOUR_API_KEY
   ```

### Basic Usage

```bash
# Scan a repository
drl scan /path/to/your/project

# List all DRL files
drl list drl

# Generate a new rule
drl generate --output new_rule.drl

# Modify an existing rule
drl modify existing_rule.drl

# Interactive mode
drl --interactive
```

## Command Reference

### Main Commands

| Command       | Parameters                      | Description                                  |
|---------------|---------------------------------|----------------------------------------------|
| `scan`        | `[path]`                       | Scan repository for DRL-related files        |
| `list`        | `[all\|java\|drl\|gdst]`       | List found files of specified type           |
| `view`        | `<file_path>`                  | View content of a specific file              |
| `edit`        | `[file_path]`                  | Edit file (creates new if not specified)     |
| `generate`    | `[--output FILE]` `[--requirements TEXT]` | Generate new DRL rule            |
| `modify`      | `[file_path]` `[--requirements TEXT]` | Modify existing DRL rule          |
| `context`     | `[--limit CHARS]`              | Show repository context                      |
| `config`      | `[action]` `[value]`           | Configure application settings               |

### Configuration Actions

| Action           | Description                          |
|------------------|--------------------------------------|
| `set-api-key`    | Set Groq API key                     |
| `set-repository` | Set default repository path          |
| `set-editor`     | Set preferred text editor            |
| `show`           | Show current configuration           |

## Examples

### 1. Full Workflow Example

```bash
# Set your API key
drl config set-api-key your_groq_api_key_here

# Scan a project
drl scan ~/projects/rules-engine

# List all DRL files
drl list drl

# Generate a new discount rule
drl generate --output discount_rules.drl

# Modify an existing validation rule
drl modify validation_rules.drl
```

### 2. Interactive Mode Example

```bash
$ drl --interactive
DRL Management System - Interactive Mode
Type 'help' for available commands or 'quit' to exit

drl> scan /path/to/project
Scanning repository: /path/to/project
Found: 5 Java model files, 12 DRL files, 3 GDST files
Loading context into LLM memory...
Sending context chunk 1/3 (approx. 3850 tokens)...
Sending context chunk 2/3 (approx. 3920 tokens)...
Sending context chunk 3/3 (approx. 1250 tokens)...
Context loading complete!

drl> modify
Select a DRL file to modify:
=== DRL Rule Files ===
 1. discount_rules.drl (/path.../discount_rules.drl) - 1204 bytes
 2. validation.drl (/path.../validation.drl) - 845 bytes
...

Enter file number to modify: 2
Current content of validation.drl:
===================================
[file content shown here]
===================================

Enter your modification requirements:
Make the age validation more strict by:
- Adding a minimum age of 18
- Adding maximum age of 100
- Include detailed error messages

Modifying rule... This may take a moment.

=== Modified Rule ===
[modified content shown]

Save this modified rule? (y/n): y
Original rule backed up to: validation.drl.bak
Modified rule saved to: validation.drl
```

### 3. Direct Command Example

```bash
# Generate a rule with immediate requirements
drl generate --requirements "Create a rule that applies 10% discount when cart total > $100 and customer is premium" --output discount_rule.drl

# Modify a rule with specific requirements
drl modify validation.drl --requirements "Add email format validation using regex pattern"
```

## Best Practices

1. **Repository Structure**:
   - Keep Java models in clear package structure
   - Organize DRL files by business domain
   - Use consistent naming conventions

2. **Context Management**:
   - Rescan after major repository changes
   - Use `context` command to verify loaded information

3. **Rate Limiting**:
   - Large repositories may take time to process
   - Monitor token usage in verbose mode

4. **Modification Workflow**:
   - Always review generated changes
   - Use version control alongside the tool
   - Keep modification requirements specific and clear

## Troubleshooting

**Error: API rate limit exceeded**
- The system automatically handles rate limiting
- Wait a minute and try again
- Larger contexts may require more time to process

**Error: No DRL files found**
- Verify your repository path
- Ensure files have .drl extension
- Check file permissions

**Error: Invalid API key**
- Verify your Groq API key
- Use `config set-api-key` to update

## License

[MIT License](LICENSE)
```

This README provides:
1. Comprehensive feature overview
2. Technical details about token management
3. Quick start guide
4. Complete command reference
5. Practical examples
6. Best practices
7. Troubleshooting tips


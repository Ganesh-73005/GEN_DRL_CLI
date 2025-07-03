# DRL Management System - Command Line Interface

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Groq](https://img.shields.io/badge/AI-Groq-orange.svg)](https://groq.com)

A comprehensive command-line tool for managing Drools Rule Language (DRL) files with AI assistance. This tool helps developers scan repositories, generate DRL rules, analyze existing rules, and manage rule files efficiently.

## 🚀 Features

- **🔍 Repository Scanner**: Automatically scan repositories for Java model files, DRL files, and GDST decision tables
- **🤖 AI-Powered Rule Generation**: Generate DRL rules based on natural language requirements using Groq AI
- **📊 Rule Analysis**: Analyze existing DRL rules for issues, suggestions, and compatibility
- **📝 File Management**: View, edit, and manage DRL files with your preferred editor
- **🧠 Context-Aware**: Uses repository context (Java models, existing rules) to generate better rules
- **💻 Cross-Platform**: Works on Windows, macOS, and Linux
- **🎯 Interactive Mode**: User-friendly interactive command interface
- **⚙️ Configuration Management**: Persistent settings and API key management

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Commands](#commands)
- [Configuration](#configuration)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🛠️ Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)
- Groq API key (for AI features) - Get one from [Groq Console](https://console.groq.com/)

### Quick Installation

#### Windows
\`\`\`cmd
# 1. Install dependencies
pip install groq

# 2. Download the script and run setup
setup_windows.bat

# 3. Start using
python drl_management_cli.py --interactive
\`\`\`

#### Linux/macOS
\`\`\`bash
# 1. Install dependencies
pip3 install groq

# 2. Make executable
chmod +x drl_management_cli.py

# 3. Run quick start
bash quick_start.sh

# 4. Start using
python3 drl_management_cli.py --interactive
\`\`\`

### Manual Installation

1. **Clone or download** the repository
2. **Install dependencies**:
   \`\`\`bash
   pip install groq
   \`\`\`
3. **Set up API key**:
   \`\`\`bash
   python drl_management_cli.py config set-api-key
   \`\`\`

## 🚀 Quick Start

### 1. First Time Setup (2 minutes)

\`\`\`bash
# Set up your Groq API key
python drl_management_cli.py config set-api-key

# Start interactive mode
python drl_management_cli.py --interactive
\`\`\`

### 2. Basic Workflow

\`\`\`bash
# In interactive mode:
drl> scan /path/to/your/java/project    # Scan repository
drl> list                               # See found files
drl> generate                           # Create new rule
drl> analyze generated_rule.drl         # Analyze rule
drl> help                              # Get help
drl> quit                              # Exit
\`\`\`

### 3. Direct Commands

\`\`\`bash
# Scan repository
python drl_management_cli.py scan /path/to/project

# Generate rule
python drl_management_cli.py generate --output new_rule.drl

# Analyze rule
python drl_management_cli.py analyze existing_rule.drl
\`\`\`

## 📖 Usage

### Interactive Mode (Recommended for beginners)

\`\`\`bash
python drl_management_cli.py --interactive
\`\`\`

Interactive mode provides a shell-like interface where you can:
- Get command suggestions and help
- See immediate feedback
- Explore features step by step

### Direct Command Mode (Great for automation)

\`\`\`bash
python drl_management_cli.py [command] [options]
\`\`\`

Direct commands are perfect for:
- Scripting and automation
- CI/CD pipelines
- Batch operations

## 🎯 Commands

### Repository Management

| Command | Description | Example |
|---------|-------------|---------|
| `scan [path]` | Scan repository for DRL-related files | `scan /path/to/project` |
| `list [type]` | List found files (all, java, drl, gdst) | `list drl` |
| `context [limit]` | Show repository context | `context 2000` |

### File Operations

| Command | Description | Example |
|---------|-------------|---------|
| `view <file>` | View file content | `view rule.drl` |
| `edit [file]` | Edit file (creates new if not specified) | `edit my_rule.drl` |

### AI Operations

| Command | Description | Example |
|---------|-------------|---------|
| `generate [output]` | Generate DRL rule using AI | `generate new_rule.drl` |
| `analyze [file]` | Analyze DRL rule using AI | `analyze existing_rule.drl` |

### Configuration

| Command | Description | Example |
|---------|-------------|---------|
| `config show` | Show current configuration | `config show` |
| `config set-api-key` | Set Groq API key | `config set-api-key` |
| `config set-repository` | Set default repository path | `config set-repository /path` |
| `config set-editor` | Set preferred text editor | `config set-editor code` |

### General

| Command | Description |
|---------|-------------|
| `help` | Show help information |
| `quit` / `exit` / `q` | Exit the application |

## ⚙️ Configuration

The tool stores configuration in `~/.drl_management_config.json`:

\`\`\`json
{
  "groq_api_key": "your-api-key-here",
  "default_repository": "/path/to/your/main/project",
  "editor": "code"
}
\`\`\`

### Setting up Groq API Key

1. Visit [Groq Console](https://console.groq.com/)
2. Sign up/login and create an API key
3. Configure it:
   \`\`\`bash
   python drl_management_cli.py config set-api-key
   \`\`\`

### Supported Editors

- **VS Code**: `code`
- **Vim**: `vim`
- **Nano**: `nano`
- **Notepad** (Windows): `notepad`
- **Notepad++**: `notepad++`
- **Any editor**: `/path/to/your/editor`

## 📚 Examples

### Example 1: Complete New Rule Creation

\`\`\`bash
$ python drl_management_cli.py --interactive

drl> scan /home/user/ecommerce-project
Scanning repository: /home/user/ecommerce-project
Found: 5 Java model files, 3 DRL files, 1 GDST files

drl> list java
=== Java Model Files ===
 1. Customer.java - 1250 bytes
 2. Order.java - 890 bytes
 3. Product.java - 650 bytes

drl> generate
Enter your rule requirements (press Ctrl+D when finished):
Create a rule that applies a 10% discount to orders over $100 for premium customers
^D

Generating rule... This may take a moment.

=== Generated Rule ===
package com.ecommerce.rules;

import com.ecommerce.model.Customer;
import com.ecommerce.model.Order;

rule "Premium Customer Discount"
    when
        $customer : Customer(membershipType == "PREMIUM")
        $order : Order(customer == $customer, totalAmount > 100.0)
    then
        $order.setDiscount(0.10);
        $order.setTotalAmount($order.getTotalAmount() * 0.9);
        System.out.println("Applied 10% discount: " + $order.getId());
end

Save this rule to a file? (y/n): y
Enter filename: premium_discount.drl
Rule saved to: premium_discount.drl

drl> analyze premium_discount.drl
=== Rule Analysis ===
SUMMARY: Applies 10% discount to orders over $100 for premium customers.
ISSUES: Consider adding null checks and thread safety measures.
SUGGESTIONS: Add logging, use discount service, prevent double application.
COMPATIBILITY: Good integration with existing model classes.
PERFORMANCE: Efficient rule with simple conditions.

drl> quit
\`\`\`

### Example 2: Batch Rule Generation

\`\`\`bash
# Generate multiple rules
python drl_management_cli.py generate --requirements "Create validation rules for user input" --output validation_rules.drl
python drl_management_cli.py generate --requirements "Create business rules for order processing" --output business_rules.drl

# Analyze all rules
python drl_management_cli.py analyze validation_rules.drl
python drl_management_cli.py analyze business_rules.drl
\`\`\`

### Example 3: Repository Analysis

\`\`\`bash
# Scan and analyze existing project
python drl_management_cli.py scan /path/to/existing/project
python drl_management_cli.py list drl
python drl_management_cli.py context --limit 5000

# Analyze existing rules
for rule in *.drl; do
    python drl_management_cli.py analyze "$rule"
done
\`\`\`

## 🔧 Troubleshooting

### Common Issues

#### "Groq client not initialized"
\`\`\`bash
# Solution: Set your API key
python drl_management_cli.py config set-api-key
\`\`\`

#### "No files found in repository"
- Check if you're scanning the correct directory
- Ensure your Java files are in directories containing "model"
- Verify DRL files have `.drl` extension

#### "Module 'groq' not found"
\`\`\`bash
# Install the required package
pip install groq
\`\`\`

#### "Permission denied" (Linux/macOS)
\`\`\`bash
# Make script executable
chmod +x drl_management_cli.py
\`\`\`

#### Editor not opening
\`\`\`bash
# Set your preferred editor
python drl_management_cli.py config set-editor code
\`\`\`

### Platform-Specific Issues

#### Windows
- Use `python` instead of `python3`
- Use Windows path format: `C:\path\to\project`
- No need for `chmod` command
- Default editor is `notepad`


### Getting Help

1. **Command Help**: `python drl_management_cli.py --help`
2. **Interactive Help**: Type `help` in interactive mode
3. **Configuration**: Check with `config show`
4. **Verbose Output**: Most commands provide detailed feedback

## 🏗️ Project Structure

\`\`\`
drl-management-cli/
├── drl_management_cli.py      # Main application
├── README.md                  # This file
└── LICENSE                   # License file
\`\`\`

## 🤝 Contributing

We welcome contributions! Here's how you can help:


2. **Suggest Features**: Have an idea? Let us know!
3. **Submit Pull Requests**: 
   - Fork the repository
   - Create a feature branch
   - Make your changes
   - Submit a pull request

### Development Setup

\`\`\`bash
# Clone the repository
git clone https://github.com/Ganesh-73005/GEN_DRL_CLI/drl-management-cli.git
cd drl-management-cli

# Install dependencies
pip install groq

# Run tests
python -m pytest tests/

# Run the tool
python drl_management_cli.py --interactive
\`\`\`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Groq** for providing the AI API
- **Drools** community for the rule engine
- **Python** community for the excellent ecosystem



## 🔗 Links

- [Groq Console](https://console.groq.com/) - Get your API key
- [Drools Documentation](https://docs.drools.org/) - Learn about DRL
- [Python.org](https://python.org) - Download Python

---

**Made with ❤️ for the Drools community**

*Happy rule writing! 🎉*

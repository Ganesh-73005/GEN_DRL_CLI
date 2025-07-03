#!/bin/bash
# Quick start script for DRL Management System CLI

echo "=== DRL Management System CLI - Quick Start ==="
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3 and try again."
    exit 1
fi

echo "✅ Python 3 found"

# Check if groq package is installed
if ! python3 -c "import groq" 2>/dev/null; then
    echo "📦 Installing groq package..."
    pip3 install groq
    if [ $? -eq 0 ]; then
        echo "✅ Groq package installed successfully"
    else
        echo "❌ Failed to install groq package"
        echo "Please run: pip3 install groq"
        exit 1
    fi
else
    echo "✅ Groq package already installed"
fi

# Make script executable
chmod +x drl_management_cli.py
echo "✅ Made script executable"

echo ""
echo "🚀 Setup complete! Here's how to get started:"
echo ""
echo "1. Set up your Groq API key:"
echo "   python3 drl_management_cli.py config set-api-key"
echo ""
echo "2. Start interactive mode:"
echo "   python3 drl_management_cli.py --interactive"
echo ""
echo "3. Or scan a repository directly:"
echo "   python3 drl_management_cli.py scan /path/to/your/project"
echo ""
echo "4. Get help anytime:"
echo "   python3 drl_management_cli.py --help"
echo ""

# Ask if user wants to set up API key now
read -p "Would you like to set up your Groq API key now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Please get your API key from: https://console.groq.com/"
    python3 drl_management_cli.py config set-api-key
fi

echo ""
echo "🎉 You're ready to use the DRL Management System CLI!"

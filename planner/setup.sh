#!/bin/bash

set -e  # Exit on any error

echo "=== Raspberry Pi Environment Setup ==="
echo ""

# Check if running on Raspberry Pi (optional)
if [ ! -f /etc/os-release ] || ! grep -q "Raspberry Pi" /etc/os-release; then
    echo "Warning: This doesn't appear to be a Raspberry Pi"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Display system info
echo "Current system:"
cat /etc/os-release | grep PRETTY_NAME
echo ""

# Update system
echo "=== Updating system ==="
sudo apt update
sudo apt upgrade -y

# Install APT packages
echo "=== Installing APT packages ==="
if [ -f apt-packages.txt ]; then
    echo "Installing packages from apt-packages.txt..."
    xargs -a apt-packages.txt sudo apt install -y
else
    echo "Warning: apt-packages.txt not found"
fi

# Install Python dependencies
echo "=== Installing Python packages ==="
if [ -f requirements.txt ]; then
    echo "Installing packages from requirements.txt..."
    pip install -r requirements.txt
else
    echo "Warning: requirements.txt not found"
fi

echo ""
echo "=== Setup complete! ==="
echo "You may need to reboot for some changes to take effect."

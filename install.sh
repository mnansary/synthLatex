#!/bin/bash

# Exit on error
set -e

# Update package list
echo "Updating package list..."
sudo apt update

# Install LaTeX (full distribution for all packages used in template_generator.py)
echo "Installing LaTeX (texlive-full)..."
sudo apt install -y texlive-full

# Install ImageMagick for converting LaTeX PDFs to images
echo "Installing ImageMagick..."
sudo apt install -y imagemagick

# Check if Conda is installed
if ! command -v conda &> /dev/null; then
    echo "Conda not found. Please install Miniconda or Anaconda first."
    echo "Download from https://docs.conda.io/en/latest/miniconda.html and follow installation instructions."
    exit 1
fi

# Create and activate Conda environment
echo "Creating Conda environment 'synthlatex'..."
conda create -n synthlatex python=3.8 -y
source "$(conda info --base)/etc/profile.d/conda.sh"  # Ensure conda is available in script
conda activate synthlatex

# Install Python dependencies from requirements.txt
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Installation complete!"
echo "To activate the environment later, run: conda activate synthlatex"
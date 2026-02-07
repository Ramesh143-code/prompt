#!/bin/bash

echo "======================================"
echo "  PromptGenius Setup Script"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${BLUE}Checking Python version...${NC}"
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"
echo ""

# Backend Setup
echo -e "${GREEN}Setting up Backend...${NC}"
cd backend

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Downloading spaCy model..."
python -m spacy download en_core_web_sm

echo "Downloading NLTK data..."
python << EOF
import nltk
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
print("NLTK data downloaded successfully!")
EOF

echo "Creating .env file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo ".env file created. Please edit it with your API keys if needed."
else
    echo ".env file already exists."
fi

cd ..

# Frontend Setup
echo ""
echo -e "${GREEN}Setting up Frontend...${NC}"
cd frontend

echo "Installing Node dependencies..."
npm install

cd ..

# Final message
echo ""
echo -e "${GREEN}======================================"
echo "  Setup Complete! ✨"
echo "======================================${NC}"
echo ""
echo "To start the application:"
echo ""
echo -e "${BLUE}Backend:${NC}"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python main.py"
echo ""
echo -e "${BLUE}Frontend:${NC}"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Then open http://localhost:3000 in your browser!"
echo ""
echo -e "${BLUE}Optional: Add API keys in backend/.env for LLM evaluation${NC}"
echo ""

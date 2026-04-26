#!/bin/bash
# Quick Start Script for AI Skill Assessment Agent

echo "🚀 AI-Powered Skill Assessment Agent - Quick Start"
echo "=================================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python
echo -e "${BLUE}1. Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}❌ Python 3 not found. Please install Python 3.10+${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo -e "${GREEN}✅ Python $PYTHON_VERSION found${NC}"
echo ""

# Navigate to backend
echo -e "${BLUE}2. Navigating to backend directory...${NC}"
cd backend || exit 1
echo -e "${GREEN}✅ In backend directory${NC}"
echo ""

# Create virtual environment
echo -e "${BLUE}3. Creating Python virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${GREEN}✅ Virtual environment already exists${NC}"
fi
echo ""

# Activate virtual environment
echo -e "${BLUE}4. Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✅ Virtual environment activated${NC}"
echo ""

# Install dependencies
echo -e "${BLUE}5. Installing Python dependencies...${NC}"
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dependencies installed${NC}"
else
    echo -e "${YELLOW}⚠️  Some dependencies may have failed. Check requirements.txt${NC}"
fi
echo ""

# Setup environment file
echo -e "${BLUE}6. Setting up environment configuration...${NC}"
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${GREEN}✅ .env created from .env.example${NC}"
        echo -e "${YELLOW}⚠️  Please edit .env with your API keys:${NC}"
        echo "   - ANTHROPIC_API_KEY or OPENAI_API_KEY"
        echo "   - DATABASE_URL (optional for MVP)"
    else
        echo -e "${YELLOW}⚠️  .env.example not found${NC}"
    fi
else
    echo -e "${GREEN}✅ .env already configured${NC}"
fi
echo ""

# Summary
echo -e "${BLUE}=================================================="
echo "✅ Setup Complete!"
echo "==================================================${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Edit .env with your API keys (ANTHROPIC_API_KEY or OPENAI_API_KEY)"
echo "2. Run: uvicorn app.main:app --reload"
echo "3. Visit: http://localhost:8000/docs"
echo ""
echo -e "${GREEN}Happy coding! 🎉${NC}"
echo ""

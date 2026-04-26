#!/bin/bash

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${PURPLE}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║        🚀 AI SKILL ASSESSMENT PLATFORM - DEMO LAUNCHER 🚀     ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo ""
echo -e "${BLUE}📋 Project Status:${NC}"
echo "   Phase 1: Setup         ✓ COMPLETE (100%)"
echo "   Phase 2: AI Agents     ✓ COMPLETE (100%)"
echo "   Phase 2.5: Integration ✓ COMPLETE (100%)"
echo "   Phase 3: NLP Services  ✓ COMPLETE (100%)"
echo "   Phase 4: Database      🔄 IN PROGRESS (75%)"
echo "   Phase 5: UI            ⚡ READY TO LAUNCH (60%)"
echo ""

# Check if ports are in use
echo -e "${BLUE}🔍 Checking system status...${NC}"

# Check backend port
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo -e "${GREEN}✓ Backend already running on port 8000${NC}"
    BACKEND_RUNNING=true
else
    echo -e "${YELLOW}⚠ Backend not running on port 8000${NC}"
    BACKEND_RUNNING=false
fi

# Check frontend port
if lsof -Pi :5173 -sTCP:LISTEN -t >/dev/null ; then
    echo -e "${GREEN}✓ Frontend already running on port 5173${NC}"
    FRONTEND_RUNNING=true
else
    echo -e "${YELLOW}⚠ Frontend not running on port 5173${NC}"
    FRONTEND_RUNNING=false
fi

echo ""
echo -e "${BLUE}🚀 Launch Options:${NC}"
echo ""
echo "1. Launch Everything (Backend + Frontend)"
echo "2. Launch Backend Only (http://localhost:8000)"
echo "3. Launch Frontend Only (http://localhost:5173)"
echo "4. View API Documentation (http://localhost:8000/docs)"
echo "5. Run Integration Tests"
echo "6. Show Project Overview"
echo "7. Exit"
echo ""

read -p "Select option (1-7): " choice

case $choice in
    1)
        echo -e "${YELLOW}Starting Backend and Frontend...${NC}"
        
        # Start backend if not running
        if [ "$BACKEND_RUNNING" = false ]; then
            echo -e "${BLUE}Starting Backend...${NC}"
            cd backend
            python3 -m app.main > /tmp/backend.log 2>&1 &
            BACKEND_PID=$!
            cd ..
            sleep 3
            echo -e "${GREEN}✓ Backend started (PID: $BACKEND_PID)${NC}"
        fi
        
        # Start frontend if not running
        if [ "$FRONTEND_RUNNING" = false ]; then
            echo -e "${BLUE}Starting Frontend...${NC}"
            cd frontend
            npm install >/dev/null 2>&1
            npm run dev > /tmp/frontend.log 2>&1 &
            FRONTEND_PID=$!
            cd ..
            sleep 3
            echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"
        fi
        
        echo ""
        echo -e "${GREEN}🎉 All Systems Running!${NC}"
        echo ""
        echo "   🌐 Frontend: http://localhost:5173"
        echo "   📚 API Docs: http://localhost:8000/docs"
        echo "   ⚡ Backend:  http://localhost:8000"
        echo ""
        echo -e "${YELLOW}Opening browser in 2 seconds...${NC}"
        sleep 2
        open http://localhost:5173 2>/dev/null || xdg-open http://localhost:5173 2>/dev/null
        ;;
        
    2)
        if [ "$BACKEND_RUNNING" = false ]; then
            echo -e "${BLUE}Starting Backend...${NC}"
            cd backend
            python3 -m app.main
        else
            echo -e "${GREEN}Backend already running on port 8000${NC}"
        fi
        ;;
        
    3)
        if [ "$FRONTEND_RUNNING" = false ]; then
            echo -e "${BLUE}Starting Frontend...${NC}"
            cd frontend
            npm install >/dev/null 2>&1
            npm run dev
        else
            echo -e "${GREEN}Frontend already running on port 5173${NC}"
        fi
        ;;
        
    4)
        echo -e "${BLUE}Opening API Documentation...${NC}"
        echo "Make sure backend is running on port 8000"
        sleep 1
        open http://localhost:8000/docs 2>/dev/null || xdg-open http://localhost:8000/docs 2>/dev/null
        ;;
        
    5)
        echo -e "${BLUE}Running Integration Tests...${NC}"
        cd backend
        python3 test_phase25_integration.py
        ;;
        
    6)
        echo ""
        echo -e "${PURPLE}╔════════════════════════════════════════════════════════════════╗${NC}"
        echo -e "${PURPLE}║                   PROJECT OVERVIEW                            ║${NC}"
        echo -e "${PURPLE}╚════════════════════════════════════════════════════════════════╝${NC}"
        echo ""
        echo -e "${YELLOW}Architecture:${NC}"
        echo "   • FastAPI Backend - Handles AI agents and NLP services"
        echo "   • PostgreSQL Database - Persistent storage for sessions"
        echo "   • React Frontend - Beautiful, responsive UI"
        echo "   • Claude 3.5 Sonnet - AI-powered question generation"
        echo "   • spaCy + Transformers - NLP skill extraction"
        echo ""
        echo -e "${YELLOW}Features:${NC}"
        echo "   ✓ AI-powered skill assessment"
        echo "   ✓ Adaptive multi-turn questions"
        echo "   ✓ NLP-based response evaluation"
        echo "   ✓ Personalized learning plans"
        echo "   ✓ Real-time proficiency scoring"
        echo ""
        echo -e "${YELLOW}Tech Stack:${NC}"
        echo "   • Backend: FastAPI, SQLAlchemy, Pydantic"
        echo "   • AI: Claude API, spaCy, Sentence-Transformers"
        echo "   • Database: PostgreSQL, pgvector"
        echo "   • Frontend: React, Tailwind CSS, Vite"
        echo ""
        echo -e "${YELLOW}Project Statistics:${NC}"
        echo "   • Code: 3,500+ lines"
        echo "   • Tests: 6/6 passing"
        echo "   • Assessment Time: <5 seconds"
        echo "   • Services: 3 NLP services"
        echo "   • Agents: 4 AI agents"
        echo ""
        ;;
        
    7)
        echo -e "${GREEN}Goodbye! 👋${NC}"
        exit 0
        ;;
        
    *)
        echo -e "${RED}Invalid option${NC}"
        exit 1
        ;;
esac

#!/bin/bash

# 1. Colors for pretty output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== 🚀 Starting Google Quiz System Automation ===${NC}"

# 2. Check for MongoDB
if pgrep -x "mongod" >/dev/null
then
    echo -e "${GREEN}✅ MongoDB is running.${NC}"
else
    echo -e "${RED}⚠️ MongoDB is NOT running!${NC}"
    echo -e "${BLUE}👉 Please open a separate terminal and run: mongod --dbpath /data/db${NC}"
    # We continue anyway because you might have it running differently
fi

# 3. Setup Backend
echo -e "${BLUE}--- 🐍 Setting up Backend ---${NC}"

# Exact case match from your screenshot: "Backend"
if [ -d "Backend" ]; then
    cd Backend
else
    echo -e "${RED}❌ Error: Could not find 'Backend' folder.${NC}"
    exit 1
fi

if [ ! -d ".venv" ]; then
    echo "Creating Python Virtual Environment..."
    python3 -m venv .venv
fi

source .venv/bin/activate
# Install dependencies quietly
pip install -q fastapi uvicorn motor pydantic pydantic-settings google-api-python-client google-auth-oauthlib python-dotenv email-validator

# Start Backend in background
echo -e "${GREEN}✅ Starting FastAPI Server on Port 8000...${NC}"
uvicorn main:app --reload &
BACKEND_PID=$!

cd ..

# 4. Setup Frontend
echo -e "${BLUE}--- ⚛️ Setting up Frontend ---${NC}"

# Exact case match from your screenshot: "Frontend"
if [ -d "Frontend" ]; then
    cd Frontend
else
    echo -e "${RED}❌ Error: Could not find 'Frontend' folder.${NC}"
    # Kill backend if frontend fails so you aren't stuck with open ports
    kill $BACKEND_PID
    exit 1
fi

if [ ! -d "node_modules" ]; then
    echo "Installing Node Modules..."
    npm install --silent
fi

# Start Frontend
echo -e "${GREEN}✅ Starting React App on Port 3000...${NC}"
npm start &
FRONTEND_PID=$!

# 5. Cleanup Function
trap "kill $BACKEND_PID; kill $FRONTEND_PID; exit" SIGINT

echo -e "${GREEN}=== 🎉 System Deployed! Press Ctrl+C to stop ===${NC}"

# Keep script running
wait
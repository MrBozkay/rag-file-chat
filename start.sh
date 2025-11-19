#!/bin/bash

# Kill any existing processes on ports 3000 and 8000
fuser -k 3000/tcp 2>/dev/null
fuser -k 8000/tcp 2>/dev/null

# Start Backend
echo "Starting Backend..."
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000 > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Start Frontend
echo "Starting Frontend..."
cd frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo "Application started!"
echo "Frontend: http://localhost:3000"
echo "Backend: http://localhost:8000"
echo "Press Ctrl+C to stop."

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID

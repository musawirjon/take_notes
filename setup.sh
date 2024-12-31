#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting project setup...${NC}"

# Create virtual environment
echo -e "${GREEN}Creating virtual environment...${NC}"
python -m venv myenv

# Activate virtual environment
echo -e "${GREEN}Activating virtual environment...${NC}"
source myenv/bin/activate

# Install dependencies
echo -e "${GREEN}Installing dependencies...${NC}"
pip install -r requirements.txt

# Create .env file
echo -e "${GREEN}Creating .env file...${NC}"
cat > .env << EOL
PROJECT_NAME=note_taking_app
ALLOWED_ORIGINS=http://localhost,https://example.com
# Database credentials
DB_USER=root
DB_PASSWORD=root
DB_NAME=note_taker_db

REDIS_URL=redis://localhost:6379/0

DATABASE_URL=postgresql://root:root@localhost:5432/note_taker_db

# DATABASE_URL=sqlite:///./app.db

# JWT
SECRET_KEY=123456
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Server
DEBUG=True
EOL

# Load environment variables from .env file
if [ -f .env ]; then
    echo "Loading .env file..."
    export $(grep -v '^#' .env | xargs)  # This will load all the variables into the environment
else
    echo ".env file not found!"
    exit 1
fi

# Initialize alembic
echo -e "${GREEN}Initializing Alembic...${NC}"
alembic init migrations

# Ensure alembic.ini uses correct database credentials
echo -e "${GREEN}Updating alembic.ini...${NC}"

# Update alembic.ini with correct connection string
sed -i '' "s|sqlalchemy.url = driver://user:pass@localhost/dbname|sqlalchemy.url = postgresql://${DB_USER}:${DB_PASSWORD}@localhost:5432/${DB_NAME}|" alembic.ini

# Check alembic.ini to verify the change
echo -e "${GREEN}Check the updated alembic.ini for the correct database URL:${NC}"
cat alembic.ini | grep sqlalchemy.url

# Create initial migration
echo -e "${GREEN}Creating initial migration...${NC}"
alembic revision --autogenerate -m "Initial migration"

# Run migrations
echo -e "${GREEN}Running migrations...${NC}"
alembic upgrade head

# Start the application
echo -e "${GREEN}Starting the application...${NC}"
uvicorn app.main:app --reload

echo -e "${BLUE}Setup complete!${NC}"
echo -e "${GREEN}You can now access:${NC}"
echo -e "API documentation: http://localhost:8000/docs"
echo -e "Alternative API documentation: http://localhost:8000/redoc"

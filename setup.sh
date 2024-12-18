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
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Server
DEBUG=True
EOL

# Initialize alembic
echo -e "${GREEN}Initializing Alembic...${NC}"
alembic init migrations

# Update alembic.ini
echo -e "${GREEN}Updating alembic.ini...${NC}"
sed -i '' 's|sqlalchemy.url = driver://user:pass@localhost/dbname|sqlalchemy.url = postgresql://user:password@localhost:5432/dbname|' alembic.ini

# Create initial migration
echo -e "${GREEN}Creating initial migration...${NC}"
alembic revision --autogenerate -m "Initial migration"

# Run migrations
echo -e "${GREEN}Running migrations...${NC}"
alembic upgrade head

# Start the application
echo -e "${GREEN}Starting the application...${NC}"
uvicorn backend.app.main:app --reload

echo -e "${BLUE}Setup complete!${NC}"
echo -e "${GREEN}You can now access:${NC}"
echo -e "API documentation: http://localhost:8000/docs"
echo -e "Alternative API documentation: http://localhost:8000/redoc" 
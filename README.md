# Food Saver API

## Setup developement environnement (Windows)
Create Python virtual env
`python -m venv .venv`

Activate Python virtual env
`source .venv/Scripts/activate`

Install depedencies
`pip install -r requirements.txt`

Create and fill env file
`cp .env.example .venv`

Create MySQL database
Run migrations
`flask db upgrade`
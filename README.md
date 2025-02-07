Python Backend: Caching Service
- A simple Python FastAPI service with a 
- GET and POST request to save user input as 
- JSON file and serve data with caching functionality
- alternately saving cached data into db table. 

📂 fast_assigment/
│── 📂 backend/              # Main application code  
│   ├── constants.py         # API routes  
│   ├── models.py            # Database models    
│   ├── main.py              # FastAPI app entry point  
|   ├── database.py          # Databse connection
|   ├── utils.py             # Utility functions
│── .env                     # Environment variables
│── .gitignore               # Git ignore file
│── .dockerignore            # Docker ignore file
│── Dockerfile               # Docker setup  
│── docker-compose.yml       # Docker compose file  
│── requirements.txt         # Python dependencies  
│── README.md                # Documentation  


Setup:
Install Docker on your local

git clone https://github.com/your-username/your-repo.git
cd fast_assigment
RUN: docker compose up --build
Go into your newly built docker container and run alembic migration commands:
 - `alembic init alembic`
 - Inside alembic.ini, find this line (`sqlalchemy.url = postgresql://user:password@localhost/dbname`)
 - Replace it with: `postgresql+psycopg2://<your_db_user>:<your_db_password>@localhost/<your_db_dbname>`

Go into .env file inside alembic folder and 
`replace target_metadata = None` 

to 

`from models import Base`
`target_metadata = Base.metadata`

Then run: 
`alembic revision --autogenerate -m "Initial migration"`
`alembic upgrade head`
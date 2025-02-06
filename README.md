Python Backend: Caching Service
- A simple Python FastAPI service with a GET and POST request to save user input as JSON file and serve data with caching functionality

📂 fast_assigment/
│── 📂 backend/              # Main application code  
│   ├── constants.py         # API routes  
│   ├── models.py            # Database models    
│   ├── main.py              # FastAPI app entry point  
|   ├── database.py          # Databse connection
|   ├── utils.py             # Utility functions
│── .env                     # Environment variables  
│── Dockerfile               # Docker setup  
│── docker-compose.yml       # Docker compose file  
│── requirements.txt         # Python dependencies  
│── README.md                # Documentation  


Setup:
Install Docker on your local

git clone https://github.com/your-username/your-repo.git
cd fast_assigment
RUN: docker compose up --build


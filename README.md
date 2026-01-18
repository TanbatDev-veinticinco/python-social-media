### The mini social feed application built with FastAPI

Project Overview

This project is a backend API for a simple social media application built with FastAPI.
It allows users to register, create posts (with optional image uploads), view posts, and like other users’ posts.

The project uses in-memory data storage (no database) and is designed for team collaboration, with clearly separated responsibilities.

🚀 Tech Stack

Python 3.10+

FastAPI

Uvicorn (ASGI server)

Pydantic (data validation)

Multipart form handling (for file uploads)

📂 Project Structure
Social-media/
│
├── main.py                 # Application entry point
├── routes/
│   ├── __init__.py
│   ├── users.py            # User-related routes
│   └── post.py             # Post-related routes
│
├── models.py                # Pydantic models (request/response)
├── storage/                # In-memory data structures
├── requirements.txt
└── README.md

🧩 API Endpoints
👤 User Endpoints
➕ Register a User

POST /users/

Request Body (JSON):

{
  "username": "john_doe",
  "email": "john@example.com"
}

📝 Post Endpoints
➕ Create a Post (with optional image upload)

POST /posts/

Form Data:

username (string)

title (string)

content (string)

image (optional file)

📄 List All Posts

GET /posts/

📄 List Posts by a Specific User

GET /users/{username}/posts

❤️ Like a Post

POST /posts/{post_id}/like

🧱 Data Models (In-Memory)

This project uses in-memory Python data structures instead of a database.

Examples:

Users stored in dictionaries

Posts stored in lists/dictionaries

Likes tracked using counters or sets

⚠️ Data will reset when the server restarts.

👥 Team Roles & Responsibilities

To support collaborative development, tasks are divided as follows:

👤 User Management

User registration

User validation

User-related routes

📝 Post Management

Create posts

Handle file/image uploads

Store post data

📰 Feed & Filtering

List all posts

Filter posts by user

❤️ Likes System

Like functionality

Like counters per post

▶️ How to Run the Project
1️⃣ Clone the Repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

2️⃣ Create a Virtual Environment
python -m venv env
source env/bin/activate   # On Windows: env\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Start the Server
uvicorn main:app --reload


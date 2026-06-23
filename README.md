# ⚡ FastAPI Project

A RESTful API built with **FastAPI** and **Python**, featuring a clean modular structure with a dedicated database layer and auto-generated interactive API documentation.

## 🖥️ Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-4B0082?style=for-the-badge&logo=uvicorn&logoColor=white)

## ✨ Features

- ⚡ High-performance REST API powered by FastAPI
- 🗄️ Persistent data storage with SQLite (`database.db`)
- 🏗️ Clean separation of concerns — app logic and database layer in separate folders
- 📄 Auto-generated interactive API docs via **Swagger UI** (`/docs`) and **ReDoc** (`/redoc`)
- 🔄 Data validation with **Pydantic** models
- 🔁 Hot reload during development with Uvicorn

## 📁 Project Structure

```
fastapiproj/
├── app/              # Core application — routes, models, schemas
├── database/         # Database configuration and session management
├── database.db       # SQLite database file
└── .gitignore
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Pronoobcodes/fastapiproj.git
   cd fastapiproj
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install fastapi uvicorn sqlalchemy
   ```
   > Or if a `requirements.txt` is added:
   > ```bash
   > pip install -r requirements.txt
   > ```

4. **Run the development server**
   ```bash
   uvicorn app.main:app --reload
   ```

5. Open your browser and navigate to:
   - **API Base:** `http://127.0.0.1:8000`
   - **Swagger Docs:** `http://127.0.0.1:8000/docs`
   - **ReDoc:** `http://127.0.0.1:8000/redoc`

## 📖 API Documentation

FastAPI automatically generates interactive documentation. Once the server is running, visit `/docs` to explore and test all available endpoints directly in your browser — no external tools like Postman needed.

## 🤝 Contributing

Pull requests are welcome! Feel free to open an issue to suggest improvements or report bugs.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

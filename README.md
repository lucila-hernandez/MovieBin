# 🎬 MovieBin

## Project Description

**MovieBin** is a personal movie tracker built with Flask, Tailwind CSS, and SQLAlchemy. It allows users to log in, add movies they’ve watched, track their personal ratings, and store the date they watched them — all in a clean, organized interface.

### MovieBin allows users to:
- Create a new account and log in securely  
- Add movies with details like title, genre, release year, and director  
- Track each movie’s personal rating and watched date  
- View all movies in a personal movie log  
- Edit or delete movie entries anytime  

### This project uses:
- **Flask** for the backend routing and form handling  
- **Flask-Login** for authentication  
- **Flask-WTF** for form management  
- **SQLAlchemy** for database models and queries  
- **Tailwind CSS** for styling  

---

## How to Run the App

1. Clone the repository:

```sh
    git clone https://github.com/your-username/moviebin.git
    cd moviebin

```

2. Install dependencies:

```sh
    python3 -m venv venv
    source venv/bin/activate  
    pip install -r requirements.txt
```

3. Start the development server:

```sh
    flask run
```

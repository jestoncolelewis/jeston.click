# Portfolio Website for Jeston Lewis

This is a portfolio website for [Jeston Lewis](https://linkedin.com/in/jestoncolelewis) hosted on Railway.

## Stack

- **Static Site**: HTML/CSS/JavaScript (www folder)
- **API Service**: Python 3.13 + Flask + Gunicorn
- **Database**: PostgreSQL
- **Platform**: Railway

## Project Structure

```
.
├── www/                  # Static website files
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── assets/
├── api/                  # Python API service
│   ├── app.py           # Flask application
│   ├── requirements.txt
│   └── init_db.py       # Database setup script
├── Procfile             # Railway process definition
└── railway.toml         # Railway configuration
```

## Deployment

See [DEPLOY.md](DEPLOY.md) for detailed deployment instructions.
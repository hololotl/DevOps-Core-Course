# DevOps Info Service (Flask)

## Overview

A lightweight Flask web service providing detailed information about itself and its runtime environment. Exposes system metrics, runtime statistics, and request metadata via JSON endpoints. Foundation for DevOps monitoring and containerization labs.

## Prerequisites

- Python 3.11+
- pip

## Installation

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running the Application

```bash
python app.py                    # Default: 0.0.0.0:5000
PORT=8080 python app.py          # Custom port
HOST=127.0.0.1 PORT=3000 python app.py
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service and system information (JSON) |
| `/health` | GET | Health check — returns status 200 if healthy |

## Configuration

Environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Bind address |
| `PORT` | `5000` | Bind port |
| `DEBUG` | `False` | Enable Flask debug mode |

Example:
```bash
HOST=127.0.0.1 PORT=3000 DEBUG=True python app.py
```

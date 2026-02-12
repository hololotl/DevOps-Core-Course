# DevOps Info Service (Go)

Lightweight HTTP server providing system and service information via JSON endpoints.

## Prerequisites

- Go 1.21+ installed

## Build

```bash
go build -o app_go main.go
```

**Binary size (optimized):**
```bash
go build -ldflags="-s -w" -o app_go main.go
ls -lh app_go
```

## Run

```bash
./app_go                    # Default: 0.0.0.0:5000
PORT=8080 ./app_go          # Custom port
HOST=127.0.0.1 PORT=3000 ./app_go
```

Or from source:
```bash
go run main.go
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
| `DEBUG` | `false` | Enable debug logging |



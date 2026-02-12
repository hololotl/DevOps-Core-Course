# LAB01 — Go Implementation Details

## Architecture

Pure Go implementation using only the standard library (`net/http`, `encoding/json`, `os`, `runtime`, etc.). No external dependencies.

## Key Differences from Flask

| Aspect | Flask (Python) | Go |
|--------|----------------|-----|
| Compilation | Interpreted | Compiled to binary |
| Dependencies | Requires venv + pip | Only Go toolchain |
| Binary size | N/A (uses Python runtime) | ~6-8 MB (optimized) |
| Startup | ~500ms | <10ms |
| Memory footprint | ~50-100 MB | ~10-15 MB |
| Concurrency | Threading/Async | Native goroutines |
| Build process | Just run with `python` | `go build` or `go run` |

## Implementation Details

### Main Components

1. **Struct Types** — JSON-serializable struct definitions for request/response
2. **Configuration** — Reads HOST, PORT, DEBUG from environment variables
3. **System Info Functions** — Retrieve hostname, platform, CPU count, Go version
4. **Uptime Calculation** — Track `startTime` at program start
5. **HTTP Handlers** — Main endpoint and health check
6. **Error Handling** — Custom 404/500 responses in JSON format
7. **Logging** — Standard `log` package for request tracking

### Code Structure

```go
type ServiceInfo struct { ... }     // Response structure
type SystemInfo struct { ... }      // System details
type RuntimeInfo struct { ... }     // Runtime stats
type RequestInfo struct { ... }     // Request metadata
type Endpoint struct { ... }        // API endpoint listing

func getUptime() (int, string)      // Calculate uptime
func getSystemInfo() SystemInfo     // Gather system info
func mainHandler()                  // GET / endpoint
func healthHandler()                // GET /health endpoint
func main()                         // Start HTTP server
```

### Performance Advantages

- **No runtime overhead** — Compiled directly to machine code
- **Minimal memory** — Lean standard library
- **Fast startup** — No interpreter initialization
- **Efficient concurrency** — One goroutine per request (automatic)

## Testing

```bash
# Build
go build -o app_go main.go

# Run
./app_go

# In another terminal
curl http://localhost:5000/ | jq
curl http://localhost:5000/health | jq
```

## Binary Size Comparison

```bash
# Go binary (optimized)
go build -ldflags="-s -w" -o app_go main.go
ls -lh app_go  # ~6 MB

# Python (with venv)
pip install -r requirements.txt
ls -lh venv/  # ~100+ MB
```

Go produces a **self-contained binary** with no dependencies, while Python requires the entire runtime and packages.

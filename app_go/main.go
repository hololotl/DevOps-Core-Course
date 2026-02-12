package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net"
	"net/http"
	"os"
	"runtime"
	"strings"
	"time"
)

// ServiceInfo represents the complete response structure
type ServiceInfo struct {
	Service   ServiceMeta `json:"service"`
	System    SystemInfo  `json:"system"`
	Runtime   RuntimeInfo `json:"runtime"`
	Request   RequestInfo `json:"request"`
	Endpoints []Endpoint  `json:"endpoints"`
}

type ServiceMeta struct {
	Name        string `json:"name"`
	Version     string `json:"version"`
	Description string `json:"description"`
	Framework   string `json:"framework"`
}

type SystemInfo struct {
	Hostname        string `json:"hostname"`
	Platform        string `json:"platform"`
	PlatformVersion string `json:"platform_version"`
	Architecture    string `json:"architecture"`
	CPUCount        int    `json:"cpu_count"`
	GoVersion       string `json:"go_version"`
}

type RuntimeInfo struct {
	UptimeSeconds int    `json:"uptime_seconds"`
	UptimeHuman   string `json:"uptime_human"`
	CurrentTime   string `json:"current_time"`
	Timezone      string `json:"timezone"`
}

type RequestInfo struct {
	ClientIP  string `json:"client_ip"`
	UserAgent string `json:"user_agent"`
	Method    string `json:"method"`
	Path      string `json:"path"`
}

type Endpoint struct {
	Path        string `json:"path"`
	Method      string `json:"method"`
	Description string `json:"description"`
}

type ErrorResponse struct {
	Error   string `json:"error"`
	Message string `json:"message"`
}

var (
	startTime = time.Now()
	config    struct {
		host  string
		port  string
		debug bool
	}
)

func init() {
	config.host = os.Getenv("HOST")
	if config.host == "" {
		config.host = "0.0.0.0"
	}

	config.port = os.Getenv("PORT")
	if config.port == "" {
		config.port = "5000"
	}

	debugStr := os.Getenv("DEBUG")
	config.debug = strings.ToLower(debugStr) == "true"
}

func getHostname() string {
	hostname, err := os.Hostname()
	if err != nil {
		return "unknown"
	}
	return hostname
}

func getPlatformVersion() string {
	// Go doesn't have a direct equivalent to platform.version()
	// Return uname or similar info
	return fmt.Sprintf("Go %s", runtime.Version())
}

func getUptime() (int, string) {
	delta := time.Since(startTime)
	seconds := int(delta.Seconds())
	hours := seconds / 3600
	minutes := (seconds % 3600) / 60
	human := fmt.Sprintf("%d hours, %d minutes", hours, minutes)
	return seconds, human
}

func getSystemInfo() SystemInfo {
	return SystemInfo{
		Hostname:        getHostname(),
		Platform:        runtime.GOOS,
		PlatformVersion: getPlatformVersion(),
		Architecture:    runtime.GOARCH,
		CPUCount:        runtime.NumCPU(),
		GoVersion:       strings.TrimPrefix(runtime.Version(), "go"),
	}
}

func getClientIP(r *http.Request) string {
	// Try X-Forwarded-For header first
	if xff := r.Header.Get("X-Forwarded-For"); xff != "" {
		return strings.Split(xff, ",")[0]
	}
	// Fall back to RemoteAddr
	ip, _, err := net.SplitHostPort(r.RemoteAddr)
	if err != nil {
		return r.RemoteAddr
	}
	return ip
}

func mainHandler(w http.ResponseWriter, r *http.Request) {
	log.Printf("Request: %s %s from %s", r.Method, r.URL.Path, getClientIP(r))

	uptimeSeconds, uptimeHuman := getUptime()
	now := time.Now().UTC().Format(time.RFC3339)
	// Convert to Z format
	now = strings.Replace(now, "+00:00", "Z", 1)

	info := ServiceInfo{
		Service: ServiceMeta{
			Name:        "devops-info-service",
			Version:     "1.0.0",
			Description: "DevOps course info service",
			Framework:   "Go (net/http)",
		},
		System: getSystemInfo(),
		Runtime: RuntimeInfo{
			UptimeSeconds: uptimeSeconds,
			UptimeHuman:   uptimeHuman,
			CurrentTime:   now,
			Timezone:      "UTC",
		},
		Request: RequestInfo{
			ClientIP:  getClientIP(r),
			UserAgent: r.Header.Get("User-Agent"),
			Method:    r.Method,
			Path:      r.RequestURI,
		},
		Endpoints: []Endpoint{
			{Path: "/", Method: "GET", Description: "Service information"},
			{Path: "/health", Method: "GET", Description: "Health check"},
		},
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(info)
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
	uptimeSeconds, _ := getUptime()
	now := time.Now().UTC().Format(time.RFC3339)
	now = strings.Replace(now, "+00:00", "Z", 1)

	response := map[string]interface{}{
		"status":         "healthy",
		"timestamp":      now,
		"uptime_seconds": uptimeSeconds,
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(response)
}

func notFoundHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusNotFound)
	json.NewEncoder(w).Encode(ErrorResponse{
		Error:   "Not Found",
		Message: "Endpoint does not exist",
	})
}

func main() {
	log.Println("DevOps Info Service starting")

	// Route handlers
	http.HandleFunc("/", mainHandler)
	http.HandleFunc("/health", healthHandler)

	// Custom 404 for all other paths
	http.HandleFunc("/{path}", notFoundHandler)

	addr := net.JoinHostPort(config.host, config.port)
	log.Printf("Listening on %s", addr)

	if err := http.ListenAndServe(addr, nil); err != nil {
		log.Fatalf("Server error: %v", err)
	}
}

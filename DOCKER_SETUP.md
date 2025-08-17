# 🐳 Docker Setup Guide for RemotelyX Platform

## 📋 Overview

This Docker setup provides a complete containerized environment for the RemotelyX platform with all necessary services.

## 🏗️ Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Frontend   │───▶│   Backend   │───▶│  Databases  │───▶│     n8n     │
│ (Streamlit) │    │  (FastAPI)  │    │(Mongo+Redis)│    │ (Workflows) │
│   :8501     │    │    :8000    │    │:27017 :6379 │    │    :5678    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                                                              │
                                                              ▼
                                                      ┌─────────────┐
                                                      │   Ollama    │
                                                      │ (Local AI)  │
                                                      │   :11434    │
                                                      └─────────────┘
```

## 🚀 Quick Start

### Windows

```cmd
# Start all services
docker-start.bat

# Or manually
docker-compose up -d
```

### Linux/Mac

```bash
# Start all services
./docker-start.sh

# Or manually
docker-compose up -d
```

## 📦 Services Included

| Service        | Container Name       | Port  | Description         |
| -------------- | -------------------- | ----- | ------------------- |
| **Frontend**   | `remotelyx_frontend` | 8501  | Streamlit Dashboard |
| **Backend**    | `remotelyx_backend`  | 8000  | FastAPI Server      |
| **MongoDB**    | `remotelyx_mongodb`  | 27017 | Primary Database    |
| **Redis**      | `remotelyx_redis`    | 6379  | Cache & Sessions    |
| **n8n**        | `remotelyx_n8n`      | 5678  | Workflow Automation |
| **PostgreSQL** | `remotelyx_postgres` | 5432  | n8n Database        |
| **Ollama**     | `remotelyx_ollama`   | 11434 | Local AI Service    |

## 🌐 Access URLs

After starting the services, access them at:

- **Frontend Dashboard**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **n8n Workflows**: http://localhost:5679 (or your ngrok URL)
- **Ollama AI**: http://localhost:11434

## 🔐 Default Credentials

### MongoDB

- **Username**: `admin`
- **Password**: `password123`
- **Database**: `remotelyx_dashboard`

### n8n

- **Username**: `hadihaidar1723@gmail.com`
- **Password**: `Treble23!`

### Application Demo Accounts

- **Admin**: `admin` / `admin123`
- **Manager**: `racile` / `password123`
- **Demo**: `demo` / `secret123`
- **User**: `user` / `hello123`

## 🛠️ Management Commands

### Docker Compose Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f frontend
docker-compose logs -f backend

# Check service status
docker-compose ps

# Restart specific service
docker-compose restart backend

# Rebuild and restart
docker-compose up -d --build
```

### Individual Service Management

```bash
# Restart specific containers
docker restart remotelyx_frontend
docker restart remotelyx_backend

# View container logs
docker logs remotelyx_frontend
docker logs remotelyx_backend

# Execute commands in containers
docker exec -it remotelyx_backend bash
docker exec -it remotelyx_mongodb mongosh
```

## 🤖 AI Setup (Ollama)

After starting the services, set up the AI model:

```bash
# Pull the required model (this may take several minutes)
docker exec remotelyx_ollama ollama pull llama3.2

# Verify model is available
docker exec remotelyx_ollama ollama list

# Test AI service
curl http://localhost:11434/api/version
```

## 📊 Health Checks

The docker-compose includes health checks for all services:

```bash
# Check all service health
docker-compose ps

# Detailed health status
docker inspect remotelyx_backend | grep Health -A 5
```

## 🔧 Environment Variables

Key environment variables (configurable in docker-compose.yml):

### Backend

```env
MONGODB_URL=mongodb://admin:password123@mongodb:27017/remotelyx_dashboard?authSource=admin
REDIS_URL=redis://redis:6379/0
SECRET_KEY=your-super-secret-key-change-in-production
OLLAMA_MODEL=llama3.2
```

### n8n

```env
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=n8n_admin
WEBHOOK_URL=http://localhost:5678/
```

## 📁 Volume Mounts

Persistent data is stored in Docker volumes:

- `mongodb_data` - MongoDB database files
- `redis_data` - Redis data
- `n8n_data` - n8n workflow data
- `postgres_data` - PostgreSQL data for n8n
- `ollama_data` - Ollama AI models

## 🚨 Troubleshooting

### Common Issues

1. **Port conflicts**

   ```bash
   # Check what's using the ports
   netstat -an | findstr :8501
   netstat -an | findstr :8000
   ```

2. **Services not starting**

   ```bash
   # Check logs for errors
   docker-compose logs

   # Restart problematic service
   docker-compose restart service_name
   ```

3. **Database connection issues**

   ```bash
   # Check MongoDB is running
   docker exec remotelyx_mongodb mongosh --eval "db.adminCommand('ping')"

   # Check Redis is running
   docker exec remotelyx_redis redis-cli ping
   ```

4. **AI model not working**

   ```bash
   # Re-pull the model
   docker exec remotelyx_ollama ollama pull llama3.2

   # Check Ollama logs
   docker logs remotelyx_ollama
   ```

### Performance Optimization

1. **Increase Docker resources** (Docker Desktop → Settings → Resources)

   - RAM: At least 8GB recommended
   - CPU: At least 4 cores recommended

2. **Clean up unused data**
   ```bash
   docker system prune
   docker volume prune
   ```

## 🔄 Development Workflow

For development with live reloading:

1. **Frontend development**

   ```bash
   # Stop containerized frontend
   docker-compose stop frontend

   # Run locally
   cd client
   streamlit run app.py
   ```

2. **Backend development**

   ```bash
   # Stop containerized backend
   docker-compose stop backend

   # Run locally
   cd server
   uvicorn main:app --reload
   ```

## 📚 Integration Examples

### n8n Workflow Integration

1. Access n8n at http://localhost:5678
2. Create a workflow with HTTP Request node
3. Configure endpoint: `http://backend:8000/api/v1/scraper/scrape`
4. Add job URL as request body

### API Usage Examples

```bash
# Health check
curl http://localhost:8000/health

# Scrape a job
curl -X POST http://localhost:8000/api/v1/scraper/scrape \
  -H "Content-Type: application/json" \
  -d '{"job_url": "https://example.com/job-posting"}'

# Get recent jobs
curl http://localhost:8000/api/v1/scraper/jobs?limit=5
```

---

**🎉 Your RemotelyX platform is now fully containerized and ready for development or production use!**

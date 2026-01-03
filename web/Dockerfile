# Multi-Stage Dockerfile for Production Deployment
# Builds frontend and backend into a single container

# ============================================
# Stage 1: Build Frontend
# ============================================
FROM node:20 AS frontend-builder

WORKDIR /app/frontend

# Copy package files (only package.json, not package-lock.json)
# package-lock.json can cause issues with optional dependencies during Docker builds
COPY frontend/package.json ./

# Install dependencies
# Using npm install without lock file to avoid optional dependencies bug
# See: https://github.com/npm/cli/issues/4828
RUN npm install

# Copy frontend source
COPY frontend/ ./

# Build frontend for production
RUN npm run build

# ============================================
# Stage 2: Build Backend
# ============================================
FROM python:3.11-slim AS backend-builder

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# ============================================
# Stage 3: Production Image
# ============================================
FROM python:3.11-slim

WORKDIR /app

# Copy Python dependencies from builder
COPY --from=backend-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-builder /usr/local/bin /usr/local/bin

# Copy backend code
COPY backend/ ./backend/

# Copy built frontend from frontend-builder
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Create necessary directories
RUN mkdir -p /app/data /app/static

# Expose port (fly.io will map this internally)
EXPOSE 8080

# Health check (optional, can be removed if not needed)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/api/health').read()" || exit 1

# Start application
# Note: We use port 8080 as configured in fly.toml
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8080"]

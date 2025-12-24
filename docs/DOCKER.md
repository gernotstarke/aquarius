# Docker Compose for Jekyll Documentation Site

## 🚀 Quick Start (Apple Silicon Compatible)

Start the Jekyll server:

```bash
cd docs
docker compose up
```

Visit: **http://localhost:4000**

The server will automatically reload when you make changes to:
- `_pages/*.md`
- `_config.yml`
- `index.html`
- CSS/assets

## 🛠️ Commands

### Start Server (with live reload)
```bash
docker compose up
```

### Start in Background
```bash
docker compose up -d
```

### Stop Server
```bash
docker compose down
```

### Rebuild and Start (after Gemfile changes)
```bash
docker compose down
docker compose up --build
```

### View Logs
```bash
docker compose logs -f jekyll
```

### Install Dependencies Only
```bash
docker compose run --rm jekyll bundle install
```

### Clean Build Cache
```bash
docker compose run --rm jekyll bundle exec jekyll clean
```

## 📦 Apple Silicon Notes

This configuration is fully compatible with Apple Silicon (M1/M2/M3):

- Uses `platform: linux/arm64` for native arm64 support
- Official Jekyll image supports multi-architecture
- Gem cache persisted in named volume for fast rebuilds
- No Rosetta translation needed

## 🔧 Customization

### Change Port

Edit `docker-compose.yml`:
```yaml
ports:
  - "8080:4000"  # Access at localhost:8080
```

### Disable LiveReload

Edit command in `docker-compose.yml`:
```yaml
command: jekyll serve --host 0.0.0.0
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find and kill process on port 4000
lsof -ti:4000 | xargs kill -9
```

### Gem Installation Errors
```bash
# Remove volume and rebuild
docker compose down -v
docker compose up
```

### File Permission Issues
```bash
# Reset permissions (macOS)
sudo chown -R $(whoami) .
```

## 📝 Workflow

1. Make changes to documentation files
2. Jekyll auto-rebuilds (watch console output)
3. Browser auto-reloads (if LiveReload enabled)
4. View changes at http://localhost:4000

---

*Optimized for macOS Apple Silicon*

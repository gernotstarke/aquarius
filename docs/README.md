# Aquarius Documentation Site

This directory contains the Jekyll-based documentation site for the Aquarius project.

## 🎨 Design

The site uses the **minimal-mistakes** theme with a clean, professional design inspired by arc42.org:

- **Homepage**: Three prominent section boxes (Requirements, Architecture, Application)
- **Responsive**: Mobile-friendly grid layout
- **Clean**: Minimalist air theme, easy navigation

## 🏗️ Structure

```
docs/
├── _config.yml          # Jekyll configuration
├── index.md             # Homepage with feature_row layout
├── _pages/              # Section pages
│   ├── requirements.md  # Requirements documentation (req42)
│   ├── architecture.md  # Architecture documentation (arc42)
│   └── app.md          # Application documentation
├── assets/
│   ├── images/         # Site images (logos, backgrounds)
│   │   └── icons/      # Section icons (optional)
│   ├── css/            # Custom stylesheets (optional)
│   └── js/             # Custom JavaScript (optional)
├── Gemfile             # Ruby dependencies
└── docker-compose.yml  # Local development (Apple Silicon compatible)
```

## 🚀 Deployment

The site deploys automatically to GitHub Pages when you push changes to the `docs/` folder:

1. **Automatic**: Push to `main` branch with changes in `docs/**`
2. **Manual**: Trigger via GitHub Actions workflow_dispatch

The workflow ensures that changes outside `docs/` don't trigger unnecessary rebuilds.

## 🛠️ Local Development

To run the site locally:

```bash
cd docs
bundle install
bundle exec jekyll serve
```

Visit: http://localhost:4000

## 📝 Adding Content

### Requirements (req42 format)
Edit: `_pages/requirements.md`

### Architecture (arc42 format)
Edit: `_pages/architecture.md`

### Application Documentation
Edit: `_pages/app.md`

## 🔧 Customization

- **Theme skin**: Edit `minimal_mistakes_skin` in `_config.yml`
- **Colors**: Modify custom CSS in `index.html` (`.feature-box` styles)
- **Sections**: Add new pages in `_pages/` directory

## 📦 GitHub Pages Setup

Ensure your repository settings are configured:

1. Go to Settings → Pages
2. Source: GitHub Actions
3. The workflow will handle the rest

The site will be available at: `https://aquarius.arc42.org` (with CNAME configured)

---

*Based on minimal-mistakes theme, styled like arc42.org family sites*

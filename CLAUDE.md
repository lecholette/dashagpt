# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DashaGPT is an AI-powered Vedic astrology web application built with Flask. The architecture is modeled after the chinese-horoscope project, featuring a clean separation between calculation logic (core_lib), web services (web), and presentation (templates).

## Technology Stack

- **Framework**: Flask 3.0+ with Gunicorn
- **Python Version**: 3.11 (NOT 3.13+)
- **Astrology**: pyswisseph (Swiss Ephemeris)
- **AI**: Google Gemini API
- **PDF Generation**: WeasyPrint
- **Payment**: Stripe
- **Deployment**: Heroku

## Project Structure

```
dashagpt/
├── app.py                    # Main Flask application (entry point)
├── core_lib/                 # Core calculation & AI logic
│   ├── calculator/          # Vedic chart calculations
│   ├── ai_integration/      # AI-powered interpretations
│   ├── core/                # Core utilities & constants
│   └── data/                # Static data
├── web/                     # Web services layer
│   └── services/            # Business logic (PDF, payments, email)
├── templates/               # Jinja2 templates
│   ├── base.html           # Base template with GA4
│   ├── landing.html        # Main landing page
│   ├── calculator.html     # Birth data input form
│   ├── pdf/                # PDF-specific templates
│   ├── legal/              # Privacy/Terms pages
│   └── errors/             # Error pages
├── static/                  # Static assets
│   ├── images/             # WebP images only
│   ├── css/                # Stylesheets
│   └── [SEO files]         # robots.txt, sitemap.xml
├── scripts/                # Utility scripts
└── tests/                  # Test suite
    └── unit/               # Unit tests
```

## Development Commands

### Environment Setup

```bash
# Create virtual environment (Python 3.11)
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Running the Application

```bash
# Development server
python app.py

# Or with Flask CLI
flask run --port=5000

# Production simulation
gunicorn app:app --workers=3 --bind 0.0.0.0:5000
```

### Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/unit/calculator/test_calculations.py -v

# Run with coverage
pytest tests/ --cov=core_lib --cov-report=html

# Run specific test
pytest tests/unit/calculator/test_calculations.py::TestClass::test_method -v
```

### Code Quality

```bash
# Format code
black .

# Lint
flake8
```

## Architecture Guidelines

### Modular Design Pattern

The application follows a strict separation of concerns:

1. **core_lib/** - Pure calculation logic, no Flask dependencies
   - `calculator/` - Vedic astrology calculations (planets, houses, dashas)
   - `ai_integration/` - AI prompt templates and response parsing
   - `core/` - Constants, utilities, exceptions
   - `data/` - Static astrology data

2. **web/** - Web-specific services
   - `services/` - Business logic (PDF generation, payments, email)
   - Should import from core_lib, never the reverse

3. **app.py** - Flask application factory
   - Route registration
   - Error handlers
   - Middleware configuration

### Key Design Principles

- **Optional Services**: PDF generation, payments, and email should be optional with graceful fallbacks
- **Pre-generated Content**: Consider caching AI-generated content as Python data files to reduce API calls
- **Session Management**: Keep session data minimal (birth details only), recalculate charts on demand
- **Testing First**: Write comprehensive unit tests for all calculation logic
- **WebP Images**: All images must be WebP format for optimization

## Configuration

### Required Environment Variables

```bash
SECRET_KEY=<generate-secure-key>
GEMINI_API_KEY=<google-api-key>
```

### Optional Environment Variables

```bash
# Payment (Optional)
STRIPE_PUBLISHABLE_KEY=pk_xxx
STRIPE_SECRET_KEY=sk_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx

# Email (Optional)
SENDGRID_API_KEY=SG.xxx

# Storage (Optional)
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx
S3_BUCKET_NAME=dashagpt-pdfs

# Error Tracking (Optional)
SENTRY_DSN=https://xxx@sentry.io/xxx

# Analytics
GA4_MEASUREMENT_ID=G-XXXXXXXXXX
```

## Deployment

### Heroku Deployment

The project is configured for Heroku deployment:

- **Procfile**: `web: gunicorn app:app`
- **runtime.txt**: Python 3.11
- **Aptfile**: System dependencies for PDF generation (Cairo, Pango)

```bash
# Create Heroku app
heroku create dashagpt

# Set environment variables
heroku config:set SECRET_KEY=xxx
heroku config:set GEMINI_API_KEY=xxx

# Deploy
git push heroku main
```

### System Dependencies

The Aptfile includes required system libraries for WeasyPrint PDF generation:
- libpango-1.0-0 (text rendering)
- libcairo2 (graphics)
- libgdk-pixbuf2.0-0 (images)

## Code Conventions

### File Organization

- **Route handlers**: Keep in `app.py` or separate into `web/routes/` if it grows beyond ~500 lines
- **Business logic**: Always in `web/services/`, never in route handlers
- **Calculations**: Always in `core_lib/calculator/`, no Flask dependencies
- **AI integration**: In `core_lib/ai_integration/`, with clear prompt templates

### Import Standards

```python
# Good - core_lib has no Flask dependencies
from core_lib.calculator.natal_chart import calculate_birth_chart
from web.services.pdf_generator import generate_pdf

# Bad - core_lib should never import from web
from web.services.something import foo  # in core_lib/ file
```

### Testing Standards

- Write tests for all calculation logic in `core_lib/`
- Use pytest fixtures for Flask app and client
- Mock external services (AI, payments, email)
- Test edge cases (timezone boundaries, date boundaries)

## Common Development Tasks

### Adding a New Route

1. Add route handler in `app.py` (or create new blueprint)
2. Create corresponding template in `templates/`
3. Update `static/sitemap.xml` if it's a public page
4. Add tests in `tests/unit/routes/`

### Adding a New Calculation

1. Create module in `core_lib/calculator/`
2. Write comprehensive unit tests first
3. Import and use in `web/services/` layer
4. Never add Flask dependencies to core_lib

### Adding AI-Generated Content

1. Create prompt template in `core_lib/ai_integration/prompts.py`
2. Add response parsing logic
3. Consider pre-generating content via batch scripts (see `scripts/`)
4. Cache results as Python data files for production

## Known Limitations

- **Python Version**: Locked to 3.11 (not 3.13+ due to dependency compatibility)
- **Session Size**: Keep session data under 3800 bytes (browser cookie limit)
- **PDF Generation**: WeasyPrint is CPU-intensive, consider background job queue for production
- **AI Rate Limits**: Gemini API has quotas, implement rate limiting and caching

## SEO Infrastructure

- **robots.txt**: Located in `static/robots.txt`
- **sitemap.xml**: Located in `static/sitemap.xml` (update when adding public pages)
- **GA4**: Integrated in `templates/base.html`
- **Meta Tags**: Use `{% block meta_description %}` in templates

## Resources

- **Repository**: https://github.com/lecholette/dashagpt
- **Reference Project**: ~/chinese-horoscope (similar architecture)
- **Deployment**: Heroku (main branch auto-deploys)

## Quick Reference

```bash
# Common workflows
source venv/bin/activate          # Activate virtualenv
python app.py                     # Run dev server
pytest tests/ -v                  # Run tests
git push heroku main             # Deploy to production
```

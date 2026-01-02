# DashaGPT

AI-Powered Vedic Astrology Birth Charts and Predictions

## Overview

DashaGPT provides accurate Vedic astrology birth chart calculations with AI-powered personalized insights. Built with Flask and modern web technologies.

## Quick Start

### Prerequisites

- Python 3.11
- pip
- virtualenv

### Installation

```bash
# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run development server
python app.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
dashagpt/
├── app.py                  # Main Flask application
├── core_lib/              # Core calculation & AI logic
│   ├── calculator/        # Vedic chart calculations
│   ├── ai_integration/    # AI-powered interpretations
│   ├── core/              # Core utilities & constants
│   └── data/              # Static data
├── web/                   # Web services layer
│   └── services/          # Business logic services
├── templates/             # Jinja2 templates
├── static/                # Static assets
├── scripts/               # Utility scripts
└── tests/                 # Test suite
```

## Configuration

Required environment variables:

- `SECRET_KEY` - Flask secret key
- `GEMINI_API_KEY` - Google Gemini API key for AI insights

Optional:
- `STRIPE_*` - Payment processing
- `SENDGRID_API_KEY` - Email delivery
- `SENTRY_DSN` - Error tracking
- `GA4_MEASUREMENT_ID` - Google Analytics

## Development

```bash
# Run tests
pytest tests/

# Run specific test
pytest tests/unit/calculator/test_calculations.py -v

# Code formatting
black .

# Linting
flake8
```

## Deployment

### Heroku

```bash
# Login to Heroku
heroku login

# Create app
heroku create dashagpt

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set GEMINI_API_KEY=your-api-key

# Deploy
git push heroku main
```

## License

Proprietary - All Rights Reserved

## Support

For support, email support@dashagpt.com

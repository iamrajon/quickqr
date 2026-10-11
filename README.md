# QuickQR — Instant QR Code Generator

A clean, modern, and high-performance QR code generator built with **Django 6**, managed with **uv**, linted and formatted with **Ruff**, and tested with **pytest**.

---

## ✨ Features

- **⚡ One-Click Generation:** Paste or type any link/text and generate scannable QR codes instantly without full-page reloads.
- **📋 Clipboard Helpers:** Dedicated "Paste from Clipboard" button for immediate input.
- **🎨 Custom Styling & Colors:**
  - Foreground & background color pickers with quick preset palettes (Dark Slate, Indigo, Emerald, Crimson, Purple).
  - Configurable resolution settings (Compact 200px up to Ultra-Res 600px).
  - Error correction levels (Low, Medium, Quartile, High).
- **💾 Multiple Export Options:**
  - Download high-res **PNG** image.
  - Download vector **SVG** file.
  - One-click **Copy Image to Clipboard**.
- **🕒 Local History:** Automatically preserves recent generations in browser local storage for fast re-access.
- **✨ Clean & Responsive UI:** Dark glassmorphism design with modern typography, glowing accents, and micro-animations.

---

## 🛠️ Tech Stack

- **Framework:** Django `6.1.2`
- **Package Manager:** [uv](https://docs.astral.sh/uv/)
- **Linter & Formatter:** [Ruff](https://docs.astral.sh/ruff/)
- **Test Runner:** [pytest](https://docs.pytest.org/) with `pytest-django`
- **QR Engine:** `qrcode[pil]` with Pillow

---

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have `uv` installed:
```bash
uv --version
```

### 2. Install Dependencies
```bash
uv sync
```

### 3. Run Migrations
```bash
uv run python manage.py migrate
```

### 4. Start Development Server
```bash
uv run python manage.py runserver
```
Visit the application in your browser at: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 🧪 Testing

Run the full automated test suite using `pytest`:
```bash
uv run pytest
```

Tests cover:
- QR code generation service (PNG bytes, Base64 data URI, SVG string, error correction).
- Form validation and color hex checking.
- Web views (HTML submission, JSON/AJAX API, and download endpoints).

---

## 🧹 Code Quality & Linting

Run Ruff to check lint rules and formatting:

```bash
# Check for lint issues
uv run ruff check .

# Auto-fix lint issues
uv run ruff check --fix .

# Check formatting
uv run ruff format --check .

# Format files
uv run ruff format .
```

---

## 📁 Project Structure

```
qr_generator/
├── config/                  # Django project configuration
│   ├── settings.py          # Settings configured for Django 6 & generator app
│   ├── urls.py              # Root URL routing
│   ├── wsgi.py
│   └── asgi.py
├── generator/               # QR Generator application
│   ├── forms.py             # Form validation & parameter mapping
│   ├── services.py          # Core QR code generation service (PNG, SVG, Base64)
│   ├── views.py             # Web views & JSON API handlers
│   ├── urls.py              # App URLs (index, download)
│   ├── templates/
│   │   └── generator/
│   │       └── index.html   # Modern responsive UI
│   ├── static/
│   │   └── generator/
│   │       ├── css/style.css # Custom design system & animations
│   │       └── js/app.js    # Client-side reactivity, fetch, clipboard & history
│   └── tests/               # Pytest suite
│       ├── test_forms.py
│       ├── test_services.py
│       └── test_views.py
├── pyproject.toml           # Project dependencies, ruff, & pytest configuration
├── uv.lock                  # Deterministic dependency lockfile
├── manage.py
└── README.md
```

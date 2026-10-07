# WolfWorks Engineering Toolkit

A modular, browser-based collection of engineering calculators, industrial automation utilities, and developer reference tools. Built with **Python and Flask**, WolfWorks Toolkit is intended to make frequently used engineering calculations and configuration tasks accessible from one place.

**Live application:** https://tools.wolfworks.tech  
**Source repository:** https://github.com/LoneWolf862/WolfWorks-Toolkit  
**Status:** Working, publicly deployed, and under active development.

> **Project scope:** This is an evolving engineering toolkit, not a completed suite of every planned utility. Some listed tools are planned rather than implemented; see [Future Work](#future-work).

## Features

### Electrical engineering

- **Ohm's Law:** Calculate voltage, current, resistance, and power from applicable inputs.
- **Voltage divider:** Calculate divider output from source voltage and resistors.
- **Series/parallel resistance:** Determine equivalent resistance for common resistor networks.
- **ADC/DAC calculations:** Work with analog-to-digital and digital-to-analog conversions.
- **Industrial analog scaling:** Convert between engineering units and signal ranges, including 4–20 mA and voltage ranges.
- **Digital clock and timing:** Calculate frequency, period, divider, timer, PWM, and UART timing quantities.

### PLC and industrial automation

- **PLC I/O Tag Manager:** Create, review, edit, and delete I/O records using a persistent SQLite database.
- Configure digital and analog points, including analog signal metadata.
- Validate submitted records to reduce invalid and duplicate configurations.

### File formats reference

- Browse reference information for **JSON, JSONC, YAML, XML, CSV, TSV, INI, TOML, SQLite, XLSX, NBT, and REG**.
- View extensions, categories, storage types, readability, comment support, and common uses.
- Each format has a dedicated reference page.
- **Not yet implemented:** File upload/inspection, JSON editor tools, CSV/TSV tools, and format conversion.

## Instructions for Build and Use

### Requirements

- **Python 3.12+** (developed with Python 3.12 on Windows; deployed with Python 3.13 on Linux).
- **Git** to clone the repository.
- A modern web browser.
- Python packages from `requirements.txt`.

### Install and run locally

1. Clone the public repository and enter its directory:

   ```bash
   git clone https://github.com/LoneWolf862/WolfWorks-Toolkit.git
   cd WolfWorks-Toolkit
   ```

2. Create and activate a virtual environment:

   **Windows (Command Prompt):**
   ```cmd
   py -m venv .venv
   .venv\Scripts\activate
   ```

   **Linux/macOS:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Initialize or update the local database schema:

   ```bash
   python -m flask --app run.py db upgrade
   ```

5. Start the development server:

   ```bash
   python run.py
   ```

6. Open **http://127.0.0.1:5000/** in your browser.

> **Important:** `python run.py` enables Flask debug mode and is intended **only for local development**. Do not expose this debug server to the public internet. The production deployment uses Gunicorn behind a reverse proxy.

### Instructions for using the software

1. Open the local URL above, or visit the hosted application.
2. Choose a category or tool from the navigation.
3. Enter the required values, select units or modes, and submit the form to calculate a result.
4. For PLC I/O management, use the configurator to create, view, edit, and remove I/O points; records persist in the application database.
5. For file-format information, visit `/file-formats/` and open **Format Reference**. You can also navigate directly to `/file-formats/reference/`.

**Known issue:** At the time of this README, the header's **File Formats** link is not connected to the new route. The pages themselves work via their direct URLs.

### Running tests

With the virtual environment active:

```bash
python -m pytest
```

At the October 2026 submission checkpoint, the test suite passed **209 tests**. The suite covers calculations, route responses, PLC operations, and file-format reference data. Test counts will change as development continues.

### Database and migrations

- The application uses **SQLite** for persistent data and **Flask-SQLAlchemy** for ORM integration.
- Schema changes are managed through **Flask-Migrate/Alembic**.
- Apply committed migrations using `python -m flask --app run.py db upgrade`.
- Local database contents are environment-specific; do not commit private or production database files.
- Back up the database before applying migrations to an existing production installation.

### Updating an existing installation

```bash
git pull origin main
python -m pip install -r requirements.txt
python -m flask --app run.py db upgrade
python -m pytest
```

Restart the application's process or service **only after** verifying the update. The hosted instance uses a systemd-managed Gunicorn service; the reverse proxy and TLS configuration are managed separately from this repository.

## Development Environment

The project was developed and tested on **Windows** and **Linux**, using a Python virtual environment and Git/GitHub version control.

Primary technologies:

| Technology | Version / role |
| --- | --- |
| Python | 3.12 (Windows development); 3.13 (Linux deployment) |
| Flask | 3.1.3 — web framework |
| Jinja2 | 3.1.6 — HTML templating |
| Flask-SQLAlchemy | 3.1.1 — database integration |
| SQLAlchemy | 2.0.54 — ORM/database layer |
| Flask-Migrate | 4.1.0 — schema migrations |
| Alembic | 1.20.0 — migration engine |
| pytest | 9.1.1 — automated tests |
| Gunicorn | 26.2.0 — production WSGI server (Linux) |
| HTML/CSS/JavaScript | Web interface and browser-side behavior |
| SQLite | Local relational database |
| Git / GitHub | Version control and public source hosting |

All pinned Python package versions, including indirect dependencies, are recorded in **`requirements.txt`**, which is the authoritative installation list.

## Project Structure

```text
WolfWorks-Toolkit/
├── run.py                    # Flask application entry point
├── requirements.txt          # Python dependencies
├── migrations/               # Database schema migration history
├── tests/                    # Automated pytest tests
└── wolfworks/
    ├── __init__.py           # Application factory and blueprint registration
    ├── core/                 # Core site routes
    ├── electrical/           # Electrical and timing calculators
    ├── plc/                  # PLC I/O tools and data handling
    ├── file_formats/         # Format catalog and routes
    ├── templates/            # Jinja2 HTML templates
    └── static/               # CSS, JavaScript, and static assets
```

The application uses **Flask blueprints** to keep tool families separate and make new tools easier to add without rewriting the rest of the site.

## Architecture and Deployment

**Request flow:** Browser → HTTPS reverse proxy → Gunicorn → Flask application → calculator logic or SQLite database → rendered HTML response.

The public instance is hosted on a Linux server and runs behind **Nginx** with HTTPS. **Gunicorn** serves the Flask application, and **systemd** manages its process. Hosting configuration, server credentials, DNS, and private database data are not part of this public source repository.

This architecture separates development from deployment and permits testing changes locally before publishing them.

## Quality and Testing

- Automated tests are written with **pytest**.
- Tests cover representative calculations, route availability, invalid inputs, and database-backed functionality.
- The File Formats module includes checks for its catalog metadata, listing pages, detail pages, and missing-format responses.
- At the October 2026 checkpoint, **209 tests passed** on the deployed Linux environment.

**Limitations:** Passing tests does not mean all planned features exist or that every edge case has been exercised. Engineering results should be independently verified before use in safety-critical or production control systems.

## Useful Websites to Learn More

Resources useful for developing and maintaining this project:

- [Flask Documentation](https://flask.palletsprojects.com/) — routing, blueprints, request handling, and application factories.
- [Jinja Documentation](https://jinja.palletsprojects.com/) — template inheritance and dynamic HTML.
- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.readthedocs.io/) — database models and sessions.
- [Flask-Migrate Documentation](https://flask-migrate.readthedocs.io/) — database migration workflow.
- [pytest Documentation](https://docs.pytest.org/) — automated Python testing.
- [Python Documentation](https://docs.python.org/3/) — language and standard library reference.
- [Git Documentation](https://git-scm.com/doc) — version control.
- [Gunicorn Documentation](https://docs.gunicorn.org/) — production Python application serving.

## Future Work

- [ ] Fix the **File Formats** header navigation link.
- [ ] Expand the file-format catalog with descriptions, examples, trade-offs, and related formats.
- [ ] Implement a safe **Data Inspector** for pasted or uploaded files.
- [ ] Add JSON validation, formatting, and inspection tools.
- [ ] Add CSV/TSV inspection and data conversion utilities.
- [ ] Improve search, filtering, and navigation across tool/reference pages.
- [ ] Expand automated tests and validate additional edge cases.
- [ ] Improve UI responsiveness, accessibility, and mobile layouts.
- [ ] Continue adding engineering and automation tools as independent modules.

## Project Notes

This project began as a CSE 310 Applied Programming module and is intended to continue as an independently maintained engineering resource. Its modular structure is deliberate: new utilities can be added without combining unrelated projects into one codebase.

**Disclaimer:** Calculators and reference material are educational and productivity aids. Verify values, units, assumptions, and relevant engineering standards before relying on outputs for physical systems.

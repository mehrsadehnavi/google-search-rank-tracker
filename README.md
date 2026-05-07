# SEO Keyword Rank Tracking System

## Overview
This project is an automated SEO rank tracking system that monitors the position of websites in Google search results for specific keywords.

The application provides RESTful APIs for managing tracked domains and keywords, performs automated web scraping using Selenium, stores ranking history in a database, and supports scheduled execution for continuous monitoring.

---

## Features

- Track Google search rankings for multiple websites
- Automated keyword-based scraping using Selenium
- RESTful API built with Flask-RESTful
- SQLite database integration
- Scheduled scraping tasks
- Ranking history storage
- Logging system for tracking scraper activity
- Cross-Origin Resource Sharing (CORS) support

---

## Project Structure

### Backend API
Implemented using Flask and Flask-RESTful.

Endpoints include:
- `/sites`
- `/keywords`
- `/run-scraper`
- `/logs`

---

### Web Scraper
The scraper:
- Uses Selenium WebDriver
- Runs Chrome in headless mode
- Searches Google for target keywords
- Detects ranking positions of target domains
- Iterates through multiple search result pages

---

### Database
SQLite is used for storing:
- Keywords
- Domains
- Ranking results
- Logs

SQLAlchemy ORM is also used for database modeling.

---

### Scheduler
A scheduling service automatically runs the scraper daily using the `schedule` library.

---

## Technologies Used

- Python
- Flask
- Flask-RESTful
- SQLAlchemy
- SQLite
- Selenium
- Chrome WebDriver
- Flask-CORS

---

## Author
Mehrsa Dehnavi

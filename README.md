# Automated Ticketing System - Flask Application

## Overview

This project is an **Automated Ticketing System** developed as part of the **Principles of Software Design (PSD)** course. The system is a web-based application built using the Flask framework. It allows users to raise tickets for tasks such as password reset or license downloads, providing an efficient and streamlined workflow for managing requests.

## Features

- **User-friendly Interface**: Simplified UI for raising and tracking tickets.
- **Automation**: Automates repetitive tasks using scripts, such as `automate.py`.
- **Dynamic Workflow**: Processes requests and delivers outputs efficiently.
- **Dockerized Setup**: Ensures portability and ease of deployment.

## Tech Stack

- **Backend**: Flask
- **Frontend**: HTML/CSS, JavaScript (if applicable)
- **Database**: postgresql
- **Containerization**: Docker
- **Language**: Python 3.8

## Prerequisites

- **Python 3.8+** installed on your system.
- **Docker** installed and running.

## Installation

### Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### Install Dependencies

Install required Python packages:

```bash
pip install -r requirements.txt
```

### Run the Application Locally

Start the Flask application:

```bash
python app.py
```

The application will be available at `http://127.0.0.1:8000` by default.

## Docker Setup

### Build the Docker Image

```bash
docker build -t automated-ticketing-system .
```

### Run the Docker Container

```bash
docker run -p 8000:8000 automated-ticketing-system
```

Access the application at `http://localhost:8000`.

## Usage

1. Navigate to the homepage of the application.
2. Submit a new ticket using the available form.
3. Tickets are processed automatically, and results (e.g., certificates or licenses) are generated.
4. Monitor ticket status directly in the app.


## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- Developed as part of the **Principles of Software Design** course.
- Thanks to the instructors and peers for their valuable input.

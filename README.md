 Ticket Booking App (V2)-  BookEase 

A web-based application for booking event tickets, creating shows, theatres and getting infos.

## 🔧 Tech Stack

### Frontend
- [Vue.js](https://vuejs.org/)
- Vue Router, Axios
- Tailwind CSS (optional)

### Backend
- [Flask](https://flask.palletsprojects.com/)
- Celery + Redis (for async task management)
- SQLite or PostgreSQL
- Jinja2 templates

---

## Table of Contents

- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [Setting up Redis Server](#setting-up-redis-for-backend-jobs)
- [Setting up Celery worker and Beat](#setting-up-celery-worker-and-beats)
- [Usage](#usage)
- [Features](#features)
- [To Do](#to-do)
- [License](#license)



## Getting Started

1. Navigate into the Project Folder, called vue-project after decompressing the zip file.

## Prerequisites

1. Python 3.X installed
2. All the backend requirements are present in requirements.txt and installed in the env1.
3. Ensure that the Interpreter is properly selected as the that of the virtual environment.([Steps to execute virtual environment](#backend-setup))
4. Frontend prerequisites-
  - Install Node.js
  - Install vue-cli 
``` sh 
npm install -g @vue/cli
```
5. The application backend uses Redis as a message broker for Celery tasks. Install Redis.[To run redis server](#setting-up-redis-for-backend-jobs)

6. For PDF reports (Monthly entertainment reports).we also need the wkhtmltopdf but it can be skipped.



## Backend Setup
1. Navigate into the 'app-backend' folder and  with the following command.
```sh 
cd app-backend 
```
2. Now to setup the virtual environment.run these commands to activate the virtual environment called 'env1'
```sh 
python3 -m venv env1
source env1/Scripts/activate
pip install -r requirements.txt
```
3. This activates the virtual environment containing all the dependencies.
4. Now to run the Python flask application. Run the following coomand.
```sh 
python app.py
```

## Frontend Setup

1. Open a new termina, Now Navigate into the 'app-frontend' folder for running the vue-js app.
```sh
cd app-frontend
```

2. After navigating to the directory there is a package.json file , run the following command to install all dependencies.
```sh
npm install
```
3. Now to run the vue js app, Named BOOKEASE. run the following command.

```sh 
npm run serve
```
3. This runs the application on localhost- port 8080


## Setting up Redis for Backend Jobs 

1. Install redis on the system.
2. Open a new Terminal and run the following command to run a redis server for backend jobs.
```sh
redis-server
```
3. This runs a redis server in backend and is ready to accept jobs.

## Setting Up Celery Worker and Beats 

1. Open a new terminal ,Activate the Virtual environment (env1) and run the following command to run the celery worker.

```sh 
celery -A app.client worker -l info -P solo
```

2. Open another terminal , activate the virtual Environment and run the following command to run a beat for scheduled tasks.

```sh
celery -A app.client beat -l info
```

## Usage 
1. The Application is up and running on the localhost-port 8080 for the usage of the user.

2. For Admin Access the Admin username and password are setup as a configuration variable and can be found on the following path.
3. > App-backend -> instance -> config.py 

4. For other users, the user function can be used.


## Features


- 🎟️ Real-time seat booking
- 📅 Admin panel for show scheduling
- 🔔 Email/notification system with Celery
- 🗃️ Import/export data via CSV
- 🌐 Clean, responsive UI

## To Do 


 - Add payment gateway integration

 - Implement user authentication

 - Add unit tests and CI workflow

 - Review Sentiment Analysis


 ## License 

 MIT License © Akriti Vishwas









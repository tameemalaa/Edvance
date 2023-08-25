# Edvance LMS

The Edvance LMS project aims to develop an open-source Learning Management System (LMS) platform that goes beyond being a storage solution. It focuses on enhancing learning and teaching experiences by automating time taking tasks for teachers and students. 
## Table of Contents

- [Edvance LMS](#edvance-lms)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
      - [Docker (Recommended)](#docker-recommended)
      - [Manually](#manually)
        - [For Backend(Server):](#for-backendserver)
        - [For frontend(Client):](#for-frontendclient)
  - [Features](#features)
    - [In-progress](#in-progress)
    - [**Planned Features:**](#planned-features)
  - [Feedback and Suggestions](#feedback-and-suggestions)
## Getting Started

A production app isn't yet ready , to run the development applicatoin follow the steps below.

### Prerequisites
  - Clone the repository 
    ```bash 
    git clone https://github.com/tameemalaa/Edvance.git
    ```
   
  - create `.env` file at `/server` and paste the following.
    ```
    SECRET_KEY = "django-insecure-un6mxt#85eik$l95pynw)4gb-vlp4f37cg*i($)oag*8(bxht$"
    DEBUG = True
    DB_ENGINE = 'django.db.backends.postgresql_psycopg2'
    DB_NAME = 'iwyquqkm'
    DB_USER = 'iwyquqkm'
    DB_PASSWORD = 'rE_x6jx0nJbCUBnXbOk3Bcby-M0bkAgc'
    DB_HOST = 'trumpet.db.elephantsql.com' 
    DB_PORT = '5432'
    DB_API_KEY ='a646d1b0-29dd-41db-9bbd-78cf5d24c13e'
    EMAIL_HOST_USER = "gproj1566@gmail.com"
    EMAIL_HOST_PASSWORD = "lrrrhdinrzzyzaxx"
    DOMAIN = "localhost:8080"
    ```
### Installation 

Proceed in one of the following ways : 

#### Docker (Recommended)
- Have docker and docker-compose installed , a simple guide can be found on the [docker website](https://docs.docker.com/engine/install/)
- Build the images 
 - `docker build --file ./server/Dockerfile.dev --tag backend:dev ./server` 
 - `docker build --file ./client/Dockerfile.dev --tag backend:dev ./client` 
 - Run the images 
   - `docker-compose --file dev-docker-compose.yml up`

#### Manually
##### For Backend(Server):
- Have python > 3.10  installed 
- create a virtual enviroment and activate it based on OS , refere [here](https://docs.python.org/3/library/venv.html)
- install dependecies 
  - `pip install -r requirements.txt` 
- run the dev server  
  - `python ./server/manage.py runserver` 

##### For frontend(Client):
- Have node installed 
- navigate to `/client`
- install dependencies 
  - `npm install` 
- run 
  - `npm run server`

## Features
The Project is still in early development , below are the inprogress and yet to be impleemnted features 
### In-progress
- [x] **User Management System:**
- [x] **Automated attendance Tracking**
- [x] **Courses Management**
- [ ] **courses Materials Repository**
- [ ] **Assignments**
### **Planned Features:**

- [ ] **Posts**
- [ ] **Comments**
- [ ] **TODO Tracking**
- [ ] **Tracking Grades**
- [ ] **Notifications**
- [ ] **Online Quizzes**
- [ ] **Automated Exam Creation**
- [ ] **Performance Tracking (Dashboard)**
    - [ ] Teacher Dashboard
    - [ ] Student Dashboard
- [ ] **Automated Grading**
- [ ] **Communication Channel (Chat)**
- [ ] **Student Toolbox**
    - [ ] Calculator
    - [ ] Cloud Integrated Development Environment (IDE)
    - [ ] Time Tracker


## Feedback and Suggestions

We welcome your feedback and suggestions for features you'd like to see. Please open an issue or reach out to us via email.

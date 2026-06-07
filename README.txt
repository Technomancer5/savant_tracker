# Overview

Savant Tracker is a specialized full-stack project tracking web-app to help users not only log time for various projects 
but also easily switch between them or pick up where they left off.
My primary goal with this project was to enhance my understanding of full-stack web architechtures and develop a way to 
more effeciently track my projects as well as having a better asthetic than simple excel sheets.

### How to Start the Test Server
To spin up the development environment and view the application locally, follow these steps:
1. Open your terminal and navigate to the project repository root:
    ```bash
    cd ~/Git/savant_tracker
2. Activate your Python virtual environment:
    source .venv/bin/activate
3. Boot up the Django integrated web server:
    python manage.py runserver
4. Launch your web browser and open the following address to see the home page:
    [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

[Savant Tracker Web App Walkthrough](https://youtu.be/k0KFO_AbvcU)

# Web Pages
Page 1: The main dashboard to view projects and upload or download an excel sheet.
It has a dynamic project count, has buttons to sync exel sheets and displays basic project information as well as a 
button to the edit page for each project.
Page 2: Displays project details and allows for editing or deleting the project.  It also contains a session history 
log as well.

# Development Environment
For development I used VS Code, GitHub, SQLite 3 and Fish/Bash terminal shells.

I used Python v3.14, Django Web Framework, Pandas, openpyxl and Bootstrap v5.3.

# Useful Websites
* [Django Project Documentation](https://docs.djangoproject.com/en/6.0/)
* [Gemini](http://gemini.google.com)

# Future Work
* Item 1: Multi-User Authentication Shielding: Integrate Django's built-in cryptographic auth middleware 
(django.contrib.auth) to support account sign-ups, protecting personal project tracking sheets with private 
profiles.
* Item 2: I will be hosting this on my server in the near future and need to see if I need to make any adjustments.
* Item 3: I would like to add my own database on my server or use a cloud database.
* Item 4: Research adding everything to my Savant Educator domain as a child page.

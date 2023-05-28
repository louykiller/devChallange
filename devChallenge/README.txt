Prerequisites:
- Have Docker installed and running

Setup and run the program (might take a while to download everything):
- docker-compose run web python manage.py migrate
- docker compose up
- Enter this link on your browser of choice: http://127.0.0.1:8000
- Enjoy!


Dev Challenge from RedLight
Welcome to my implementation of a web platform to manage internship applications in a company.
The aim of this challenge was to build a simple web platform that helps to manage different role submissions for that company.

These were the goals for this platform:
- Create new applicants
- List existing applicants
- Show an existing applicant
- Update existing applicants
- Delete an existing applicant
- Search for applicants
- Create new roles
- List existing roles
- Show an existing role
- Update existing roles
- Delete an existing role
- Search for roles
- Change the applicant status on a given role


Frontend
For the frontend (not my biggest strength) I used plain HTML and CSS with Bootstrap and jQuery

Backend
For the backend I used Django, the high-level Python web framework with the SQLite database while developing the application but switched to PostgreSQL for the final incorporation with Docker

Main Database Objects
- Applicant
    Name - Text
    Phone Number - Text
    Email - Text
- Role
    Name - Text
- Applicant Role
    Applicant - Foreign Key
    Role - Foreign Key
    Status - Enum (Approved, Rejected or Under analysis)

Extras
I validated that the backend and frontend only receives the parameters it needs, no more, no less.
For example when adding a new role to a user (or vice-versa) it only allows remaining options instead of all options.
I created validations for the form fields, for example for the phone number it only accepts portuguese numbers (9 digits).
I also added clear messages for every action the user makes.

Code Structure:
- Inside the applicantManager folder I have the models, urls and views for this project.
- The settings of this project are in the devChallenge folder.
- Finally in the templates folder are all of the html files for the web application.


PS - I tried to fork the GitLab repository and upload all the files there but it doesn't let me do that due to some security issues
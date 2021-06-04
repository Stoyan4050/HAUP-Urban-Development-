# HAUP Urban Development

## Table of Contents

* [General Information](#general-information)
* [Key Features](#key-features)
* [Technologies](#technologies)
* [Setup](#setup)
* [Launch](#launch)
* [Usage](#usage)
* [Team](#team)
* [Contributions](#contributions)

## General Information

HAUP Urban Development is a web application that uses semi-supervised machine learning to detect greenery on historical maps of the Netherlands, in order to analyze the changes in urban development over the years.

## Key Features

- Recognizes greenery in maps of the Netherlands
- Supports maps from different years (all the way back to 1815)
<!--- - Saves your manual classifications for future use --->
- Displays a textual representation of the most important information for maps of different years
<!--- - Can export the most important information for maps of different years in a CSV formatted file for offline use --->

## Technologies

The project HAUP Urban Development uses the following technologies:
- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- HTML5
- CSS5
- [JavaScript](https://www.javascript.com/)
- [jQuery](https://jquery.com/)

## Setup

In order to set the project up, follow the steps below:
```sh
# Clone the repository to your local machine
git clone https://gitlab.ewi.tudelft.nl/cse2000-software-project/2020-2021-q4/cluster-09/haup-historic-development/haup-historic-development.git

# Go into the repository's root folder
cd haup-historic-development

# Install the requirements
pip install -r requirements.txt
```

## Launch

In order to launch the project, go to the root directory of the project and follow the steps below:
```sh
# Go into the src folder
cd src

# Run the web application
python manage.py runserver
```
You can now access the web application using a web browser of your choice at the following link:
[https://localhost:8000](https://localhost:8000)

## Usage

#### Login Page

Initially, upon entering the website, users are redirected to the login page. From there users can log in either with their account, if they have one, or as a guest. Moreover, from the login page user can go to the Registration Page, in order to create a new account, or to the Change Password Page, in order to change the password associated with their account.

#### Registration Page

When creating an account, users have to provide their email address and a password, which they also have to confirm. This creates a new account, which is temporarily inactive, and sends an activation email to the email address entered by the user. The email contains an activation link, which is only valid for 10 minutes, after the time of sending the email. If the activation link in the email is still valid, when the user goes to it, their account gets activated and they can log in with their email address and password from the Login Page.

#### Change Password Page

In order to change their password, users must provide the email address associated with their account. Then, they receive an email with a link, which is only valid for 10 minutes, after the time of sending the email. If the link in the email is still valid, when the user goes to it, they get redirected to another page, where they have to enter and confirm their new password. After that, the password associated with the user's account is changed and they can log in with their email address and their new password from the Login Page.

#### Map Page

After logging in with their account or as a guest, users are redirected to the Map Page, which shows the map for the currently selected year (by default, the most recent available year is selected). From the menu bar at the top of the page users can switch between the Map Page and the Data Page. Moreover, they can select the year, which they want to view the map of, as well as add an overlay to the map of the currently selected year. The following overlays are available:
- The 'Classified as' overlay provides information on what different map tiles have been classified as:
  - Map tiles colored in green have been classified as containing greenery;
  - Map tiles colored in red have been classified as not containing greenery.
- The 'Classified by' overlay gives information on who provided the classifications for different map tiles:
  - Map tiles colored in magenta have been classified by the training data used by our machine learning algorithm;
  - Map tiles colored in yellow have been classified by a user;
  - Map tiles colored in cyan have been classified by our machine learning algorithm.

#### Data Page

When users go to the Data Page, they are shown a fairly simple textual representation of the most important information for the map of the currently selected year. From the menu bar at the top of the page users can select the year, the map of which they want to view the information for. The displayed information includes:
- The total number of map tiles of the selected year, which have been classified;
- The number/percentage of map tiles of the selected year classified as containing greenery;
- The number/percentage of map tiles of the selected year classified as not containing greenery;
- The number/percentage of map tiles of the selected year classified by the training data used by our machine learning algorithm; 
- The number/percentage of map tiles of the selected year classified by a user;
- The number/percentage of map tiles of the selected year classified by our machine learning algorithm.

## Team

Angel Karchev - ank1972@abv.bg\
Ivan Nestorov - ivan.nestorov1401@gmail.com\
Ivan Todorov - ivan.s.t@icloud.com\
Liselotte Jongejans - liselottejongejans@gmail.com\
Stoyan Dimitrov - s.g.dimitrov@student.tudelft.nl

## Contributions

All help is always welcome. However, before making changes, please open an issue to discuss your ideas.

NOTE: In order to reduce the load on the server, please make sure that both [Pylint](https://www.pylint.org/) and [Flake8](https://flake8.pycqa.org/en/latest/) pass with no warnings and that all tests pass, before pushing your changes. Instructions on how to run the aforementioned static code analysis tools and the tests can be found below.

#### [Pylint](https://www.pylint.org/)

In order to run [Pylint](https://www.pylint.org/), go to the root directory of the project and run the following commands:
```sh
pylint -d E0633 src/api/*.py
pylint -d E0633 src/classification/*.py
pylint -d E0633 src/urban_development/*.py
pylint -d E0633 src/utils/*.py
```

#### [Flake8](https://flake8.pycqa.org/en/latest/)

In order to run [Flake8](https://flake8.pycqa.org/en/latest/), go to the root directory of the project and run the following commands:
```sh
flake8 --max-line-length=120 src/api/*.py
flake8 --max-line-length=120 src/classification/*.py
flake8 --max-line-length=120 src/urban_development/*.py
flake8 --max-line-length=120 src/utils/*.py
```

#### Unit Tests

In order to run the unit tests, go to the root directory of the project and follow the steps below:
```sh
# Go into the src folder
cd src

# Run the unit tests
python manage.py test
```

NOTE: To measure the code coverage of the current test suite, the project HAUP Urban Development uses [Coverage.py](https://coverage.readthedocs.io/en/coverage-5.5/). In order to run [Coverage.py](https://coverage.readthedocs.io/en/coverage-5.5/) and view the test coverage report generated by it, go to the root directory of the project and follow the steps below:
```sh
# Go into the src folder
cd src

# Run Coverage.py
coverage run manage.py test

# Generate the test coverage report as an HTML page
coverage html

# Go into the htmlcov folder
cd htmlcov

# Open the index.html file
index.html
```

#### UI Integration Tests

NOTE: For running the UI integration tests, chromedriver needs to be installed. In order to install chromedriver, go to the folder on your local machine, where Python is installed, and add [chromedriver.exe](https://chromedriver.chromium.org/downloads) to the Scripts folder.

In order to run the UI integration tests, launch the project using the instuctions in the [Launch](#launch) section, then, while the project is launched, go to the the root directory of the project and follow the steps below:
```sh
# Go into the integration_tests folder
cd src/api/integration_tests

# Run the integration tests
python ui_integration_tests.py
```

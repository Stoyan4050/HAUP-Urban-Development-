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

- Recognizes greenery on historical maps of the Netherlands.
- Supports maps from different years (all the way back to 1815).
- Displays a textual representation of the most important information about the maps.
- Registered users can classify map tiles either manually or using the integrated machine learning algorithm.

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

# Go into the root directory of the project
cd haup-historic-development

# Install the requirements
pip install -r requirements.txt
```

## Launch

In order to launch the project, go into the root directory of the project and follow the steps below:
```sh
# Go into the src folder
cd src

# Run the web application
python manage.py runserver
```
You can now access the web application using a web browser of your choice at the following link: [https://localhost:8000](https://localhost:8000)

## Usage

#### Login Page

Initially, upon entering the website, users are redirected to the [Login Page](#login-page). From there users can log in either with their account, if they have one, or as a guest. Moreover, from the [Login Page](#login-page) users can go to the [Registration Page](#registration-page), in order to create a new account, or to the [Change Password Page](#change-password-page), in order to change the password associated with their account.

#### Registration Page

When creating an account, users have to provide their email address and a password, which they also have to confirm. This creates a new account, which is temporarily inactive, and sends an activation email to the email address entered by the user. The email contains an activation link, which is only valid for 10 minutes, after the time of sending the email. If the activation link in the email is still valid, when the user goes to it, their account gets activated and they can log in with their email address and password from the [Login Page](#login-page).

#### Change Password Page

In order to change their password, users must provide the email address associated with their account. Then, they receive an email with a link, which is only valid for 10 minutes, after the time of sending the email. If the link in the email is still valid, when the user goes to it, they get redirected to another page, where they have to enter and confirm their new password. After that, the password associated with the user's account is changed and they can log in with their email address and their new password from the [Login Page](#login-page).

#### Map Page

After logging in with their account or as a guest, users are redirected to the [Map Page](#map-page), which shows the map of the currently selected year (by default, the most recent available year is selected). From the menu bar at the top of the page users can switch between the [How to Use Page](#how-to-use-page), the [Map Page](#map-page) and the [Data Page](#data-page). Moreover, they can select the year, which they want to view the map of, as well as add an overlay to the map of the currently selected year. The following overlays are available:
- The 'Classified as' overlay provides information on what different map tiles have been classified as:
  - Map tiles colored in green have been classified as containing greenery;
    - Map tiles colored in low-opacity green have been classified as containing low amount of greenery;
    - Map tiles colored in medium-opacity green have been classified as containing medium amount of greenery;
    - Map tiles colored in high-opacity green have been classified as containing high amount of greenery;
  - Map tiles colored in red have been classified as not containing greenery.
- The 'Classified by' overlay gives information on who provided the classifications for different map tiles:
  - Map tiles colored in cyan have been classified by a user;
  - Map tiles colored in magenta have been classified by the integrated machine learning algorithm;
  - Map tiles colored in yellow have been classified by the training data used by the integrated machine learning algorithm.

Additionally, if users are only interested in one particular province of the Netherlands, they can select it, after choosing one of the two overlays, described above.

#### Data Page

When users go to the [Data Page](#data-page), they are shown a fairly simple textual representation of the most important information for the map of the currently selected year. From the menu bar at the top of the page users can select the year, the map of which they want to view the information for. The displayed information includes:
- The total number of map tiles of the selected year, which have been classified;
- The number/percentage of map tiles of the selected year classified as not containing greenery;
- The number/percentage of map tiles of the selected year classified as containing greenery;
- The number/percentage of map tiles of the selected year classified as containing low amount of greenery;
- The number/percentage of map tiles of the selected year classified as containing medium amount of greenery;
- The number/percentage of map tiles of the selected year classified as containing high amount of greenery; 
- The number/percentage of map tiles of the selected year classified by a user;
- The number/percentage of map tiles of the selected year classified by the integrated machine learning algorithm;
- The number/percentage of map tiles of the selected year classified by the training data used by the integrated machine learning algorithm.

#### How to Use Page

The [How to Use Page](#how-to-use-page) provides step-by-step instructions for new users on how to use the [key features](#key-features) of the web application.

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

In order to run [Pylint](https://www.pylint.org/), go into the root directory of the project and run the following command:
```sh
pylint src
```

#### [Flake8](https://flake8.pycqa.org/en/latest/)

In order to run [Flake8](https://flake8.pycqa.org/en/latest/), go into the root directory of the project and run the following command:
```sh
flake8 src
```

#### Unit Tests

In order to run the unit tests, go into the root directory of the project and follow the steps below:
```sh
# Go into the src folder
cd src

# Run the unit tests
python manage.py test api
```

NOTE: To measure the code coverage of the current test suite, the project HAUP Urban Development uses [Coverage.py](https://coverage.readthedocs.io/en/coverage-5.5/). In order to run [Coverage.py](https://coverage.readthedocs.io/en/coverage-5.5/) and view the test coverage report generated by it, go into the root directory of the project and follow the steps below:
```sh
# Go into the src folder
cd src

# Run Coverage.py
coverage run manage.py test api

# Generate the test coverage report as an HTML page
coverage html

# Go into the htmlcov folder
cd htmlcov

# Open the index.html file
index.html
```

#### UI Integration Tests

NOTE: For running the UI integration tests, chromedriver needs to be installed. In order to install chromedriver, go into the folder on your local machine, where Python is installed, and add [chromedriver.exe](https://chromedriver.chromium.org/downloads) to the Scripts folder.

In order to run the UI integration tests, launch the project using the instuctions in the [Launch](#launch) section, then, while the project is launched, go into the root directory of the project and follow the steps below:
```sh
# Go into the integration_tests folder
cd src/integration_tests

# Run the integration tests
python ui_integration_tests.py
```

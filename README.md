# HAUP Urban Development

## Table of Contents
* [Introduction](##introduction)
* [Key Features](#key-features)
* [Technologies](#technologies)
* [Setup](#setup)
* [Contributions](#contributions)

## Introduction

HAUP Urban Development is an application that uses semi-supervised machine learning to detect greenery on historical maps of the Netherlands, in order to analyze the changes in urban development over the years.

## Key Features

- Recognize greenery in maps of the Netherlands
- Supports maps from different years (all the way back to 1815)
- Log in with your account, and save your personal classifications for future use
- View a textual representation of the most important statistical data for maps of different years
<!--- - Export the most important statistical data for maps of different years in a CSV formatted file for offline use --->

## Technologies

HAUP Urban Development uses the following technologies:

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- HTML5
- CSS5
- [JavaScript](https://www.javascript.com/)
- [jQuery](https://jquery.com/)

## Setup

To setup the project follow the steps below:
```sh
# Clone the repository
git clone https://gitlab.ewi.tudelft.nl/cse2000-software-project/2020-2021-q4/cluster-09/haup-historic-development/haup-historic-development.git

# Go into the repository
cd haup-historic-development

# Install requirements
pip install -r requirements.txt

# Go into the src folder
cd src

# Run the app
python manage.py runserver
```
You can now access the app at:
[https://localhost:8000](https://localhost:8000)

NOTE: For running the UI integration tests, chromedriver needs to be installed. Go to the folder where Python is installed on your computer. In the Scripts folder add [chromedriver.exe](https://chromedriver.chromium.org/downloads).

## Usage

#### To View Greenery on Maps
After logging in with your account or as a guest, you will be redirected to the map page. In the menu bar at the top, select the year of map and the type of classification you want to view. 'Classified as' provides a overlay on the map with the different types of classifications. 'Classified by' provides an overlay depending on who determined the classification. Default is the classification by the classifier algorithm of the tool.

#### To View Important Statistical Data
In the menu bar at the top, select 'Data View'. In the menu bar at the top, select the year of the map for which you want to view (statistical) data. You will then see statistics regarding the percentages of the map classified as a certain label, as well as statistics concerning what or who classified (sections of) the map.

## Contributions

All help is always welcome. However, before making changes, please open an issue to discuss your suggested changes.

Make sure to run [Flake8](https://flake8.pycqa.org/en/latest/) and [Pylint](https://www.pylint.org/) and that all tests pass, before pushing your changes, to reduce the load onto the server.
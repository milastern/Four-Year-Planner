# William & Mary Four-Year Plan Generator

## Overview

The **William & Mary Four-Year Plan Generator** is a web application built with **Dash**, designed to help students create personalized four-year academic plans based on their major, minor, language preferences, study-abroad options, and academic credits. This tool is highly customizable to accommodate different degree types such as single major, double major, or major with a minor. The generated plan includes a chart that visually represents the student's course schedule for the chosen degree path.

## Features

- **Select Primary Major**: Choose a primary major from a list of available options.
- **Credits Input**: Enter the number of credits already earned.
- **Language Preference**: Select a language for the foreign language proficiency and for international relations majors.
- **Study Abroad Options**: Indicate if the student plans to study abroad during their academic career.
- **Degree Type**: Choose from single major, double major, or major-minor configurations.
- **Dynamic Field Visibility**: Depending on the selected degree type, the app will show or hide additional fields like secondary major and minor selections.
- **Personalized Four-Year Plan**: Upon submitting the form, the app generates a course schedule and displays it as an image.

## Installation Instructions

To get started with the William & Mary Four-Year Plan Generator, follow these steps:

### 1. Install Dependencies

Clone this repository to your local machine:

```bash
git clone https://github.com/your-username/four-year-plan-generator.git
cd four-year-plan-generator
```
Create and activate a virtual environment. If you use uv, it's as simple as:

```bash
uv venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
```
Then, install the project dependencies using the pyproject.toml file:

```bash
uv pip install -e .
```

This will install all the necessary libraries, including Dash, matplotlib, and others that are used in the app.

# 2. Data Setup

Ensure that the required data files are in place:

- **majors_list.npy**: A list of available majors.
- **minors_list.npy**: A list of available minors.
- **majors.npy**: A dictionary of the major requirements for the avalible majors 
- **minors.npy**: A dictionary of the minor requirements for the avalible minors
-**course_catalog.npy**: A list of information on all avalable courses


These files should be placed in a folder named `data` in the root of the project directory. You can create sample data in the format shown in the example files if they do not exist.

# 3. Running the Application

After installing the dependencies and setting up the data, you can run the application:

```python
python main.py 
```

This will start the Dash server and you can access the app by opening your browser and navigating to [http://127.0.0.1:8050/](http://127.0.0.1:8050/).

# Using the Application

- **Open the app**: When the app is running, open your browser and go to the local server URL: [http://127.0.0.1:8050/](http://127.0.0.1:8050/).
- **Enter Your Information**: Fill out the form with the following details:
- **Submit the Form**: Once you have filled in the form, click the "Submit" button to generate your four-year plan.
- **View the Plan**: After submitting, a personalized course schedule will appear as a visual chart representing your four-year plan.

# Code Structure

The code structure of this project is organized to separate concerns, making it modular and easy to understand. Each component of the program is designed for a specific role, from user interaction to schedule generation and data handling.

## 1. **main.py**
   - **Role**: This is the main entry point for the application and the file that runs the Dash server. It is responsible for setting up the web server and managing dynamic interactions between user inputs and the course scheduling logic.
   - **Key Features**:
     - **Callback Logic**: Defines the logic for interacting with user inputs. It reacts to user selections, such as primary major, secondary major, credits earned, study abroad preferences, etc., and triggers the appropriate updates to the UI or processing logic.
     - **Dynamic Form Behavior**: Based on the selected degree type (e.g., single major, double major, or major-minor combination), the form dynamically adjusts which fields are visible or hidden. This is done using Dash's `Input` and `Output` objects.
     - **Form Submission**: Once the user fills out the form and clicks "Submit," the inputs are processed to generate a personalized academic schedule, which is then visualized as a chart.

## 2. **src/ui_program.py**
   - **Role**: Contains the configuration for the Dash application, including layout and UI components.
   - **Key Features**:
     - **Dash Layout**: This file defines the structure of the user interface using Dash components (`html.Div`, `dcc.Dropdown`, `dcc.Input`, etc.). The layout consists of various sections, such as the introduction, input fields for user data, and dynamic display components.
     - **User Inputs**: The UI includes fields for selecting a primary major, entering credits, selecting a language, and determining study abroad preferences. These fields guide the user through creating a personalized four-year plan.
     - **Style and Appearance**: Basic styling, such as borders, padding, and margins, is applied to create a clean and user-friendly experience. You can further customize the appearance with additional CSS or themes like `dash_bootstrap_components`.

## 3. **src/get_courses.py**
   - **Role**: Contains the `MakeASchedule` class, which performs all core scheduling logic based on user input.
    - **Overview of `MakeASchedule` Methods**:
    - `clean_course_data(self)`: Prepares and cleans course data before scheduling.
    - `get_unmet_prereqs(self)`: Identifies which prerequisite courses are still required for a given course.
    - `add_course(self, course)`: Adds a single course to the schedule.
    - `get_minor_courses(self)`: Retrieves required courses for the selected minor.
    - `get_major_classes(self)`: Retrieves required courses for the selected major(s).
    - `add_coll_classes(self)`: Adds general COLL classes to the schedule.
    - `add_abroad(self)`: Inserts study abroad semesters and adjusts scheduling accordingly.
    - `add_any_electives(self)`: Fills remaining credit requirements with elective courses.
    - `compile(self)`: Compiles the entire course list across semesters into a unified format.
    - `sort_schedule(self)`: Orders courses chronologically and logically across the four years.
    - `make_schedule(self)`: Generates the full semester-by-semester schedule in dictionary form.
    - `make_chart(self, output: str = None)`: Generates a chart for visualizing the schedule.

    - **Key Concept**: This class allows encapsulated logic for generating and validating course schedules.
   

## 4. **data/**
   - **Role**: The `data` folder contains the files that provide the foundation for the app's dynamic inputs. These files store lists of majors, minors, and other academic options, which the app uses to populate dropdowns and validate user choices.
   - **Files**:
     - **`majors_list.npy`**: A NumPy file containing a list of available majors at the institution. The app reads this list to populate the dropdown for selecting a primary or secondary major.
     - **`majors.npy`**: A NumPy file containing a list of all available majors at the institution and their requirements. This is used for creating cirriculums for primary and secondary majors 
     - **`minors_list.npy`**: A NumPy file containing a list of available minors at the institution. It is used to populate the minor dropdown if the user selects a major-minor degree type.
     - **`minors.npy`**: A NumPy file containing a list of all available minors at the institution and their requirements. This is used for creating cirriculums for minors
   - **Customization**: You can easily customize these files to reflect the specific majors, minors, and academic options offered by your institution. Modify the `.npy` files as needed, or replace them with other data formats that your application can parse.

   ## 5. **data_prep/**
- `course_catalog.py`:
  - **Purpose**: Web scraper that extracts course data from the William & Mary online course catalog.
  - **Output**: Provides structured data used by `get_courses.py`.
- `majors_n_minors.py`:
  - **Purpose**: Stores hardcoded requirement dictionaries for the 10 most popular William & Mary majors and minors.
  - **Use**: Referenced by `MakeASchedule` to determine required classes.

  ## 6 **assets/**
- Stores static assets for the Dash app.
- **Notably includes** the PNG output of the user’s generated four-year schedule.
- Automatically overwritten with each new schedule generation.


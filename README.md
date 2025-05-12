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
Then, install the required Python packages using pip:

```bash
pip install -r requirements.txt

``` 


This will install all the necessary libraries, including Dash, Plotly, and others that are used in the app.

# 2. Data Setup

Ensure that the required data files are in place:

- **majors_list.npy**: A list of available majors.
- **minors_list.npy**: A list of available minors.

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
  - **Primary Major**: Select your primary major from the dropdown list.
  - **Number of Credits Already Earned**: Enter the total credits you have earned so far.
  - **Language**: If applicable, select a language from the dropdown.
  - **Study Abroad Preference**: Select whether you are planning to study abroad.
  - **Degree Type**: Choose whether you are pursuing a single major, double major, or a major-minor combination.
  - **Secondary Major/Minor**: Depending on your degree type, these options will appear dynamically.
- **Submit the Form**: Once you have filled in the form, click the "Submit" button to generate your four-year plan.
- **View the Plan**: After submitting, a personalized course schedule will appear as a visual chart representing your four-year plan.

# Code Structure

The code structure of this project is organized to separate concerns, making it modular and easy to understand. Each component of the system is designed for a specific role, from user interaction to schedule generation and data handling.

## 1. **main.py**
   - **Role**: This is the main entry point for the application and the file that runs the Dash server. It is responsible for setting up the web server and managing dynamic interactions between user inputs and the course scheduling logic.
   - **Key Features**:
     - **Callback Logic**: Defines the logic for interacting with user inputs. It reacts to user selections, such as primary major, secondary major, credits earned, study abroad preferences, etc., and triggers the appropriate updates to the UI or processing logic.
     - **Dynamic Form Behavior**: Based on the selected degree type (e.g., single major, double major, or major-minor combination), the form dynamically adjusts which fields are visible or hidden. This is done using Dash's `Input` and `Output` objects.
     - **Form Submission**: Once the user fills out the form and clicks "Submit," the inputs are processed to generate a personalized academic schedule, which is then visualized as a chart.

## 2. **app.py**
   - **Role**: Contains the configuration for the Dash application, including layout and UI components.
   - **Key Features**:
     - **Dash Layout**: This file defines the structure of the user interface using Dash components (`html.Div`, `dcc.Dropdown`, `dcc.Input`, etc.). The layout consists of various sections, such as the introduction, input fields for user data, and dynamic display components.
     - **User Inputs**: The UI includes fields for selecting a primary major, entering credits, selecting a language, and determining study abroad preferences. These fields guide the user through creating a personalized four-year plan.
     - **Style and Appearance**: Basic styling, such as borders, padding, and margins, is applied to create a clean and user-friendly experience. You can further customize the appearance with additional CSS or themes like `dash_bootstrap_components`.

## 3. **src/get_courses.py**
   - **Role**: This file contains the business logic that processes user inputs and generates the academic schedule. It defines the `make_a_schedule` function, which is responsible for scheduling courses based on user preferences and degree requirements.
   - **Key Features**:
     - **`make_a_schedule` Function**: This is the core function that takes in the user's selections (primary major, secondary major/minor, language, study abroad preferences, and credits) and generates a customized academic plan. 
     - **Schedule Generation**: The function may involve creating course lists, calculating semesters, and ensuring that all necessary courses for the selected degree program are included. You can modify this function to adjust the logic for selecting and sequencing courses, according to specific institutional requirements.
     - **Chart Creation**: After generating the schedule, the function creates a visual representation of the course plan (usually in a chart format). This chart is then displayed to the user in the app.

## 4. **data/**
   - **Role**: The `data` folder contains the files that provide the foundation for the app's dynamic inputs. These files store lists of majors, minors, and other academic options, which the app uses to populate dropdowns and validate user choices.
   - **Files**:
     - **`majors_list.npy`**: A NumPy file containing a list of available majors at the institution. The app reads this list to populate the dropdown for selecting a primary or secondary major.
     - **`minors_list.npy`**: A NumPy file containing a list of available minors at the institution. It is used to populate the minor dropdown if the user selects a major-minor degree type.
   - **Customization**: You can easily customize these files to reflect the specific majors, minors, and academic options offered by your institution. Modify the `.npy` files as needed, or replace them with other data formats that your application can parse.

# Workflow

The workflow of the app is designed to automate the process of generating a personalized four-year academic schedule for students. Here's how it works:

## 1. **User Interaction (Frontend)**
   - The user interacts with the application through a dynamic web interface built with Dash. The user is prompted to provide essential academic information:
     - Primary major selection
     - Number of credits earned
     - Language preference (if applicable)
     - Study abroad preference
     - Degree type (single major, double major, or major-minor combination)
   - Based on the user's degree type, the relevant fields (e.g., secondary major or minor) are displayed dynamically using callback functions.

## 2. **Form Submission and Validation**
   - After completing the form, the user clicks the "Submit" button. This triggers a series of validations:
     - Ensure that a primary major is selected.
     - Ensure that a language is selected if needed (e.g., for International Relations majors).
     - Ensure that all required fields are filled out.

## 3. **Schedule Generation (Backend)**
   - Once the form is submitted and validated, the backend logic (in `src/get_courses.py`) takes over:
     - The `make_a_schedule` function uses the input data to generate a four-year academic plan.
     - This includes determining which courses are required for the selected major and minor, considering any prerequisites, and sequencing them across semesters.
     - The function calculates whether study abroad fits within the student's timeline and incorporates any study-abroad requirements.
     - The output is a visual chart showing the four-year schedule, with each semester's courses plotted.

## 4. **Visualization (Frontend)**
   - The generated schedule is displayed as a chart on the frontend using Plotly, and the user sees their personalized course plan.
   - This step allows students to visualize their academic journey, helping them make informed decisions about their degree progression.

## 5. **Customization and Adaptability**
   - **Adding New Majors or Minors**: By modifying the `majors_list.npy` and `minors_list.npy` files, you can easily add new academic options. This ensures the app remains adaptable to the changing curriculum of your institution.
   - **Adjusting Degree Requirements**: The logic for how courses are selected and sequenced is housed in `src/get_courses.py`. You can modify the rules and flow to reflect the degree requirements specific to your institution.
   - **Styling and Layout**: The app's visual appearance and layout can be customized to better match your institution's branding or user preferences, either by modifying Dash components or incorporating custom CSS.

This workflow ensures that students can generate an efficient and personalized four-year academic plan while allowing administrators or developers to customize the app to fit specific institutional needs.
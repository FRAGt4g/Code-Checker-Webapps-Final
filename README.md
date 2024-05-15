# LASACC
LASA_CC (LASA Code Checker) is our Web Design and Applications final project focused on the agile development process. The problem statement that our team was faced with was the deprecation for Replit's Teams for Education system and more specifically their code checking service. In an effort to assist the LASA Computer Science department (faculty and students), LASACC is a program designed to provide quick, accurate, and easy feedback on computer science assignments for teachers and students.

### Description of Features
- Read from a .txt file with simple LASA_CC syntax (outlined and explained below) to build checking requirements for any number of labs/assignments. You can have any number of conditions to meet for any number of different grade percent levels.
- Compile, run, and check java (.java and .class) or c++ (.cpp and .h) projects.
- Automatically and quickly send all results to a google sheet for the teacher to look over and see all the important information about a certain student’s submission.

### Tools Used
- Python
- HTML
- CSS
- JS

#### Libraries used
- Flask (for connecting to the website)
- subprocess (for running terminal level commands)
- gspread (for connecting to google sheets)
- oatuh2client (for connecting to google sheets)
- re (for using Regular expressions for checking requirements)
- json (for translating python variables into JSON format to be used in javascript functions)

## How to start using LASA_CC
###Check System installments
The program is meant to run serverside and therefore this will become obsolete but until then in order for the program to work you must have python and all the aforementioned libraries installed. You must also have GNU compiler and Java VM installed for compiling along with running the C++ and Java files.

###Create a sheet (or disable the service)
If you want to have all submissions write to a Google sheet, you will need to download and include a secret JSON key from Google's Cloud APIs service. Once you have the key and include it into the project, you will need to go into the `GoogleSheetsConnection.py` file and change the value of the global variable `json_file_name` to the filename of your secret key. Next, you will have to create the Google sheet you want to use and share it with the associated email your JSON key is connected to. Now change the value of `google_sheet_name` inside the `GoogleSheetsConnection.py` file to the name of the newly created Google sheet. 

###Start writing labs inside the `conditions.txt` file
NOTE: This file can be renamed, you simply have to change the value of the global variable `lab_requirements_text_file` within `main.py` to the name of the file.
####Basic syntax:
- Lines starting with `Project` are saved for creating new labs. After the `Project` keyword, you will have a set of braces and inside list all the acceptable file types.
    - An example for a lab titled "C++ Only Lab" that only takes C++ and Header files would be: `Project [.cpp, .h]: C++ Only Lab`. Note how you can have spaces in your project names and do not need quotes around the name.
- Lines starting with `@` signify a new grade level within the current project. The syntax to make a new grade level of, say 80%, would be: `@80: ` on its own line. A grade level is a set of requirements and a grade attached to it; if you pass all the requirements of that grade level, you will get at least that many points.
    - You can have as many grade levels within a project as you want
    - All subsequent requirements will be added to that grade level until you state a new grade level or project
- Lines starting with `#` are comments and will be ignored.
- All other lines follow this format: {type of requirement} + ": " + {string value for that type of requirement}. This may sound complicated, but really it's pretty simple. There are only 4 types of requirements: `equals`, `contains`, `starts`, and `ends`. With each of these types of requirements you also need a string to check against which means if I wanted to check if the output of the code starts "Hello" I would include the condition `starts: Hello` on a new line. Note again how the syntax needs the space between the colon and start of the value along with the lack of quotes.
    - equals --> checks if the whole output is exactly the same to the value. Does not include the end new line character.
    - contains --> checks if value is anywhere within the output string.
    - starts --> checks if the start of the string is the same as value.
    - ends --> checks if the end of the string is the same as value. Does not inlcude the newline character of breaking to the new line. 

## Structure
```
.
├── [SECRET JSON KEY FOR GOOGLE SHEETS].json
├── Conditions.py
├── conditions.txt
├── files
│   	…
├── GoogleSheetsConnection.py
├── main.py
├── README.md
├── Screenshot2024-05-13172818.png
├── static
│   ├── main.js
│   └── style.css
└── templates
    └── index.html
```

## Authors

Miles Fritzmather, Jacob Mathew, & Matthew Shi

## License

This project is licensed under the MIT License



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

## How to write an assignment into a .txt file
Lorem ipsum....

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



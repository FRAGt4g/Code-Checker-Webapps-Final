import io  # for reading files
import os  # for using operating system functionality
import subprocess  # for running files
import re  # for regular expressions

from flask import Flask, redirect, render_template, request, url_for  # you know this one

from conditions import Lab_Requirements, Condition
import GoogleSheetsConnection

app = Flask(__name__)

class Submission_Result:
  grade = 0
  failures = []
  output = ""

  def __init__(self, grade, failures, output):
    self.grade = grade
    self.failures = failures
    self.output = output


output = subprocess.run(['./output'])

@app.route('/')
def root():
  print("Hello world!")
  print(output)
  
  return render_template('index.html', results=None)
  
@app.route('/submit', methods=['POST'])
def submit():
  if 'files[]' not in request.files:
    print('requested data is non-existent')
    return redirect(url_for('root'))

  files = request.files.getlist('files[]')  # Get the list of files uploaded
  
  if files[0].filename == '':
    return redirect(url_for('root'))

  path, attempt_number = create_folder_with_suffix('files', f'S{request.form["ID"]}')
  for file in files:
    fName = str(file.filename)
    with open(os.path.join(path, fName), "wb") as f:
      f.write(file.stream.read())

  results = runSubmission_txt(path)
  
  GoogleSheetsConnection.writeSubmission("LASA_ALLOC", [
    request.form['ID'], #Id
    results.grade, #Grade
    attempt_number if attempt_number != 0 else 1, #Attempt number
    str([file_data.filename for file_data in files]), #Files
    GoogleSheetsConnection.to_sheet_cell(results.failures), #Problems
    results.output #Output
  ])
  
  print(f"Grade would be a { results.grade }%")
  print("Problems: ")
  for fault in results.failures:
    print(f"\t{fault[0]}: {str(fault[1])}")
  
  return render_template('index.html', results=results)

def runSubmission_txt(dir):
  output = run_code(dir)
  print("****Code output****: " + str(output))

  requirements = Lab_Requirements('conditions.txt')
  print("----------------------Done compiling conditions----------------------")
  print(requirements)
  checks = requirements.passedLevel(output)
  return Submission_Result(checks[0], checks[1], output)


def run_code(dir):
  print('dir: ' + str(dir))
  # Check if there are both C++ and Java files
  file_dirs = os.listdir(dir)
  has_cpp = any(filename.endswith('.cpp') for filename in file_dirs)
  has_java = any(filename.endswith('.java') for filename in file_dirs)

  if has_cpp and has_java:
    return "Mix of C++ and Java files. Only one type of source files should be provided."

  elif has_cpp:
    return run_cpp(dir)

  elif has_java:
    return run_java(dir)
    
  return "No useable files found. Please specify a different directory or add files."

def run_cpp(dir):
  # Compile all C++ source files into a single executable
  compilation_command = ['g++', '-o', 'output'] + ['-std=c++11'] + [os.path.join(dir, file_dir) for file_dir in os.listdir(dir) if file_dir.endswith('.cpp')]
  
  compilation_process = subprocess.Popen(
    compilation_command, 
    stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE
  )
  compilation_output, compilation_errors = compilation_process.communicate()
  
  if compilation_errors:
    # Compilation failed, return the error message
    return "Compilation Error:\n" + compilation_errors.decode('utf-8')
  
  # Run the compiled executable
  execution_process = subprocess.Popen(['./output'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  execution_output, execution_errors = execution_process.communicate()
  
  if execution_errors:
    # Execution failed, return the error message
    return "Execution Error:\n" + execution_errors.decode('utf-8')
  
  # Return the output of the execution
  return execution_output.decode('utf-8')

def run_java(dir):
  print("running java tester. Directory is: " + dir)

  compilation_command = ["javac"] + [file_dir for file_dir in os.listdir(dir)]
  subprocess.run(compilation_command, cwd=dir, check=True)

  run_command = ['java'] + [
    class_files.split('.')[0] for class_files in os.listdir(dir) if class_files.endswith('.class')
  ]
  output = subprocess.run(
    run_command,
    cwd=dir, 
    text=True, 
    stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE
  )
  print("java output: " + str(output))
  if (output.returncode != 0):
    return "Execution Errors: " + output.stderr
  
  return output.stdout


def open_file_with_suffix(filename, mode='wb'):
  base, ext = os.path.splitext(filename)
  counter = 1
  while os.path.exists(filename):
    counter += 1
    filename = f"{base} ({counter}){ext}"
  return open(filename, mode)

def create_folder_with_suffix(base_dir, sub_dir):
  base = os.path.join(base_dir, sub_dir)
  if not os.path.exists(base):
    os.makedirs(base)
    return (str(base), 0)
  
  index = 2
  while index < 20: #To ensure no there will never be more than 20 submissions from one id
    folder_name = f"{sub_dir} ({index})"
    folder_path = os.path.join(base_dir, folder_name)
    if not os.path.exists(folder_path):
      os.makedirs(folder_path)
      return (str(folder_path), index)
    index += 1

  return ("REACHED OVER 10 FILES", -1)

def compile_conditions(filename='conditions.txt'):
  with open(filename, 'r') as f:
    conditions = f.read().split('\n')
  return "".join(conditions)

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080)
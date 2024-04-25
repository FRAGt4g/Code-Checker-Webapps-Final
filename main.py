import io  # for reading files
import os  # for using operating system functionality
import subprocess  # for running files
import re  # for regular expressions

from flask import Flask, redirect, render_template, request, url_for  # you know this one

app = Flask(__name__)

@app.route('/')
def root():
  return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
  if 'files[]' not in request.files:
    print('requested data is non-existent')
    return redirect(url_for('root'))

  files = request.files.getlist('files[]')  # Get the list of files uploaded
  
  if files[0].filename == '':
    return redirect(url_for('root'))

  else:
    path = create_folder_with_suffix('files', f'S{request.form["ID"]}')
    for file in files:
      fName = str(file.filename)
      with open(os.path.join(path, fName), "wb") as f:
        f.write(file.stream.read())

  output = runSubmission_txt(files)
  print(output)
  return render_template('index.html', message=str())

def runSubmission_txt(files):
  conditions = compile_conditions()
  print("Requirement: " + conditions)
  output = run_code(files)
  passed = re.search(conditions, output)
  return passed

@app.route("/run", methods=["POST"])
def runSubmissions():
  print(os.path.join('files', id) for id in os.listdir('files')) 
  outputs = { 
    id: run_code(os.path.join('files', id)) for id in os.listdir('files') 
  }
  passed = { 
    id: outputs[id] for id in outputs if re.search(request.form["requirements"], outputs[id])
  }

  results = [str(outputs[id]) for id in outputs]
  print(results)


  print('outputs: ' + str(outputs))
  print('who passed: ' + str(passed))
  return redirect(url_for('root'))



def run_code(source_files):
  print('source files: ' + str(source_files))
  # Check if there are both C++ and Java files
  has_cpp = any(file.filename.endswith('.cpp') for file in source_files)
  has_java = any(file.filename.endswith('.java') for file in source_files)

  if has_cpp and has_java:
    return "Mix of C++ and Java files. Only one type of source files should be provided."

  elif has_cpp:
    return run_cpp(source_files)

  elif has_java:
    return run_java(source_files)
    
  return "No useable files found. Please specify a different directory or add files."

def run_cpp(source_files):
  # Compile all C++ source files into a single executable
  compilation_command = ['g++', '-o', 'output'] + source_files
  compilation_process = subprocess.Popen(compilation_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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

def run_java(source_files):
  # Compile all Java source files into bytecode
  compilation_command = ['javac'] + source_files
  compilation_process = subprocess.Popen(compilation_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  compilation_output, compilation_errors = compilation_process.communicate()

  if compilation_errors:
      # Compilation failed, return the error message
      return "Compilation Error:\n" + compilation_errors.decode('utf-8')

  # Find the main Java file to execute
  main_java_file = next(file for file in source_files if file.endswith('.java') and 'Main' in file)

  # Run the compiled Java program
  execution_process = subprocess.Popen(['java', main_java_file[:-5]], cwd=project_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  execution_output, execution_errors = execution_process.communicate()

  if execution_errors:
      # Execution failed, return the error message
      return "Execution Error:\n" + execution_errors.decode('utf-8')

  # Return the output of the execution
  return execution_output.decode('utf-8')



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
    return str(base)
  
  index = 2
  while index < 10: #To ensure no there will never be more than 10 submissions from one id
    folder_name = f"{sub_dir} ({index})"
    folder_path = os.path.join(base_dir, folder_name)
    if not os.path.exists(folder_path):
      os.makedirs(folder_path)
      return str(folder_path)
    index += 1

  return "Reached over 10 folders"

def compile_conditions(filename='conditions.txt'):
  with open(filename, 'r') as f:
    conditions = f.read().split('\n')
  return "".join(conditions)

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080)
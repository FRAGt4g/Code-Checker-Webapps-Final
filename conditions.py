import os
import io
import re

# Class for individual condition within a grade level of a Project
# Variable 'type' is a string that represents the type of condition (either: equals, starts, ends, or contains)
# Variables 'value' is a string that holds the value of the condition i.e any string that needs to be within the final output
# an example Condition might look like: Condition("equals", "Hello")
    # this would be equivelant to ^Hello$ in regex.
class Condition:
  type = None
  value = ""

  #Dictionary of conversions from type to real regex. Used in 'toregex()'
  regex_patterns = {
    "contains": "___",
    "starts": "^___",
    "ends": "___$",
    "equals": "^___\n$",
  }
  
  def __init__(self, type, value):
    self.type = type
    self.value = value

  def __str__(self):
    return f"{self.type}: {self.value}"    

  #Returns a regex expression of the condition. 
  #Takes in self so it can personal variables. 
  #Throws an error if the type is not valid
  def toregex(self):
    if self.type in self.regex_patterns:
      print(self.regex_patterns[str(self.type)].replace('___' , self.value))
      return self.regex_patterns[str(self.type)].replace('___' , self.value)

    raise Exception("Invalid condition type")
    

#Class for entire lab grade requirements. There would be one of these for an entire lab submision and it would contain many conditions for each grade level.
class Lab_Requirements:
  project_name = ""
  levels = {
    #Grade value:
    #Conditions to pass
  }

  #Contructor that takes in the file name of the text file for the conditions and lab requirements
  def __init__(self, filename):
    current_grade_level = 0
    with open(filename, 'rb+') as f:
      #Read and assign lab name from first line of file
      top_line = f.readline().decode('utf-8')
      #Parses the first line into only the string of the actual project name (removes the '#Project: ' part)
        #lab_name will be None if first line does not start with '#Project: '
      self.project_name = top_line[len("#Project: "):-1] if top_line.startswith('#Project: ') else None

      #iterate over all lines in file
      for line in f.readlines():
        line = line.decode('utf-8')
        if line[0] == '\n' or line.startswith('#'): continue #Lines starting with # are comments and should be ignored. Lines that are empty shoudl also be skipped

        #Starting with an @ means starting a new grade level. It should be followed by a number for that grade level. All conditions that follow will be added to this grade level until a new grade level is defined
        if line.startswith('@'):
          current_grade_level = int(line[1:-2])
          self.levels[current_grade_level] = []
          continue

        #Adding new condition to current grade level.
          #The text must be spliced apart first around the ': '. YOU MUST INCLUDE THAT SPACE BETWEEN THE COLON AND THE CONDITION.
          #The left hand side is the type of condition. The right hand side is the value of the condition.
        self.levels[current_grade_level].append(Condition(line.split(': ')[0], line.split(': ')[1][:-1]))

  #An override for str(Lab_Requirements) that returns the name of the project followed by each grade level and its conditions
  def __str__(self):
    result = f"Project name: {self.project_name}\n\tGrade Levels:\n"
    for level, conditions in self.levels.items():
        result += f"\t\t{level}:\n"
        for condition in conditions:
            result += f"\t\t\t{condition}\n"  # Calling __str__() explicitly here
    return result

  #Returns a tuple of the maximum grade the output would acheive along with the points where the ouput failed.
    #If the output is perfect, the tuple would be (100, None)
    #Otherwise, it would look something like (80, [Condition('starts', 'Hello'), Condition('ends', 'World')])
  def passedLevel(self, output):
    failures = [
      #Tuple of grade level and condition
    ]
    for level, conditions in reversed(self.levels.items()):
      failed_at_level = False
      for condition in conditions:
        if not re.search(condition.toregex(), output):
          failures.append((level, condition))
          failed_at_level = True
          break
      if not failed_at_level:
        return (level, failures)
    return (0, failures)
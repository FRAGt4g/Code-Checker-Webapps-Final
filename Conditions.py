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

  def to_dict(self):
    return {
      'type': self.type,
      'value': self.value
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
      return self.regex_patterns[str(self.type)].replace('___' , self.value)

    raise Exception("Invalid condition type")


#Class for entire lab grade requirements. There would be one of these for an entire lab submision and it would contain many conditions for each grade level.
class Lab_Requirements:
  lab_name = ""
  filetypes = []
  levels = {
    #Grade value:
    #Conditions to pass
  }

  def __init__(self, lab_name, filetypes, levels):
    self.lab_name = lab_name
    self.filetypes = filetypes
    self.levels = levels

  def to_dict(self):
    return {
      'lab name': self.lab_name,
      'filetypes': self.filetypes,
      'levels': {
        level : [condition.to_dict() for condition in self.levels[level]] for level in self.levels
      },
    }

  #An override for str(Lab_Requirements) that returns the name of the project followed by each grade level and its conditions
  def __str__(self):
    result = f"Project name: {self.lab_name}\n\tGrade Levels:\n"
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
    print("Input for check: " + output)
    for level, conditions in reversed(self.levels.items()):
      failed_at_level = False
      for condition in conditions:
        print("REGEX: '" + condition.toregex() + "'")
        if not re.search(condition.toregex(), output):
          failures.append((level, condition))
          failed_at_level = True
      if not failed_at_level:
        return (level, failures)
        
    return (0, failures) #Failed at least one condition at every grade level

  @staticmethod
  def fault_to_string(fault):
      return f"What is required: { str(fault[1]) }. Grade level: { fault[0] }"
  
  @staticmethod
  def compileAllLabConditions(filename):
    current_grade_level = 0
    labs = {
      #Lab name (key)
      #Lab requirements (value)
    }
    with open(filename, 'rb+') as f:
      #Read and assign lab name from first line of file 
      top_line = f.readline().decode('utf-8')
      #Parses the first line into only the string of the actual project name (removes the '#Project: ' part)
        #lab_name will be None if first line does not start with '#Project: '
      if (not top_line.startswith('Project:')):
        ValueError("Must start conditions file with a Project name. Syntax is: Project: ____")
      
      filetypes = [filetype.strip() for filetype in top_line[top_line.index('[')+1:top_line.index(']')].split(',')]
      print("f: " + str(filetypes))
      current_lab_name = top_line[top_line.index(':')+1:-2]
      labs[current_lab_name] = Lab_Requirements(current_lab_name, filetypes, {})

      #iterate over all lines in file
      for line in f.readlines():
        line = line.decode('utf-8')
        if line.startswith('#') or line.strip() == "": continue #Lines starting with # are comments and should be ignored. Lines that are empty should also be skipped

        #Starting with an @ means starting a new grade level. It should be followed by a number for that grade level. All conditions that follow will be added to this grade level until a new grade level is defined
        if line.startswith('@'):
          current_grade_level = int(line.strip()[1:])
          labs[current_lab_name].levels[current_grade_level] = []
          continue

        if line.startswith('Project'):
          filetypes = [filetype.strip() for filetype in line[line.index('[')+1:line.index(']')].split(',')]
          current_lab_name = line[line.index(':')+1:-2]
          labs[current_lab_name] = Lab_Requirements(current_lab_name, filetypes, {})
          continue

        #Adding new condition to current grade level.
          #The text must be spliced apart first around the ': '. YOU MUST INCLUDE THAT SPACE BETWEEN THE COLON AND THE CONDITION.
          #The left hand side is the type of condition. The right hand side is the value of the condition.
        type, value = line.split(': ')

        input = Condition(type, value[:-2])
        labs[current_lab_name].levels[current_grade_level].append(input)

    return labs

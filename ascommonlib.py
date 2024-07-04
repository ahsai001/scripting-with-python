import os

import tkinter as tk
from tkinter import filedialog

def get_line_in_file(filename, line_number):
  data = ""
  with open(filename, 'r') as read_file:
    for index, line in enumerate(read_file):
      if line_number-1 == index:
        data = line
        break
  return data 

def exist_line_in_file(filename, line_string):
  exist = False
  with open(filename, 'r') as read_file:
    for line in read_file:
      if line_string in line:
        exist = True
        break
  return exist 

def exist_multiline_in_file(filename, multiline_string):
  exist = False
  with open(filename, 'r') as read_file:
    content: str = ''
    for line in read_file:
        content += line
  if multiline_string in content:
    exist = True
  return exist

def replace_in_file(filename, old_string, new_string):
  with open(filename, 'r') as read_file, open(filename + '.bak', 'w') as write_file:
    for line in read_file:
      if old_string in line:
        write_file.write(line.replace(old_string, new_string))
      else:
        write_file.write(line)
  os.replace(filename + '.bak', filename)

def remove_all_before(filename, before_keyword, include_keyword=False):
  with open(filename, 'r') as read_file, open(filename + '.bak', 'w') as write_file:
    in_removal_zone = True 
    pending_once = False
    for line in read_file:
      if before_keyword in line:
        if include_keyword:
          pending_once = True
        else:
          in_removal_zone = False
      if not in_removal_zone:
        write_file.write(line)
      if pending_once:
        pending_once = False
        in_removal_zone = False
  os.replace(filename + '.bak', filename)

def remove_all_after(filename, after_keyword, include_keyword=False):
  with open(filename, 'r') as read_file, open(filename + '.bak', 'w') as write_file:
    in_removal_zone = False 
    pending_once = False
    for line in read_file:
      if after_keyword in line:
        if include_keyword:
          in_removal_zone = True
        else:
          pending_once = True
      if not in_removal_zone:
        write_file.write(line)
      if pending_once:
        pending_once = False
        in_removal_zone = True
  os.replace(filename + '.bak', filename)


def remove_multiline_strings(filename, strings):
  with open(filename, 'r') as read_file, open(filename + '.bak', 'w') as write_file:
    content: str = ''
    for line in read_file:
        content += line

    new_content = content.replace(strings,"")
    write_file.write(new_content)

  os.replace(filename + '.bak', filename)

def read_file(filename):
    content: str = ''
    with open(filename, 'r') as read_file:
      content: str = ''
      for line in read_file:
          content += line
    return content


def prepend_to_file(filename, content):
  with open(filename, 'r') as read_file, open(filename + '.bak', 'w') as write_file:
    write_file.write(f"{content}\n")  # Write new content at the beginning
    write_file.writelines(read_file)  # Append existing file content

  os.replace(filename + '.bak', filename)

def append_to_file(filename, content):
  with open(filename, 'r') as read_file, open(filename + '.bak', 'w') as write_file:
    write_file.writelines(read_file)  # Write existing file content
    write_file.write(f"{content}\n")  # Write new content at the end

  os.replace(filename + '.bak', filename)



def insert_strings_to_file_after(filename, strings, after_keyword):
  with open(filename, 'r') as read_file, open(filename + '.bak', 'w') as write_file:
    for line in read_file:
      if after_keyword in line:
        write_file.write(line)
        write_file.write(strings+"\n")
      else:
        write_file.write(line)
  os.replace(filename + '.bak', filename)

def insert_strings_to_file_before(filename, strings, before_keyword):
  with open(filename, 'r') as read_file, open(filename + '.bak', 'w') as write_file:
    for line in read_file:
      if before_keyword in line:
        write_file.write(strings+"\n")
        write_file.write(line)
      else:
        write_file.write(line)
  os.replace(filename + '.bak', filename)


def insert_strings_to_file_line(filename, strings, line_number):
  with open(filename, 'r') as read_file, open(filename + '.bak', 'w') as write_file:
    for index, line in enumerate(read_file):
      if index == (line_number-1):
        write_file.write(strings+"\n")
        write_file.write(line)
      else:
        write_file.write(line)
  os.replace(filename + '.bak', filename)


def change_directory(target_dir):
    try:
        os.chdir(target_dir)
        print(f"Successfully changed directory to: {os.getcwd()}")
    except OSError as e:
        print(f"Error changing directory: {e}")
        exit(1)


def create_new_file(filename, content):
  """
  Creates a new file and writes the specified content to it.

  Args:
      filename (str): The name of the file to create.
      content (str): The content to write to the file.
  """

  try:
    with open(filename, "w") as file:
      file.write(content)
    print(f"File '{filename}' created successfully!")
  except OSError as error:
    print(f"Error creating file: {error}")


def input_filepath(instruction):
  filepath = input(f"{instruction} or enter to open file picker: ")
  if filepath=="":
    filepath = choose_file()
  return filepath

def input_directorypath(instruction):
  folderpath = input(f"{instruction} or enter to open directory picker: ")
  if folderpath=="":
    folderpath = choose_directory()
  return folderpath

def choose_file():
  """Opens a file picker dialog and returns the selected file path."""

  root = tk.Tk()
  root.withdraw()  # Hide the main window
  root.attributes('-topmost', True)  # Set the dialog to be always on top

  filepath = filedialog.askopenfilename()
  
  normalized_path = os.path.normpath(filepath)
  if normalized_path:
    print(f"You selected file : {normalized_path}")
    return normalized_path
  else:
    print("No file selected.")
    return ''
  
def choose_directory():
  """Opens a file picker dialog and returns the selected folder path."""

  root = tk.Tk()
  root.withdraw()  # Hide the main window
  root.attributes('-topmost', True)  # Set the dialog to be always on top

  directory_path = filedialog.askdirectory()
  normalized_path = os.path.normpath(directory_path)
  if normalized_path:
    print(f"You selected directory : {normalized_path}")
    return normalized_path
  else:
    print("No directory selected.")
    return ''



def run_command(command: str):
  result = os.system(command)
  if result == 0:
    return True
  return False 



def generate_class_from_json(json,project_directory,path_to_file, filename, target_file_format):
  request_dir = os.path.join(project_directory, path_to_file)
  os.makedirs(request_dir, exist_ok=True)
  json_file_path = os.path.join(project_directory, f"{path_to_file}/{filename}.json")
  output_file_path = os.path.join(project_directory, f"{path_to_file}/{filename}.{target_file_format}")
  create_new_file(json_file_path, json)
  command = f"quicktype {json_file_path} -o {output_file_path}"
  run_command(command)
  remove_file(json_file_path)


def remove_file(fullpath):
  try:
    os.remove(fullpath)
    print(f"File '{fullpath}' deleted successfully.")
  except FileNotFoundError:
    print(f"Error: File '{fullpath}' not found.")
  except PermissionError:
    print(f"Error: You don't have permission to delete '{fullpath}'.")
  except OSError as e:
    print(f"An error occurred while deleting the file: {e}")
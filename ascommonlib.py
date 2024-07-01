import os

import tkinter as tk
from tkinter import filedialog


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
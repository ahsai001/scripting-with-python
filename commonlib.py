import os


def change_directory(target_dir):
    try:
        os.chdir(target_dir)
        print(f"Successfully changed directory to: {os.getcwd()}")
    except OSError as e:
        print(f"Error changing directory: {e}")
        exit(1)


def create_file_with_content(filename, content):
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

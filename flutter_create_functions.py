import os
import shutil

from commonlib import change_directory

print("Selamat datang di flutter functions: ")
print("1. create flutter project")
print("2. define folder with clean architecture")

task = input("Apa yg ingin anda lakukan (1 atau 2): ")

if task=="1":
    org = input("masukkan unik org: ")
    name = input("masukkan nama aplikasi: ")
    folder = input("masukkan path folder: ")

    if folder!="":
        change_directory(folder)
    command = f"flutter create --org {org} --project-name {name} {name}"
    result = os.system(command)

    if result == 0:
        print(f"task '{task}' executed successfully.")
    else:
        print(f"Error: task '{task}' failed.")
elif task=="2":
    project_dir = input("masukkan path folder: ")

    # Define folder structure
    folders = [
        "lib",
        "lib/src",
        "lib/src/app",
        "lib/src/domain",
        "lib/src/data",
        "lib/src/app/pages",
        "lib/src/app/widgets",
        "lib/src/domain/usecases",
        "lib/src/domain/entities",
        "lib/src/domain/irepositories",
        "lib/src/data/repositories",
        "lib/src/data/datasources",
        "lib/src/data/models",
    ]

    # Create folders within the project
    for folder in folders:
        full_path = os.path.join(project_dir, folder)
        os.makedirs(full_path, exist_ok=True)

    shutil.copyfile("../scripting-with-python/flutter_create_functions/general_usecase.dart", os.path.join(project_dir, "lib/src/domain/usecases/general_usecase.dart"))

    print(f"Clean architecture folders created at: {project_dir}")
else:
    print(f"task '{task}' not defined")
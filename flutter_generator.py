import os
import shutil

from ascommonlib import append_to_file, change_directory, choose_file, input_directorypath, input_filepath, read_file, run_command

print("Welcome in flutter generator: ")
print("1. create flutter project")
print("2. init folder lib with clean architecture")
print("3. activate launcher icon")
print("4. activate native splash")
print("5. generate domain layer based on json")
print("press enter to exit")

task = input("What do you want (1 or 2): ")

script_directory = os.getcwd()
flutter_generator_dir = os.path.join(script_directory,"flutter_generator")


flutter_command = input("input flutter command (fvm flutter/flutter, default flutter): ")
if(flutter_command==""):
    flutter_command = "flutter"

def activate_launcher_icons(project_directory):
    change_directory(project_directory)
    command = f"{flutter_command} pub add flutter_launcher_icons"
    run_command(command)

    launcher_filepath = input_filepath("input image file for launcher icons")
    print(f"launcher_filepath : {launcher_filepath}")

    asset_dir_name=input("input asset directory name: ")
    print(f"asset_dir_name : {asset_dir_name}")

    asset_directory = os.path.join(project_directory, asset_dir_name)
    print(f"asset_directory : {asset_directory}")

    os.makedirs(asset_directory, exist_ok=True)

    launcher_icon_filename = os.path.basename(launcher_filepath).replace(" ","_").lower()
    launcher_filepath_local = os.path.join(asset_directory,launcher_icon_filename)
    print(f"launcher_filepath_local : {launcher_filepath_local}")
    
    shutil.copyfile(launcher_filepath, launcher_filepath_local)


    pubspec_yaml = os.path.join(project_directory, "pubspec.yaml")
    launcher_config_content = read_file(os.path.join(flutter_generator_dir, "launcher_icons_config.yaml"))

    background_color = input("input background color (#RRGGBB): ")
    theme_color = input("input theme color (#RRGGBB): ")

    launcher_config_content = launcher_config_content.replace("{{icon_asset_path}}", f"{asset_dir_name}/{launcher_icon_filename}").replace("{{background_color}}", background_color).replace("{{theme_color}}", theme_color)
    append_to_file(pubspec_yaml, launcher_config_content)

    command = f"dart run flutter_launcher_icons"
    run_command(command)

def activate_native_splash(project_directory):
    change_directory(project_directory)
    command = f"{flutter_command} pub add flutter_native_splash"
    run_command(command)

    splash_filepath = input_filepath("input image file for splash")

    asset_dir_name=input("input asset directory name: ")
    asset_directory = os.path.join(project_directory, asset_dir_name)

    
    os.makedirs(asset_directory, exist_ok=True)

    splash_icon_filename = os.path.basename(splash_filepath).replace(" ","_").lower()
    splash_filepath_local = os.path.join(asset_directory,splash_icon_filename)
    print(f"splash_filepath_local : {splash_filepath_local}")
    
    shutil.copyfile(splash_filepath, splash_filepath_local)


    pubspec_yaml = os.path.join(project_directory, "pubspec.yaml")
    splash_config_content = read_file(os.path.join(flutter_generator_dir, "native_splash_config.yaml"))

    background_color = input("input background color (#RRGGBB): ")
    
    splash_config_content = splash_config_content.replace("{{splash_asset_path}}", f"{asset_dir_name}/{splash_icon_filename}").replace("{{background_color}}", background_color)
    append_to_file(pubspec_yaml, splash_config_content)

    command = f"dart run flutter_native_splash:create"
    run_command(command)

if task=="1":  
    project_directory_name = input("input project directory name: ")
    org = input("input org name (com.example): ")
    project_name = input("input app name: ")
    dest_directory = input_directorypath("input dest directory")

    if dest_directory!="":
        change_directory(dest_directory)
    else:
        dest_directory = script_directory

    command = f"{flutter_command} create --org {org} --project-name {project_name} {project_directory_name}"
    create_success = run_command(command)

    project_root_directory = os.path.join(dest_directory, project_directory_name)
    print(f"project_root_directory : {project_root_directory}")


    add_launcher = input("do you want to add launcher icons (y/n): ")
    if add_launcher=="y":
        activate_launcher_icons(project_root_directory)

    add_splash = input("do you want to add native splash (y/n): ")
    if add_splash=="y":
        activate_native_splash(project_root_directory)


    command = f"{flutter_command} pub get"
    pubget_success = run_command(command)

    if create_success and pubget_success:
        print(f"task '{task}' executed successfully.")
    else:
        print(f"Error: task '{task}' failed.")
elif task=="2":
    project_dir = input_directorypath("input project directory")

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

    # copy some files
    shutil.copyfile("../scripting-with-python/flutter_generator/general_usecase.dart", os.path.join(project_dir, "lib/src/domain/usecases/general_usecase.dart"))

    print(f"Clean architecture folders created at: {project_dir}")
elif task=="3":
    project_directory = input_directorypath("input project directory")
    print(f"project_directory : {project_directory}")
    activate_launcher_icons(project_directory)
elif task=="4":
    project_directory = input_directorypath("input project directory")
    print(f"project_directory : {project_directory}")
    activate_native_splash(project_directory)
elif task=="5":
    project_directory = input_directorypath("input project directory")
    print(f"project_directory : {project_directory}")
    print("Coming soon, please be patient")
else:
    print("Thanks for using flutter generator")
    print("managed by ahsailabs")
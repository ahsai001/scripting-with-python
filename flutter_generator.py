import os
import shutil

from ascommonlib import append_to_file, change_directory, choose_file, create_new_file, exist_line_in_file, generate_class_from_json, get_line_in_file, input_directorypath, input_filepath, insert_strings_to_file_after, insert_strings_to_file_before, prepend_to_file, read_file, remove_all_after, remove_all_before, remove_multiline_strings, replace_in_file, run_command

print("Welcome in flutter generator: ")
print("1. create flutter project")
print("2. init folder lib with clean architecture")
print("3. activate launcher icon")
print("4. activate native splash")
print("5. add flutter alcore")
print("6. add DI")
print("7. add app preference")
print("8. add api package")
print("9. add database package")
print("10. create new datasource and repository")
print("11. create new model and/or entity")
print("12. 1-2-3-4-6-7-8-9")
print("press enter to exit")

task = input("What do you want (1 or 2): ")

script_directory = os.getcwd()
flutter_generator_dir = os.path.join(script_directory,"flutter_generator")

if task != "":
    flutter_command = input("input flutter command (fvm flutter/flutter, default flutter): ")
    if(flutter_command==""):
        flutter_command = "flutter"

def activate_launcher_icons(project_directory):
    change_directory(project_directory)
    command = f"{flutter_command} pub add dev:flutter_launcher_icons"
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
    command = f"{flutter_command} pub add dev:flutter_native_splash"
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

def get_project_name(project_directory):
    pubspec_yaml_file = os.path.join(project_directory, "pubspec.yaml")
    line_1_pubspec = get_line_in_file(pubspec_yaml_file, 1)
    project_name = line_1_pubspec.split(": ")[1].strip()
    return project_name

if task=="1":  
    print("1. create flutter project")
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

    # split main.dart and app.dart
    change_directory(project_root_directory)
    os.makedirs("lib/src", exist_ok=True)
    shutil.copyfile("lib/main.dart", "lib/src/app.dart")
    main_file = os.path.join(project_root_directory, "lib/main.dart")
    app_file = os.path.join(project_root_directory, "lib/src/app.dart")
    remove_all_before(app_file, "class MyApp extends StatelessWidget {")
    remove_all_after(main_file, "class MyApp extends StatelessWidget {",include_keyword=True)
    prepend_to_file(app_file, "import 'package:flutter/material.dart';\n")
    prepend_to_file(main_file, f"import 'package:{project_name}/src/app.dart';")
    
    test_file = os.path.join(project_root_directory, "test/widget_test.dart")
    replace_in_file(test_file,f"import 'package:{project_name}/main.dart';",f"import 'package:{project_name}/src/app.dart';\n")

    # pub get
    command = f"{flutter_command} pub get"
    pubget_success = run_command(command)

    if create_success and pubget_success:
        print(f"task '{task}' executed successfully.")
    else:
        print(f"Error: task '{task}' failed.")
elif task=="2":
    print("2. init folder lib with clean architecture")
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
    shutil.copyfile("../scripting-with-python/flutter_generator/general_usecase.dart.txt", os.path.join(project_dir, "lib/src/domain/usecases/general_usecase.dart"))

    print(f"Clean architecture folders created at: {project_dir}")
elif task=="3":
    print("3. activate launcher icon")
    project_directory = input_directorypath("input project directory")
    print(f"project_directory : {project_directory}")
    activate_launcher_icons(project_directory)
    print(f"task '{task}' executed successfully.")
elif task=="4":
    print("4. activate native splash")
    project_directory = input_directorypath("input project directory")
    print(f"project_directory : {project_directory}")
    activate_native_splash(project_directory)
    print(f"task '{task}' executed successfully.")
elif task=="5":
    print("5. add flutter alcore")
    project_directory = input_directorypath("input project directory")
    print(f"project_directory : {project_directory}")
    print(f"flutter_generator_dir : {flutter_generator_dir}")
    flutter_alcore_yaml = read_file(os.path.join(flutter_generator_dir, "common_packages.yaml"))
    pubspec_yaml = os.path.join(project_directory, "pubspec.yaml")
    print(f"pubspec_yaml : {pubspec_yaml}")
    print(f"flutter_alcore_yaml : {flutter_alcore_yaml}")
    insert_strings_to_file_before(pubspec_yaml, flutter_alcore_yaml+"\n\n","dev_dependencies:")
    change_directory(project_directory)
    command = f"{flutter_command} pub get"
    pubget_success = run_command(command)
    if pubget_success:
        print(f"task '{task}' executed successfully.")
    else:
        print(f"Error: task '{task}' failed.")    
elif task=="6":
    print("6. add DI")
    project_directory = input_directorypath("input project directory")
    print(f"project_directory : {project_directory}")
    print(f"flutter_generator_dir : {flutter_generator_dir}")
    
    change_directory(project_directory)

    command = f"{flutter_command} pub add get_it logger"
    run_command(command)

    main_file = os.path.join(project_directory, "lib/main.dart")
    if not exist_line_in_file(main_file, "Future<void> setupServices() async {"):
        append_to_file(main_file, '''Future<void> setupServices() async {

  //DO NOT REMOVE/CHANGE THIS : SETUP SERVICES
}''')
        
    if not exist_line_in_file(main_file, "Future<void> registerDI() async {"):
        append_to_file(main_file, '''Future<void> registerDI() async {
  var inject = GetIt.I; 
  inject.registerLazySingleton(() => Logger());
  
  /* // use like this : inject()
  
  // examples :
  inject.registerLazySingleton(() => SerialNumberRemoteDatasource(inject()));
  inject.registerLazySingleton<ISerialNumberRepository>(() => SerialNumberRepository(inject()));
  inject.registerFactory(() => CheckAppUpdateUseCase(inject()));
  */

  //DO NOT REMOVE/CHANGE THIS : REGISTER DI
}''')

    if not exist_line_in_file(main_file, "await registerDI();"):    
        insert_strings_to_file_after(main_file, '''  //dependecy injection
  await registerDI();
  //logger
  Logger.level = kDebugMode ? Level.trace : Level.off;''', "Future<void> setupServices() async {")
    
    if not exist_line_in_file(main_file, "await setupServices();"): 
        insert_strings_to_file_before(main_file, '''\n  await setupServices();''', "runApp(")

    replace_in_file(main_file, "void main() {", "Future<void> main() async {")

    if not exist_line_in_file(main_file, "import 'package:get_it/get_it.dart';"): 
        insert_strings_to_file_before(main_file, '''import 'package:get_it/get_it.dart';\n''', "Future<void> main() async {")
    
    if not exist_line_in_file(main_file, "import 'package:logger/logger.dart';"): 
        insert_strings_to_file_before(main_file, '''import 'package:logger/logger.dart';\n''', "Future<void> main() async {")

    if not exist_line_in_file(main_file, "import 'package:flutter/foundation.dart';"): 
        insert_strings_to_file_before(main_file, '''import 'package:flutter/foundation.dart';\n''', "Future<void> main() async {")

    if not exist_line_in_file(main_file, "WidgetsFlutterBinding.ensureInitialized();"):
        insert_strings_to_file_before(main_file, '''  WidgetsFlutterBinding.ensureInitialized();''', "await setupServices();")
    

    # pub get
    command = f"{flutter_command} pub get"
    pubget_success = run_command(command)
    if pubget_success:
        print(f"task '{task}' executed successfully.")
    else:
        print(f"Error: task '{task}' failed.")
elif task=="7":
    print("7. add app preference")
    project_directory = input_directorypath("input project directory")
    print(f"project_directory : {project_directory}")
    print(f"flutter_generator_dir : {flutter_generator_dir}")

    # copy some files
    preference_dir = os.path.join(project_directory, "lib/src/data/preference")
    os.makedirs(preference_dir, exist_ok=True)
    shutil.copyfile("../scripting-with-python/flutter_generator/app_preference.dart.txt", os.path.join(project_directory, "lib/src/data/preference/app_preference.dart"))
    
    main_file = os.path.join(project_directory, "lib/main.dart")
    if not exist_line_in_file(main_file, "  inject.registerLazySingletonAsync<AppPreference>("):    
        insert_strings_to_file_before(main_file, '''  //app preferences
  inject.registerLazySingletonAsync<AppPreference>(() => AppPreference().initialize());\n\n''', "inject.registerLazySingleton(() => Logger());")

    project_name = get_project_name(project_directory)

    if not exist_line_in_file(main_file, f"import 'package:{project_name}/src/data/preference/app_preference.dart';"):
        insert_strings_to_file_before(main_file, f'''import 'package:{project_name}/src/data/preference/app_preference.dart';\n\n''', "Future<void> main() async {")

    # add dependecy
    change_directory(project_directory)
    command = f"{flutter_command} pub add shared_preferences"
    run_command(command)

    # pub get
    command = f"{flutter_command} pub get"
    pubget_success = run_command(command)
    if pubget_success:
        print(f"task '{task}' executed successfully.")
    else:
        print(f"Error: task '{task}' failed.")
elif task=="8":
    print("8. add api package")
    project_directory = input_directorypath("input project directory")
    print(f"project_directory : {project_directory}")
    print(f"flutter_generator_dir : {flutter_generator_dir}")


    api_dir = os.path.join(project_directory, "lib/src/data/api")
    env_dir = os.path.join(project_directory, "lib/env")
    # copy some files
    os.makedirs(api_dir, exist_ok=True)
    shutil.copyfile("../scripting-with-python/flutter_generator/api_client.dio.dart.txt", os.path.join(project_directory, "lib/src/data/api/api_client.dart"))
    shutil.copyfile("../scripting-with-python/flutter_generator/api_endpoint.dart.txt", os.path.join(project_directory, "lib/src/data/api/api_endpoint.dart"))
    shutil.copyfile("../scripting-with-python/flutter_generator/api_exception.dio.dart.txt", os.path.join(project_directory, "lib/src/data/api/api_exception.dart"))
    os.makedirs(env_dir, exist_ok=True)
    shutil.copyfile("../scripting-with-python/flutter_generator/env.dart.txt", os.path.join(project_directory, "lib/env/env.dart"))
    shutil.copyfile("../scripting-with-python/flutter_generator/.env.txt", os.path.join(project_directory, ".env"))
    

    change_directory(project_directory)

    # add deps
    command = f"{flutter_command} pub add dio package_info_plus pretty_dio_logger envied dev:envied_generator dev:build_runner"
    run_command(command)
    
   
    api_client_file = os.path.join(project_directory, "lib/src/data/api/api_client.dart")
    api_endpoint_file = os.path.join(project_directory, "lib/src/data/api/api_endpoint.dart")
    pubspec_yaml_file = os.path.join(project_directory, "pubspec.yaml")
    
    # replace content some files
    
    project_name = get_project_name(project_directory)
    replace_in_file(api_client_file,"{{project_name}}", project_name)
    replace_in_file(api_endpoint_file,"{{project_name}}", project_name)

    main_file = os.path.join(project_directory, "lib/main.dart")
    if not exist_line_in_file(main_file, "inject.registerSingleton<ApiClient>"):
        insert_strings_to_file_before(main_file, '''  //api client
  final apiClient = ApiClient();
  await apiClient.initialize();
  inject.registerSingleton<ApiClient>(apiClient);\n''', "inject.registerLazySingleton(() => Logger());")

    if not exist_line_in_file(main_file, f"import 'package:{project_name}/src/data/api/api_client.dart';"): 
        insert_strings_to_file_before(main_file, f'''import 'package:{project_name}/src/data/api/api_client.dart';\n''', "Future<void> main() async {")
    
    
    # build runner
    command = "dart run build_runner build"
    build_success = run_command(command)

    # pub get
    command = f"{flutter_command} pub get"
    pubget_success = run_command(command)
    if build_success and pubget_success:
        print(f"task '{task}' executed successfully.")
    else:
        print(f"Error: task '{task}' failed.")
elif task=="9":
    print("9. add database")
    project_directory = input_directorypath("input project directory")
    print(f"project_directory : {project_directory}")
    print(f"flutter_generator_dir : {flutter_generator_dir}")


    database_dir = os.path.join(project_directory, "lib/src/data/database")
    # copy some files
    os.makedirs(database_dir, exist_ok=True)
    shutil.copyfile("../scripting-with-python/flutter_generator/drift_provider.dart.txt", os.path.join(project_directory, "lib/src/data/database/drift_provider.dart"))
    

    change_directory(project_directory)
    project_name = get_project_name(project_directory)

    # add deps
    command = f"{flutter_command} pub add drift path path_provider sqlite3_flutter_libs dev:drift_dev dev:build_runner"
    run_command(command)
    
    
    pubspec_yaml_file = os.path.join(project_directory, "pubspec.yaml")

    main_file = os.path.join(project_directory, "lib/main.dart")
 
    if not exist_line_in_file(main_file, "inject.registerLazySingleton<DriftProvider>("):
        insert_strings_to_file_before(main_file, '''  inject.registerLazySingleton<DriftProvider>(() => DriftProvider());\n\n''', "inject.registerLazySingleton(() => Logger());")
    

    if not exist_line_in_file(main_file, f"import 'package:{project_name}/src/data/database/drift_provider.dart';"): 
        insert_strings_to_file_before(main_file, f'''import 'package:{project_name}/src/data/database/drift_provider.dart';\n''', "Future<void> main() async {")
   

    
    # build runner
    command = "dart run build_runner build"
    build_success = run_command(command)

    # pub get
    command = f"{flutter_command} pub get"
    pubget_success = run_command(command)
    
    if build_success and pubget_success:
        print(f"task '{task}' executed successfully.")
    else:
        print(f"Error: task '{task}' failed.")
elif task=="10":
    print("10. create new datasource and repository")
    project_directory = input_directorypath("input project directory")
    print(f"project_directory : {project_directory}")
    print(f"flutter_generator_dir : {flutter_generator_dir}")
    name = input("input repository/datasource name: ").lower()


    name_underlined = name.replace(" ", "_")
    name_titlecased= name.title().replace(" ", "")
    name_variablecased= name_titlecased[0].lower()+name_titlecased[1:]

    # make some folders
    irepos_dir = os.path.join(project_directory, "lib/src/domain/irepositories")
    os.makedirs(irepos_dir, exist_ok=True)
    usecases_dir = os.path.join(project_directory, f"lib/src/domain/usecases/{name_underlined}")
    os.makedirs(usecases_dir, exist_ok=True)
    entities_dir = os.path.join(project_directory, f"lib/src/domain/entities/{name_underlined}")
    os.makedirs(entities_dir, exist_ok=True)

    repos_dir = os.path.join(project_directory, "lib/src/data/repositories")
    os.makedirs(repos_dir, exist_ok=True)
    datasources_dir = os.path.join(project_directory, f"lib/src/data/datasources/{name_underlined}")
    os.makedirs(datasources_dir, exist_ok=True)
    models_dir = os.path.join(project_directory, f"lib/src/data/models/{name_underlined}")
    os.makedirs(models_dir, exist_ok=True)


    # copy some files
    shutil.copyfile("../scripting-with-python/flutter_generator/name_irepository.dart.txt", os.path.join(irepos_dir, f"{name_underlined}_irepository.dart"))
    shutil.copyfile("../scripting-with-python/flutter_generator/name_repository.dart.txt", os.path.join(repos_dir, f"{name_underlined}_repository.dart"))
    shutil.copyfile("../scripting-with-python/flutter_generator/name_local_datasource.dart.txt", os.path.join(datasources_dir, f"{name_underlined}_local_datasource.dart"))
    shutil.copyfile("../scripting-with-python/flutter_generator/name_remote_datasource.dart.txt", os.path.join(datasources_dir, f"{name_underlined}_remote_datasource.dart"))

    project_name = get_project_name(project_directory)

    irepo_file = os.path.join(irepos_dir, f"{name_underlined}_irepository.dart")
    replace_in_file(irepo_file,"{{name_titlecased}}", name_titlecased)

    repo_file = os.path.join(repos_dir, f"{name_underlined}_repository.dart")
    replace_in_file(repo_file,"{{project_name}}", project_name)
    replace_in_file(repo_file,"{{name_titlecased}}", name_titlecased)
    replace_in_file(repo_file,"{{name_variablecased}}", name_variablecased)
    replace_in_file(repo_file,"{{name_underlined}}", name_underlined)

    local_datasource_file = os.path.join(datasources_dir, f"{name_underlined}_local_datasource.dart")
    replace_in_file(local_datasource_file,"{{project_name}}", project_name)
    replace_in_file(local_datasource_file,"{{name_titlecased}}", name_titlecased)

    remote_datasource_file = os.path.join(datasources_dir, f"{name_underlined}_remote_datasource.dart")
    replace_in_file(remote_datasource_file,"{{project_name}}", project_name)
    replace_in_file(remote_datasource_file,"{{name_titlecased}}", name_titlecased)


    main_file = os.path.join(project_directory, "lib/main.dart")
 
    if not exist_line_in_file(main_file, f"  inject.registerLazySingleton(() => {name_titlecased}LocalDatasource(inject()));"):
        insert_strings_to_file_before(main_file, f'''  inject.registerLazySingleton(() => {name_titlecased}LocalDatasource(inject()));\n\n''', "  //DO NOT REMOVE/CHANGE THIS : REGISTER DI")
    if not exist_line_in_file(main_file, f"  inject.registerLazySingleton(() => {name_titlecased}RemoteDatasource(inject()));"):
        insert_strings_to_file_before(main_file, f'''  inject.registerLazySingleton(() => {name_titlecased}RemoteDatasource(inject()));\n\n''', "  //DO NOT REMOVE/CHANGE THIS : REGISTER DI")
    if not exist_line_in_file(main_file, f"  inject.registerLazySingleton<I{name_titlecased}Repository>(() => {name_titlecased}Repository(inject()));"):
        insert_strings_to_file_before(main_file, f'''  inject.registerLazySingleton<I{name_titlecased}Repository>(() => {name_titlecased}Repository(inject(),inject()));\n\n''', "  //DO NOT REMOVE/CHANGE THIS : REGISTER DI")
    

    if not exist_line_in_file(main_file, f"import 'package:{project_name}/src/data/datasources/{name_underlined}/{name_underlined}_local_datasource.dart';"): 
        insert_strings_to_file_before(main_file, f'''import 'package:{project_name}/src/data/datasources/{name_underlined}/{name_underlined}_local_datasource.dart';\n''', "Future<void> main() async {")
   
    if not exist_line_in_file(main_file, f"import 'package:{project_name}/src/data/datasources/{name_underlined}/{name_underlined}_remote_datasource.dart';"): 
        insert_strings_to_file_before(main_file, f'''import 'package:{project_name}/src/data/datasources/{name_underlined}/{name_underlined}_remote_datasource.dart';\n''', "Future<void> main() async {")
    
    if not exist_line_in_file(main_file, f"import 'package:{project_name}/src/data/repositories/{name_underlined}_repository.dart';"): 
        insert_strings_to_file_before(main_file, f'''import 'package:{project_name}/src/data/repositories/{name_underlined}_repository.dart';\n''', "Future<void> main() async {")

    if not exist_line_in_file(main_file, f"import 'package:{project_name}/src/domain/irepositories/{name_underlined}_irepository.dart';"): 
        insert_strings_to_file_before(main_file, f'''import 'package:{project_name}/src/domain/irepositories/{name_underlined}_irepository.dart';\n''', "Future<void> main() async {")

    
    change_directory(project_directory)
    # pub get
    command = f"{flutter_command} pub get"
    pubget_success = run_command(command)
    
    if pubget_success:
        print(f"task '{task}' executed successfully.")
    else:
        print(f"Error: task '{task}' failed.")


elif task=="11":
    import tkinter as tk

    def do_process():
        """
        """
        requestJson = requestText.get('1.0', tk.END)
        responseJson = responseText.get('1.0', tk.END)
        folder_path = folder_path_entry.get().lower()
        entity_name = entity_name_entry.get().lower()
        # print(f"Request Json: {requestJson}")
        # print(f"Response Json: {responseJson}")

        # create request file
        loading_label = tk.Label(window, text="Loading...", font=("Arial", 12, "bold"))
        loading_label.pack()
        window.update_idletasks()

        entity_name_underlined = entity_name.replace(" ", "_")
        entity_name_titlecased= entity_name.title().replace(" ", "")
        entity_name_variablecased= entity_name_titlecased[0].lower()+entity_name_titlecased[1:]

        if entity_var.get()==1:
            generate_class_from_json(requestJson,project_directory,f"lib/src/domain/entities/{folder_path}",f"{entity_name_underlined}_request_entity","dart")
            generate_class_from_json(responseJson,project_directory,f"lib/src/domain/entities/{folder_path}",f"{entity_name_underlined}_response_entity","dart")
        
        if model_var.get()==1:
            request_dart_file = generate_class_from_json(requestJson,project_directory,f"lib/src/data/models/{folder_path}",f"{entity_name_underlined}_request_model","dart")
            response_dart_file = generate_class_from_json(responseJson,project_directory,f"lib/src/data/models/{folder_path}",f"{entity_name_underlined}_response_model","dart")

            if entity_var.get()==1:
                project_name = get_project_name(project_directory)
                insert_strings_to_file_before(request_dart_file, '''    static {{name}}RequestModel fromEntity({{name}}RequestEntity request) {return {{name}}RequestModel();}''',f"factory {entity_name_titlecased}RequestModel.fromJson")
                replace_in_file(request_dart_file, "{{name}}", entity_name_titlecased)
                insert_strings_to_file_before(request_dart_file, f"import 'package:{project_name}/src/domain/entities/{folder_path}/{entity_name_underlined}_request_entity.dart';\n",f"{entity_name_titlecased}RequestModel {entity_name_variablecased}RequestModelFromJson")
                
                insert_strings_to_file_before(response_dart_file, '''   {{name}}ResponseEntity toEntity() {return {{name}}ResponseEntity();}''',f"factory {entity_name_titlecased}ResponseModel.fromJson")
                replace_in_file(response_dart_file, "{{name}}", entity_name_titlecased)
                insert_strings_to_file_before(response_dart_file, f"import 'package:{project_name}/src/domain/entities/{folder_path}/{entity_name_underlined}_response_entity.dart';\n",f"{entity_name_titlecased}ResponseModel {entity_name_variablecased}ResponseModelFromJson")
            
        # pub get
        change_directory(project_directory)
        command = f"{flutter_command} pub get"
        pubget_success = run_command(command)
        
        if pubget_success:
            print(f"task '{task}' executed successfully.")
        else:
            print(f"Error: task '{task}' failed.")
        
        loading_label.pack_forget()
        window.quit()


    print("11. create new model and/or entity")
    project_directory = input_directorypath("input project directory")
    print(f"project_directory : {project_directory}")
    print(f"flutter_generator_dir : {flutter_generator_dir}")

    # Create the main window
    window = tk.Tk()
    window.title("Request - Response Json")

    window.wm_attributes('-topmost', True)  # Set the dialog to be always on top

    # Handle the "X" button click (WM_DELETE_WINDOW event)
    def on_closing():
        if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
            window.destroy()  # Close the window
            exit()  # Exit the program

    window.protocol("WM_DELETE_WINDOW", on_closing)

    # Create labels for entry fields
    label1 = tk.Label(window, text="Request Json:")
    label1.pack(expand=True)

    # Create entry fields for user input
    requestText = tk.Text(window, width=100, height=15)
    requestText.pack(expand=True)

    label2 = tk.Label(window, text="Response Json:")
    label2.pack()

    responseText = tk.Text(window, width=100, height=15)
    responseText.pack()

    label3 = tk.Label(window, text="folder path (inside entities/models): ")
    label3.pack()

    folder_path_entry = tk.Entry(window)
    folder_path_entry.pack()

    label4 = tk.Label(window, text="entity/model name: ")
    label4.pack()

    entity_name_entry = tk.Entry(window)
    entity_name_entry.pack()

    panel_checkbox = tk.Frame(window)
    panel_checkbox.pack()
    
    entity_var = tk.IntVar(panel_checkbox, value=1)
    model_var = tk.IntVar(panel_checkbox, value=0)

    label_entity = tk.Label(panel_checkbox, text="entity ")
    label_entity.pack(side="left")

    entity_checkbox = tk.Checkbutton(panel_checkbox, variable=entity_var)
    entity_checkbox.pack(side="left")

    label_model = tk.Label(panel_checkbox, text="model ")
    label_model.pack(side="left")

    model_checkbox = tk.Checkbutton(panel_checkbox, variable=model_var)
    model_checkbox.pack(side="left")

    # Create a button to trigger input retrieval
    button = tk.Button(window, text="Generate all", command=do_process)
    button.pack()

    # Run the main loop to display the GUI
    window.mainloop()
    
else:
    print("Thanks for using flutter generator")
    print("managed by ahsailabs")
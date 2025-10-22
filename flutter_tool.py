import os

from ascommonlib import EntryWithDialog, append_to_file, change_directory, choose_file, copy_file, create_new_file, exist_line_in_file, generate_class_from_json, get_line_in_file, input_directorypath, input_filepath, insert_strings_to_file_after, insert_strings_to_file_before, prepend_to_file, read_file, remove_all_after, remove_all_before, remove_line_contains, remove_multiline_strings, replace_in_file_multiline_string, replace_in_file_singleline_string, run_command

print("Welcome in flutter tool: ")
print("1. create flutter project")
print("2. init folder lib with clean architecture")
print("3. activate launcher icon")
print("4. activate native splash")
print("5. add flutter alcore")
print("6. add DI")
print("7. add app preference")
print("8. add api package")
print("9. add local database package")
print("10. create new repository and datasource")
print("11. create new entity and/or model")
print("12. create usecase")
print("13. activate gorouter + firebase auth")
print("14. enable path url for web")
print("15. change application name")
print("16. change package name or application id")
print("press enter to exit")

task = input("What do you want (1 or 2): ")


script_directory = os.path.dirname(__file__)
flutter_generator_dir = os.path.join(script_directory,"flutter_generator")

if task != "":
    flutter_command = input("input flutter command (fvm flutter/flutter, default flutter): ")
    if len(flutter_command)==0:
        flutter_command = "flutter"

    dart_command = input("input dart command (fvm dart/dart, default dart): ")
    if len(dart_command)==0:
        dart_command = "dart"

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
    
    copy_file(launcher_filepath, launcher_filepath_local)


    pubspec_yaml = os.path.join(project_directory, "pubspec.yaml")
    launcher_config_content = read_file(os.path.join(flutter_generator_dir, "launcher_icons_config.yaml"))

    background_color = input("input background color (#RRGGBB): ")
    theme_color = input("input theme color (#RRGGBB): ")

    launcher_config_content = launcher_config_content.replace("{{icon_asset_path}}", f"{asset_dir_name}/{launcher_icon_filename}").replace("{{background_color}}", background_color).replace("{{theme_color}}", theme_color)
    append_to_file(pubspec_yaml, launcher_config_content)

    command = f"{dart_command} run flutter_launcher_icons"
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
    
    copy_file(splash_filepath, splash_filepath_local)


    pubspec_yaml = os.path.join(project_directory, "pubspec.yaml")
    splash_config_content = read_file(os.path.join(flutter_generator_dir, "native_splash_config.yaml"))

    background_color = input("input background color (#RRGGBB): ")
    
    splash_config_content = splash_config_content.replace("{{splash_asset_path}}", f"{asset_dir_name}/{splash_icon_filename}").replace("{{background_color}}", background_color)
    append_to_file(pubspec_yaml, splash_config_content)

    command = f"{dart_command} run flutter_native_splash:create"
    run_command(command)

def get_project_name(project_directory):
    pubspec_yaml_file = os.path.join(project_directory, "pubspec.yaml")
    line_1_pubspec = get_line_in_file(pubspec_yaml_file, 1)
    project_name = line_1_pubspec.split(": ")[1].strip()
    return project_name


def generateEntityAndModel(project_directory, requestJson,responseJson, folder_path, entity_name, is_create_entity,  is_create_model):
    print("="*20)
    print("json data before: "+requestJson)
    print("="*20)

    if len(requestJson) == 0:
        requestJson = "{}"
    if len(responseJson) == 0:
        responseJson = "{}"

    print("="*20)
    print("json data after: "+requestJson)
    print("="*20)
    # print(f"Request Json: {requestJson}")
    # print(f"Response Json: {responseJson}")

    # create request file

    entity_name_underlined = entity_name.replace(" ", "_")
    entity_name_titlecased= entity_name.title().replace(" ", "")
    entity_name_variablecased= entity_name_titlecased[0].lower()+entity_name_titlecased[1:]

    if is_create_entity:
        generate_class_from_json(requestJson,project_directory,f"lib/app/domain/entities/{folder_path}",f"{entity_name_underlined}_request_entity","dart",f"{entity_name_titlecased}RequestEntity")
        generate_class_from_json(responseJson,project_directory,f"lib/app/domain/entities/{folder_path}",f"{entity_name_underlined}_response_entity","dart",f"{entity_name_titlecased}ResponseEntity")
    
    if is_create_model:
        request_dart_file = generate_class_from_json(requestJson,project_directory,f"lib/app/data/models/{folder_path}",f"{entity_name_underlined}_request_model","dart",f"{entity_name_titlecased}RequestModel")
        response_dart_file = generate_class_from_json(responseJson,project_directory,f"lib/app/data/models/{folder_path}",f"{entity_name_underlined}_response_model","dart",f"{entity_name_titlecased}ResponseModel")

        if is_create_entity:
            project_name = get_project_name(project_directory)
            insert_strings_to_file_before(request_dart_file, '''    static {{name}}RequestModel fromEntity({{name}}RequestEntity request) {return {{name}}RequestModel.fromJson(request.toJson());}''',f"factory {entity_name_titlecased}RequestModel.fromJson")
            replace_in_file_singleline_string(request_dart_file, "{{name}}", entity_name_titlecased)
            insert_strings_to_file_before(request_dart_file, f"import 'package:{project_name}/app/domain/entities/{folder_path}/{entity_name_underlined}_request_entity.dart';\n",f"{entity_name_titlecased}RequestModel {entity_name_variablecased}RequestModelFromJson")
            
            insert_strings_to_file_before(response_dart_file, '''   {{name}}ResponseEntity toEntity() {return {{name}}ResponseEntity.fromJson(toJson());}''',f"factory {entity_name_titlecased}ResponseModel.fromJson")
            replace_in_file_singleline_string(response_dart_file, "{{name}}", entity_name_titlecased)
            insert_strings_to_file_before(response_dart_file, f"import 'package:{project_name}/app/domain/entities/{folder_path}/{entity_name_underlined}_response_entity.dart';\n",f"{entity_name_titlecased}ResponseModel {entity_name_variablecased}ResponseModelFromJson")
        

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
    os.makedirs("lib/app", exist_ok=True)
    copy_file("lib/main.dart", "lib/app/app.dart")
    main_file = os.path.join(project_root_directory, "lib/main.dart")
    app_file = os.path.join(project_root_directory, "lib/app/app.dart")
    remove_all_before(app_file, "class MyApp extends StatelessWidget {")
    remove_all_after(main_file, "class MyApp extends StatelessWidget {",include_keyword=True)
    prepend_to_file(app_file, "import 'package:flutter/material.dart';\n")
    prepend_to_file(main_file, f"import 'package:{project_name}/app/app.dart';")
    
    test_file = os.path.join(project_root_directory, "test/widget_test.dart")
    replace_in_file_singleline_string(test_file,f"import 'package:{project_name}/main.dart';",f"import 'package:{project_name}/app/app.dart';\n")

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
        "lib/app",
        "lib/app/presentation", 
        "lib/app/domain",
        "lib/app/data",
        "lib/app/presentation/pages",
        "lib/app/presentation/widgets",
        "lib/app/domain/usecases",
        "lib/app/domain/entities",
        "lib/app/domain/irepositories",
        "lib/app/data/repositories",
        "lib/app/data/datasources",
        "lib/app/data/providers",
        "lib/app/data/providers/api",
        "lib/app/data/providers/database",
        "lib/app/data/providers/preference",
        "lib/app/data/models",
        "lib/app/shared",
        "lib/app/shared/utils",
        "lib/app/shared/configs",
        "lib/app/shared/extensions",
        
    ]

    # Create folders within the project
    for folder in folders:
        full_path = os.path.join(project_dir, folder)
        os.makedirs(full_path, exist_ok=True)

    # copy some files
    copy_file(os.path.join(flutter_generator_dir,"general_usecase.dart.txt"), os.path.join(project_dir, "lib/app/domain/usecases/general_usecase.dart"))

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
  inject.registerLazySingleton(() => SerialANumberRemoteDatasource(inject()));
  inject.registerLazySingleton<ISerialNumberRepository>(() => SerialANumberRepository(inject()));
  inject.registerFactory(() => CheckAppAUpdateUseCase(inject()));
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

    replace_in_file_singleline_string(main_file, "void main() {", "Future<void> main() async {")
    replace_in_file_singleline_string(main_file, "void main() async {", "Future<void> main() async {")

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
    preference_dir = os.path.join(project_directory, "lib/app/data/providers/preference")
    os.makedirs(preference_dir, exist_ok=True)
    copy_file(os.path.join(flutter_generator_dir,"app_preference.dart.txt"), os.path.join(project_directory, "lib/app/data/providers/preference/app_preference.dart"))
    
    main_file = os.path.join(project_directory, "lib/main.dart")
    if not exist_line_in_file(main_file, "  inject.registerLazySingletonAsync<AppPreference>("):    
        insert_strings_to_file_before(main_file, '''  //app preferences
  inject.registerLazySingletonAsync<AppPreference>(() => AppPreference().initialize());\n\n''', "inject.registerLazySingleton(() => Logger());")

    project_name = get_project_name(project_directory)

    if not exist_line_in_file(main_file, f"import 'package:{project_name}/app/data/providers/preference/app_preference.dart';"):
        insert_strings_to_file_before(main_file, f'''import 'package:{project_name}/app/data/providers/preference/app_preference.dart';\n\n''', "Future<void> main() async {")

    # add dependecy
    change_directory(project_directory)
    command = f"{flutter_command} pub add shared_preferences flutter_secure_storage encrypt"
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


    api_dir = os.path.join(project_directory, "lib/app/data/providers/api")
    env_dir = os.path.join(project_directory, "lib/env")
    # copy some files
    os.makedirs(api_dir, exist_ok=True)
    copy_file(os.path.join(flutter_generator_dir,"api_client.dio.dart.txt"), os.path.join(project_directory, "lib/app/data/providers/api/api_client.dart"))
    copy_file(os.path.join(flutter_generator_dir,"api_endpoint.dart.txt"), os.path.join(project_directory, "lib/app/data/providers/api/api_endpoint.dart"))
    copy_file(os.path.join(flutter_generator_dir,"api_exception.dio.dart.txt"), os.path.join(project_directory, "lib/app/data/providers/api/api_exception.dart"))
    os.makedirs(env_dir, exist_ok=True)
    copy_file(os.path.join(flutter_generator_dir,"env.dart.txt"), os.path.join(project_directory, "lib/env/env.dart"))
    copy_file(os.path.join(flutter_generator_dir,".env.txt"), os.path.join(project_directory, ".env"))
    

    change_directory(project_directory)

    # add deps
    command = f"{flutter_command} pub add dio package_info_plus pretty_dio_logger envied dev:envied_generator dev:build_runner"
    run_command(command)
    
   
    api_client_file = os.path.join(project_directory, "lib/app/data/providers/api/api_client.dart")
    api_endpoint_file = os.path.join(project_directory, "lib/app/data/providers/api/api_endpoint.dart")
    pubspec_yaml_file = os.path.join(project_directory, "pubspec.yaml")
    
    # replace content some files
    
    project_name = get_project_name(project_directory)
    replace_in_file_singleline_string(api_client_file,"{{project_name}}", project_name)
    replace_in_file_singleline_string(api_endpoint_file,"{{project_name}}", project_name)

    main_file = os.path.join(project_directory, "lib/main.dart")
    if not exist_line_in_file(main_file, "inject.registerSingleton<ApiClient>"):
        insert_strings_to_file_before(main_file, '''  //api client
  final apiClient = ApiClient();
  await apiClient.initialize();
  inject.registerSingleton<ApiClient>(apiClient);\n''', "inject.registerLazySingleton(() => Logger());")

    if not exist_line_in_file(main_file, f"import 'package:{project_name}/app/data/providers/api/api_client.dart';"): 
        insert_strings_to_file_before(main_file, f'''import 'package:{project_name}/app/data/providers/api/api_client.dart';\n''', "Future<void> main() async {")
    
    
    # build runner
    command = f"{dart_command} run build_runner build"
    build_success = run_command(command)

    # pub get
    command = f"{flutter_command} pub get"
    pubget_success = run_command(command)
    if build_success and pubget_success:
        print(f"task '{task}' executed successfully.")
    else:
        print(f"Error: task '{task}' failed.")
elif task=="9":
    print("9. add local database package")
    project_directory = input_directorypath("input project directory")
    print(f"project_directory : {project_directory}")
    print(f"flutter_generator_dir : {flutter_generator_dir}")


    database_dir = os.path.join(project_directory, "lib/app/data/providers/database")
    # copy some files
    os.makedirs(database_dir, exist_ok=True)
    copy_file(os.path.join(flutter_generator_dir,"drift_provider.dart.txt"), os.path.join(project_directory, "lib/app/data/providers/database/drift_provider.dart"))
    

    change_directory(project_directory)
    project_name = get_project_name(project_directory)

    # add deps
    command = f"{flutter_command} pub add drift path path_provider sqlite3_flutter_libs dev:drift_dev dev:build_runner"
    run_command(command)
    
    
    pubspec_yaml_file = os.path.join(project_directory, "pubspec.yaml")

    main_file = os.path.join(project_directory, "lib/main.dart")
 
    if not exist_line_in_file(main_file, "inject.registerLazySingleton<DriftProvider>("):
        insert_strings_to_file_before(main_file, '''  inject.registerLazySingleton<DriftProvider>(() => DriftProvider());\n\n''', "inject.registerLazySingleton(() => Logger());")
    

    if not exist_line_in_file(main_file, f"import 'package:{project_name}/app/data/providers/database/drift_provider.dart';"): 
        insert_strings_to_file_before(main_file, f'''import 'package:{project_name}/app/data/providers/database/drift_provider.dart';\n''', "Future<void> main() async {")
   

    
    # build runner
    command = f"{dart_command} run build_runner build"
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
    irepos_dir = os.path.join(project_directory, "lib/app/domain/irepositories")
    os.makedirs(irepos_dir, exist_ok=True)
    usecases_dir = os.path.join(project_directory, f"lib/app/domain/usecases/{name_underlined}")
    os.makedirs(usecases_dir, exist_ok=True)
    entities_dir = os.path.join(project_directory, f"lib/app/domain/entities/{name_underlined}")
    os.makedirs(entities_dir, exist_ok=True)

    repos_dir = os.path.join(project_directory, "lib/app/data/repositories")
    os.makedirs(repos_dir, exist_ok=True)
    datasources_dir = os.path.join(project_directory, f"lib/app/data/datasources/{name_underlined}")
    os.makedirs(datasources_dir, exist_ok=True)
    models_dir = os.path.join(project_directory, f"lib/app/data/models/{name_underlined}")
    os.makedirs(models_dir, exist_ok=True)

    utils_dir = os.path.join(project_directory, "lib/app/shared/utils")
    os.makedirs(utils_dir, exist_ok=True)

    widget_util_file = os.path.join(utils_dir, "widget_util.dart")
    is_internet_connected_function = '''Future<bool> isInternetConnected() async {
  bool isDeviceConnected = false;
  final connectionStatus = await Connectivity().checkConnectivity();
  if (connectionStatus != ConnectivityResult.none) {
    isDeviceConnected = await InternetConnectionChecker().hasConnection;
  }
  return isDeviceConnected;
}
'''
    if os.path.exists(widget_util_file):
        if not exist_line_in_file(widget_util_file,"Future<bool> isInternetConnected() async {"):
            append_to_file(widget_util_file, is_internet_connected_function)
    else:
        create_new_file(widget_util_file, is_internet_connected_function)

    if not exist_line_in_file(widget_util_file, "import 'package:connectivity_plus/connectivity_plus.dart';"): 
        prepend_to_file(widget_util_file, '''import 'package:connectivity_plus/connectivity_plus.dart';''')
    if not exist_line_in_file(widget_util_file, "import 'package:internet_connection_checker/internet_connection_checker.dart';"): 
        prepend_to_file(widget_util_file, '''import 'package:internet_connection_checker/internet_connection_checker.dart';''')


    # copy some files
    copy_file(os.path.join(flutter_generator_dir,"name_irepository.dart.txt"), os.path.join(irepos_dir, f"{name_underlined}_irepository.dart"))
    copy_file(os.path.join(flutter_generator_dir,"name_repository.dart.txt"), os.path.join(repos_dir, f"{name_underlined}_repository.dart"))
    copy_file(os.path.join(flutter_generator_dir,"name_local_datasource.dart.txt"), os.path.join(datasources_dir, f"{name_underlined}_local_datasource.dart"))
    copy_file(os.path.join(flutter_generator_dir,"name_remote_datasource.dart.txt"), os.path.join(datasources_dir, f"{name_underlined}_remote_datasource.dart"))

    project_name = get_project_name(project_directory)

    irepo_file = os.path.join(irepos_dir, f"{name_underlined}_irepository.dart")
    replace_in_file_singleline_string(irepo_file,"{{name_titlecased}}", name_titlecased)

    repo_file = os.path.join(repos_dir, f"{name_underlined}_repository.dart")
    replace_in_file_singleline_string(repo_file,"{{project_name}}", project_name)
    replace_in_file_singleline_string(repo_file,"{{name_titlecased}}", name_titlecased)
    replace_in_file_singleline_string(repo_file,"{{name_variablecased}}", name_variablecased)
    replace_in_file_singleline_string(repo_file,"{{name_underlined}}", name_underlined)

    local_datasource_file = os.path.join(datasources_dir, f"{name_underlined}_local_datasource.dart")
    replace_in_file_singleline_string(local_datasource_file,"{{project_name}}", project_name)
    replace_in_file_singleline_string(local_datasource_file,"{{name_titlecased}}", name_titlecased)

    remote_datasource_file = os.path.join(datasources_dir, f"{name_underlined}_remote_datasource.dart")
    replace_in_file_singleline_string(remote_datasource_file,"{{project_name}}", project_name)
    replace_in_file_singleline_string(remote_datasource_file,"{{name_titlecased}}", name_titlecased)


    main_file = os.path.join(project_directory, "lib/main.dart")
 
    if not exist_line_in_file(main_file, f"  inject.registerLazySingleton(() => {name_titlecased}LocalDatasource(inject()));"):
        insert_strings_to_file_before(main_file, f'''  inject.registerLazySingleton(() => {name_titlecased}LocalDatasource(inject()));\n\n''', "  //DO NOT REMOVE/CHANGE THIS : REGISTER DI")
    if not exist_line_in_file(main_file, f"  inject.registerLazySingleton(() => {name_titlecased}RemoteDatasource(inject()));"):
        insert_strings_to_file_before(main_file, f'''  inject.registerLazySingleton(() => {name_titlecased}RemoteDatasource(inject()));\n\n''', "  //DO NOT REMOVE/CHANGE THIS : REGISTER DI")
    if not exist_line_in_file(main_file, f"  inject.registerLazySingleton<I{name_titlecased}Repository>(() => {name_titlecased}Repository(inject()));"):
        insert_strings_to_file_before(main_file, f'''  inject.registerLazySingleton<I{name_titlecased}Repository>(() => {name_titlecased}Repository(inject(),inject()));\n\n''', "  //DO NOT REMOVE/CHANGE THIS : REGISTER DI")
    

    if not exist_line_in_file(main_file, f"import 'package:{project_name}/app/data/datasources/{name_underlined}/{name_underlined}_local_datasource.dart';"): 
        insert_strings_to_file_before(main_file, f'''import 'package:{project_name}/app/data/datasources/{name_underlined}/{name_underlined}_local_datasource.dart';\n''', "Future<void> main() async {")
   
    if not exist_line_in_file(main_file, f"import 'package:{project_name}/app/data/datasources/{name_underlined}/{name_underlined}_remote_datasource.dart';"): 
        insert_strings_to_file_before(main_file, f'''import 'package:{project_name}/app/data/datasources/{name_underlined}/{name_underlined}_remote_datasource.dart';\n''', "Future<void> main() async {")
    
    if not exist_line_in_file(main_file, f"import 'package:{project_name}/app/data/repositories/{name_underlined}_repository.dart';"): 
        insert_strings_to_file_before(main_file, f'''import 'package:{project_name}/app/data/repositories/{name_underlined}_repository.dart';\n''', "Future<void> main() async {")

    if not exist_line_in_file(main_file, f"import 'package:{project_name}/app/domain/irepositories/{name_underlined}_irepository.dart';"): 
        insert_strings_to_file_before(main_file, f'''import 'package:{project_name}/app/domain/irepositories/{name_underlined}_irepository.dart';\n''', "Future<void> main() async {")

    
    change_directory(project_directory)

    # add deps
    command = f"{flutter_command} pub add connectivity_plus internet_connection_checker"
    run_command(command)

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
        requestJson = requestText.get('1.0', tk.END).strip()
        responseJson = responseText.get('1.0', tk.END).strip()
        folder_path = folder_path_entry.get().lower()
        entity_name = entity_name_entry.get().lower()
        
        loading_label = tk.Label(window, text="Loading...", font=("Arial", 12, "bold"))
        loading_label.pack()
        window.update_idletasks()
            
        generateEntityAndModel(project_directory, requestJson, responseJson, folder_path, entity_name, entity_var.get()==1, model_var.get()==1)
        
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

    print("11. create new entity and/or model")
    project_directory = input_directorypath("input project directory")
    print(f"project_directory : {project_directory}")
    print(f"flutter_generator_dir : {flutter_generator_dir}")

    # Create the main window
    window = tk.Tk()
    window.title("Create entity and/or model")

    window.wm_attributes('-topmost', True)  # Set the dialog to be always on top

    # Handle the "X" button click (WM_DELETE_WINDOW event)
    def on_closing():
        if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
            window.destroy()  # Close the window
            exit()  # Exit the program

    window.protocol("WM_DELETE_WINDOW", on_closing)


    panel_main = tk.Frame(window, padx=20, pady=20)
    panel_main.pack(fill=tk.BOTH, expand=True)

    # Create labels for entry fields
    label1 = tk.Label(panel_main, text="Request Json:")
    label1.pack(expand=True)

    # Create entry fields for user input
    requestText = tk.Text(panel_main, width=40, height=7)
    requestText.pack()

    label2 = tk.Label(panel_main, text="Response Json:")
    label2.pack()

    responseText = tk.Text(panel_main, width=40, height=7)
    responseText.pack(expand=True)

    label3 = tk.Label(panel_main, text="folder path (inside entities/models): ")
    label3.pack()

    folder_path_entry = tk.Entry(panel_main)
    folder_path_entry.pack()

    label4 = tk.Label(panel_main, text="entity/model name: ")
    label4.pack()

    entity_name_entry = tk.Entry(panel_main)
    entity_name_entry.pack()

    panel_checkbox = tk.Frame(panel_main)
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
    button = tk.Button(panel_main, text="Generate all", command=do_process)
    button.pack()

    # Run the main loop to display the GUI
    window.mainloop()
elif task=="12":
    import tkinter as tk

    def do_process():
        """
        """
        usecase_path = usecase_folder_path_entry.get()
        usecase_name = usecase_name_entry.get().lower()
        
        usecase_name_underlined = usecase_name.replace(" ", "_")
        usecase_name_class = usecase_name.title().replace(" ", "")
        usecase_name_var = usecase_name_class[0].lower()+usecase_name_class[1:]

       
        loading_label = tk.Label(window, text="Loading...", font=("Arial", 12, "bold"))
        loading_label.pack()
        window.update_idletasks()

        project_name = get_project_name(project_directory)

        usecase_file_dir =  os.path.join(usecase_dir,usecase_path)
        os.makedirs(usecase_file_dir, exist_ok=True)
        usecase_file = os.path.join(usecase_file_dir,usecase_name.replace(" ", "_")+"_usecase.dart")

        if use_repo_selected_option.get()=="userepodatasource":
            # use repo/datasource
            
            datasource_filepath = datasource_text.get()
            datasource_path_to_filename = datasource_filepath.split("/lib/app/data/datasources/")[1].replace("_remote_datasource.dart", "")
            datasource_path_to_filename_array = datasource_path_to_filename.split("/")
            datasource_name = datasource_path_to_filename_array[-1].replace("_", " ")
            datasource_path_to_filename_array.pop()
            datasource_folder_path = "/".join(datasource_path_to_filename_array)

            irepo_filepath = os.path.join(project_directory, f"lib/app/domain/irepositories/{datasource_name.replace(' ','_')}_irepository.dart")

            entity_name = "" # app online
            entity_folder_path = "" #path/to/folder
            
            if request_entity_selected_option.get()=="request_entity_create_new":
                requestJson = request_entity_option1_text.get('1.0', tk.END).strip()
                responseJson = response_entity_option1_text.get('1.0', tk.END).strip()
                entity_folder_path = entity_folder_path_entry.get().lower()
                entity_name = entity_name_entry.get().lower()

                generateEntityAndModel(project_directory, requestJson, responseJson, entity_folder_path, entity_name, True, True)
            else:
                full_request_entity_path = request_entity_option2_text.get()
                path_to_file_request_entity = full_request_entity_path.split("/lib/app/domain/entities/")[1]
                path_to_file_request_entity = path_to_file_request_entity.replace("_request_entity.dart", "").replace("_response_entity.dart", "")
                request_entity_path_array = path_to_file_request_entity.split("/")
                entity_name = request_entity_path_array[-1].replace("_", " ")
                request_entity_path_array.pop() # remove last element (entity name)
                entity_folder_path = "/".join(request_entity_path_array)

            
            datasource_name_class = datasource_name.title().replace(" ", "")
            datasource_name_var = datasource_name_class[0].lower()+datasource_name_class[1:]

            entity_name_class = entity_name.title().replace(" ", "")
            entity_name_var = entity_name_class[0].lower()+entity_name_class[1:]

            # generate usecase
            copy_file(os.path.join(flutter_generator_dir,"repo_usecase.dart.txt"),usecase_file)
            replace_in_file_singleline_string(usecase_file, "{{project_name}}", project_name)
            replace_in_file_singleline_string(usecase_file, "{{usecase_name_class}}", usecase_name_class)
            replace_in_file_singleline_string(usecase_file, "{{usecase_name_var}}", usecase_name_var)

            replace_in_file_singleline_string(usecase_file, "{{entity_folder}}", entity_folder_path)
            replace_in_file_singleline_string(usecase_file, "{{repo_name}}", datasource_name.replace(" ", "_"))
            replace_in_file_singleline_string(usecase_file, "{{entity_name_class}}",entity_name_class)
            replace_in_file_singleline_string(usecase_file, "{{entity_name}}", entity_name.replace(" ", "_"))
            replace_in_file_singleline_string(usecase_file, "{{repo_name_class}}", datasource_name_class)
            replace_in_file_singleline_string(usecase_file, "{{repo_name_var}}", datasource_name_var)

            entity_name_file = entity_name.replace(" ", "_")

            # update irepo
            insert_strings_to_file_before(irepo_filepath, f'''Future<{entity_name_class}ResponseEntity> {usecase_name_var}({entity_name_class}RequestEntity request);\n''', "  //DO NOT REMOVE/CHANGE THIS : IREPOSITORY")
            
            import_request_entity = f'''import 'package:{project_name}/app/domain/entities/{entity_folder_path}/{entity_name_file}_request_entity.dart';'''
            import_response_entity = f'''import 'package:{project_name}/app/domain/entities/{entity_folder_path}/{entity_name_file}_response_entity.dart';\n'''
            import_request_model = f'''import 'package:{project_name}/app/data/models/{entity_folder_path}/{entity_name_file}_request_model.dart';'''
            import_response_model = f'''import 'package:{project_name}/app/data/models/{entity_folder_path}/{entity_name_file}_response_model.dart';\n'''

            if not exist_line_in_file(irepo_filepath, import_request_entity): 
                insert_strings_to_file_before(irepo_filepath, import_request_entity, f"abstract class I{datasource_name_class}Repository")
            if not exist_line_in_file(irepo_filepath, import_response_entity): 
                insert_strings_to_file_before(irepo_filepath, import_response_entity, f"abstract class I{datasource_name_class}Repository")

            # update repo
            repo_filepath = os.path.join(project_directory, f"lib/app/data/repositories/{datasource_name.replace(' ', '_')}_repository.dart")
            
            method_at_repo = '''  @override
  Future<{{entity_name_class}}ResponseEntity> {{usecase_name_var}}({{entity_name_class}}RequestEntity request) async {
    {{entity_name_class}}ResponseModel response = await {{repo_name_var}}RemoteDatasource.{{usecase_name_var}}({{entity_name_class}}RequestModel.fromEntity(request));
    return response.toEntity();
  }\n'''
            insert_strings_to_file_before(repo_filepath, method_at_repo, "  //DO NOT REMOVE/CHANGE THIS : REPOSITORY")
            replace_in_file_singleline_string(repo_filepath, "{{entity_name_class}}", entity_name_class)
            replace_in_file_singleline_string(repo_filepath, "{{usecase_name_var}}", usecase_name_var)
            replace_in_file_singleline_string(repo_filepath, "{{repo_name_var}}", datasource_name_var)

            
            if not exist_line_in_file(repo_filepath, import_request_entity): 
                insert_strings_to_file_before(repo_filepath, import_request_entity, f"class {datasource_name_class}Repository extends I{datasource_name_class}Repository")
            if not exist_line_in_file(repo_filepath, import_response_entity): 
                insert_strings_to_file_before(repo_filepath, import_response_entity, f"class {datasource_name_class}Repository extends I{datasource_name_class}Repository")
            if not exist_line_in_file(repo_filepath, import_request_model): 
                insert_strings_to_file_before(repo_filepath, import_request_model, f"class {datasource_name_class}Repository extends I{datasource_name_class}Repository")
            if not exist_line_in_file(repo_filepath, import_response_model): 
                insert_strings_to_file_before(repo_filepath, import_response_model, f"class {datasource_name_class}Repository extends I{datasource_name_class}Repository")

            # update remote datasources
            remote_datasource_filepath = os.path.join(project_directory, f"lib/app/data/datasources/{datasource_folder_path}/{datasource_name.replace(' ', '_')}_remote_datasource.dart")
            
            method_get_at_datasource = '''  Future<{{entity_name_class}}ResponseModel> {{usecase_name_var}}(
      {{entity_name_class}}RequestModel request) async {
    try {
      final response = await apiClient.get(ApiEndPoint.chekSerialNumber, queryParameters: {
        "param1": "",
      });

      return compute({{entity_name_var}}ResponseModelFromJson, response);
    } catch (e) {
      return Future.error(e);
    }
  }\n'''
            method_post_at_datasource = '''  Future<{{entity_name_class}}ResponseModel> {{usecase_name_var}}(
      {{entity_name_class}}RequestModel request) async {
    try {
      var formData = {
        'param1': "",
        'files[]': ["", ""]
            .map((file) => FileUploadData(file, null, basename(file), null))
            .toList(),
      };
      final response = await apiClient.post(ApiEndPoint.chekSerialNumber,
          data: formData, isMultipart: true);

      return compute({{entity_name_var}}ResponseModelFromJson, response);
    } catch (e) {
      return Future.error(e);
    }
  }\n'''
            method_at_remote_datasource = ""
            if(get_or_post_selected_option.get()=="get"):
                method_at_remote_datasource  = method_get_at_datasource
            else:
                method_at_remote_datasource  = method_post_at_datasource
            
            insert_strings_to_file_before(remote_datasource_filepath, method_at_remote_datasource, "  //DO NOT REMOVE/CHANGE THIS : REMOTEDATASOURCE")
            replace_in_file_singleline_string(remote_datasource_filepath, "{{entity_name_class}}", entity_name_class)
            replace_in_file_singleline_string(remote_datasource_filepath, "{{usecase_name_var}}", usecase_name_var)
            replace_in_file_singleline_string(remote_datasource_filepath, "{{entity_name_var}}", entity_name_var)

            if not exist_line_in_file(remote_datasource_filepath, import_request_model): 
                insert_strings_to_file_before(remote_datasource_filepath, import_request_model, f"class {datasource_name_class}RemoteDatasource")
            if not exist_line_in_file(remote_datasource_filepath, import_response_model): 
                insert_strings_to_file_before(remote_datasource_filepath, import_response_model, f"class {datasource_name_class}RemoteDatasource")
            if not exist_line_in_file(remote_datasource_filepath, "import 'package:flutter/foundation.dart';"): 
                insert_strings_to_file_before(remote_datasource_filepath, "import 'package:flutter/foundation.dart';", f"class {datasource_name_class}RemoteDatasource")
            if not exist_line_in_file(remote_datasource_filepath, f"import 'package:{project_name}/app/data/providers/api/api_endpoint.dart';"): 
                insert_strings_to_file_before(remote_datasource_filepath, f"import 'package:{project_name}/app/data/providers/api/api_endpoint.dart';\n", f"class {datasource_name_class}RemoteDatasource")
            
            if(get_or_post_selected_option.get()=="post"):
                if not exist_line_in_file(remote_datasource_filepath, "import 'package:path/path.dart';"): 
                    insert_strings_to_file_before(remote_datasource_filepath, "import 'package:path/path.dart';\n", f"class {datasource_name_class}RemoteDatasource")


            # update local datasources
            method_at_local_datasource = '''  Future<{{entity_name_class}}ResponseModel> getCacheOf{{usecase_name_class}}(
      {{entity_name_class}}RequestModel request) async {
    try {
      final localList = await myDatabase.select(myDatabase.dataUnits).get();
      {{entity_name_class}}ResponseModel response = {{entity_name_class}}ResponseModel();
      for (var element in localList) {
        //response.output!.add(ProjectArea1.fromJson(element.toJson()));
      }
      return response;
    } catch (e) {
      return Future.error(e);
    }
  }

  Future<int> saveCacheOf{{usecase_name_class}}(
      {{entity_name_class}}RequestModel request, {{entity_name_class}}ResponseModel response) async {
    int totalOfSuccess = 0;
    try {
      List<String> list = [];
      await myDatabase.transaction(() async {
        for (final element in list) {
          try {
            final rowId = await myDatabase.into(myDatabase.dataUnits).insert(
                DataUnitsCompanion.insert(
                    unitCode: '',
                    unitName: '',
                    model: '',
                    project: '',
                    costCenter: ''),
                mode: InsertMode.insertOrReplace);
            if (rowId > 0) {
              totalOfSuccess++;
            }
          } catch (e) {
            debugPrint(e.toString());
          }
        }
      });

      return totalOfSuccess;
    } catch (e) {
      return Future.error(e);
    }
  }\n'''
            local_datasource_filepath = os.path.join(project_directory, f"lib/app/data/datasources/{datasource_folder_path}/{datasource_name.replace(' ', '_')}_local_datasource.dart")
            insert_strings_to_file_before(local_datasource_filepath, method_at_local_datasource, "  //DO NOT REMOVE/CHANGE THIS : LOCALDATASOURCE")
            replace_in_file_singleline_string(local_datasource_filepath, "{{entity_name_class}}", entity_name_class)
            replace_in_file_singleline_string(local_datasource_filepath, "{{usecase_name_class}}", usecase_name_class)

            if not exist_line_in_file(local_datasource_filepath, "import 'package:drift/drift.dart';"): 
                insert_strings_to_file_before(local_datasource_filepath, "import 'package:drift/drift.dart';", f"class {datasource_name_class}LocalDatasource")
            if not exist_line_in_file(local_datasource_filepath, "import 'package:flutter/foundation.dart';"): 
                insert_strings_to_file_before(local_datasource_filepath, "import 'package:flutter/foundation.dart';", f"class {datasource_name_class}LocalDatasource")
            if not exist_line_in_file(local_datasource_filepath, import_request_model): 
                insert_strings_to_file_before(local_datasource_filepath, import_request_model, f"class {datasource_name_class}LocalDatasource")
            if not exist_line_in_file(local_datasource_filepath, import_response_model): 
                insert_strings_to_file_before(local_datasource_filepath, import_response_model, f"class {datasource_name_class}LocalDatasource")
            

        else:
            # without repo/datasource
            copy_file(os.path.join(flutter_generator_dir,"only_usecase.dart.txt"), usecase_file)
            replace_in_file_singleline_string(usecase_file, "{{project_name}}", project_name)
            replace_in_file_singleline_string(usecase_file, "{{name}}", usecase_name_class)
            print("")


        # insert to DI in main
        main_file = os.path.join(project_directory, "lib/main.dart")
 
        if use_repo_selected_option.get()=="userepodatasource":
            if not exist_line_in_file(main_file, f"  inject.registerFactory(() => {usecase_name_class}Usecase(inject()));"):
                insert_strings_to_file_before(main_file, f'''  inject.registerFactory(() => {usecase_name_class}Usecase(inject()));\n\n''', "  //DO NOT REMOVE/CHANGE THIS : REGISTER DI")
        else:
            if not exist_line_in_file(main_file, f"  inject.registerFactory(() => {usecase_name_class}Usecase());"):
                insert_strings_to_file_before(main_file, f'''  inject.registerFactory(() => {usecase_name_class}Usecase());\n\n''', "  //DO NOT REMOVE/CHANGE THIS : REGISTER DI")

        if not exist_line_in_file(main_file, f"import 'package:{project_name}/app/domain/usecases/{usecase_path}/{usecase_name_underlined}_usecase.dart';"):
            insert_strings_to_file_before(main_file, f'''import 'package:{project_name}/app/domain/usecases/{usecase_path}/{usecase_name_underlined}_usecase.dart';\n''', "Future<void> main() async {")
    

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

    print("12. create usecase")
    project_directory = input_directorypath("input project directory")
    print(f"project_directory : {project_directory}")
    print(f"flutter_generator_dir : {flutter_generator_dir}")

    entity_dir = os.path.join(project_directory, "lib/app/domain/entities")
    irepo_dir = os.path.join(project_directory, "lib/app/domain/irepositories")
    datasource_dir = os.path.join(project_directory, "lib/app/data/datasources")
    usecase_dir = os.path.join(project_directory, "lib/app/domain/usecases")

    # Create the main window
    window = tk.Tk()
    window.title("Create UseCase")

    window.wm_attributes('-topmost', True)  # Set the dialog to be always on top

    # Handle the "X" button click (WM_DELETE_WINDOW event)
    def on_closing():
        if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
            window.destroy()  #  Close the window
            exit()  # Exit the program

    window.protocol("WM_DELETE_WINDOW", on_closing)


    #main panel
    panel_main = tk.Frame(window, padx=20, pady=20) 
    panel_main.pack(fill="both")

    
    ## usecase panel
    panel_usecase = tk.Frame(panel_main, padx=20)
    panel_usecase.pack()


    usecase_folder_path_label = tk.Label(panel_usecase, text="folder path (inside usecases): ")
    usecase_folder_path_label.pack()

    usecase_folder_path_entry = tk.Entry(panel_usecase)
    usecase_folder_path_entry.pack()

    label_usecase = tk.Label(panel_usecase, text="usecase name: ")
    label_usecase.pack(side="left")

    usecase_name_entry = tk.Entry(panel_usecase)
    usecase_name_entry.pack(side="left", fill="x")

    ## radio repo panel
    panel_radio_repo = tk.Frame(panel_main, padx=20)
    panel_radio_repo.pack()

    use_repo_selected_option = tk.StringVar(panel_radio_repo,value="withoutrepodatasource")
    def handle_selection_use_repo(value):
        use_repo_selected_option.set(value)
        if value == "userepodatasource":
            panel_entity.pack(fill="x")
        elif value == "withoutrepodatasource":
            panel_entity.pack_forget()
        button.pack_forget()
        button.pack(pady=30)
    use_repo_option1_button = tk.Radiobutton(panel_radio_repo, text="Use Repo/Datasource", variable=use_repo_selected_option, value="userepodatasource", command=lambda: handle_selection_use_repo("userepodatasource"))
    use_repo_option2_button = tk.Radiobutton(panel_radio_repo, text="Without Repo/Datasource", variable=use_repo_selected_option, value="withoutrepodatasource", command=lambda: handle_selection_use_repo("withoutrepodatasource"))
    use_repo_option1_button.pack(side="left")
    use_repo_option2_button.pack(side="left")
    

    ## usecase panel
    panel_entity = tk.Frame(panel_main)
    panel_entity.pack_forget()


    datasource_label = tk.Label(panel_entity, text="Remote Datasource Path:")
    datasource_label.pack()

    datasource_text = EntryWithDialog(panel_entity, initialdir=datasource_dir)
    datasource_text.pack()

    panel_radio_get_or_post = tk.Frame(panel_entity, padx=20)
    panel_radio_get_or_post.pack()
    get_or_post_selected_option = tk.StringVar(panel_radio_get_or_post,value="get")
    def handle_selection_get_post(value):
        get_or_post_selected_option.set(value)
    get_or_post_option1_button = tk.Radiobutton(panel_radio_get_or_post, text="get", variable=get_or_post_selected_option, value="get", command=lambda: handle_selection_get_post("get"))
    get_or_post_option2_button = tk.Radiobutton(panel_radio_get_or_post, text="post", variable=get_or_post_selected_option, value="post", command=lambda: handle_selection_get_post("post"))
    get_or_post_option1_button.pack(side="left")
    get_or_post_option2_button.pack(side="left")


    ### radio create new or existing panel
    panel_radio_create_or_use = tk.Frame(panel_entity)
    panel_radio_create_or_use.pack()
    request_entity_selected_option = tk.StringVar(panel_radio_create_or_use,value="request_entity_use_existing")
    def handle_selection(value):
        request_entity_selected_option.set(value)
        if value == "request_entity_create_new":
            request_entity_option1_label.pack(fill="x")
            request_entity_option1_text.pack(fill="x")
            request_entity_option2_label.pack_forget()
            request_entity_option2_text.pack_forget()
            response_entity_option1_label.pack(fill="x")
            response_entity_option1_text.pack(fill="x")

            entity_folder_path_label.pack()
            entity_folder_path_entry.pack()
            entity_label.pack()
            entity_name_entry.pack()
        elif value == "request_entity_use_existing":
            request_entity_option2_label.pack(fill="x")
            request_entity_option2_text.pack(fill="x")
            request_entity_option1_label.pack_forget()
            request_entity_option1_text.pack_forget()
            response_entity_option1_label.pack_forget()
            response_entity_option1_text.pack_forget()

            entity_folder_path_label.pack_forget()
            entity_folder_path_entry.pack_forget()
            entity_label.pack_forget()
            entity_name_entry.pack_forget()
        button.pack_forget()
        button.pack(pady=30)
        

    # Radio buttons with different text and variable values
    request_entity_option1_button = tk.Radiobutton(panel_radio_create_or_use, text="Create New Entity/Model", variable=request_entity_selected_option, value="request_entity_create_new", command=lambda: handle_selection("request_entity_create_new"))
    request_entity_option2_button = tk.Radiobutton(panel_radio_create_or_use, text="Use Existing Entity/Model", variable=request_entity_selected_option, value="request_entity_use_existing", command=lambda: handle_selection("request_entity_use_existing"))
    
    # Pack the buttons to display them in the window
    request_entity_option1_button.pack(side="left")
    request_entity_option2_button.pack(side="left")

   


    request_entity_option1_label = tk.Label(panel_entity, text="Request Json:")
    request_entity_option1_label.pack_forget()

    request_entity_option1_text = tk.Text(panel_entity, width=40, height=7)
    request_entity_option1_text.pack_forget()


    request_entity_option2_label = tk.Label(panel_entity, text="Request Entity Path:")
    request_entity_option2_label.pack()

    request_entity_option2_text = EntryWithDialog(panel_entity, initialdir=entity_dir)
    request_entity_option2_text.pack()


    
    response_entity_option1_label = tk.Label(panel_entity, text="Response Json:")
    response_entity_option1_label.pack_forget()

    response_entity_option1_text = tk.Text(panel_entity, width=40, height=7)
    response_entity_option1_text.pack_forget()


    entity_folder_path_label = tk.Label(panel_entity, text="folder path (inside entities/models): ")
    entity_folder_path_label.pack_forget()

    entity_folder_path_entry = tk.Entry(panel_entity)
    entity_folder_path_entry.pack_forget()

    entity_label = tk.Label(panel_entity, text="entity/model name: ")
    entity_label.pack_forget()

    entity_name_entry = tk.Entry(panel_entity)
    entity_name_entry.pack_forget()

   

    ## model panel
    panel_request_model = tk.Frame(panel_main)
    panel_request_model.pack()

    panel_response_model = tk.Frame(panel_main)
    panel_response_model.pack()

    # Create a button to trigger input retrieval
    button = tk.Button(panel_main, text="Generate all", command=do_process)
    button.pack(pady=30)

    # Run the main loop to display the GUI
    window.mainloop()   
elif task=="13":
    print("13. activate gorouter + firebase auth")
    project_directory = input_directorypath("input project directory")
    print(f"project_directory : {project_directory}")
    print(f"flutter_generator_dir : {flutter_generator_dir}")

    change_directory(project_directory)
    command = f"{flutter_command} pub add go_router firebase_core firebase_auth firebase_ui_auth firebase_ui_oauth_google"
    run_command(command)


    app_file = os.path.join(project_directory, "lib/app/app.dart")

    replace_in_file_singleline_string(app_file,"    return MaterialApp(", "    return MaterialApp.router(")

    insert_strings_to_file_before(app_file,'''    final providers = [
      GoogleProvider(
          clientId:
              "375290265425-qpci8sha4m4vumj5lgvvuu8c5u0d3gqi.apps.googleusercontent.com"),
    ];''',"    return MaterialApp.router(")


    insert_strings_to_file_after(app_file, '''      routerConfig: GoRouter(
          initialLocation: '/',
          errorBuilder: (context, state) {
            return const InformationPage();
          },
          routes: [
            GoRoute(
              path: "/signin",
              builder: (context, state) {
                return SignInScreen(
                  providers: providers,
                  headerBuilder: (context, constraints, shrinkOffset) {
                    return const Center(child: FlutterLogo());
                  },
                  sideBuilder: (context, constraints) {
                    return const Center(child: FlutterLogo());
                  },
                  actions: [
                    AuthStateChangeAction<SignedIn>((context, state) {
                      if (state.user != null) {
                        context.go('/');
                      }
                    }),
                  ],
                );
              },
            ),
            GoRoute(
                path: "/",
                redirect: (context, state) {
                  if (FirebaseAuth.instance.currentUser == null) {
                    return '/signin';
                  }
                  return null;
                },
                builder: (context, state) {
                  return HomePage();
                },
                routes: [
                  GoRoute(
                    path: "profile",
                    builder: (context, state) {
                      return ProfileScreen(
                        providers: providers,
                        appBar: AppBar(
                          //foregroundColor: context.primaryColor,
                          forceMaterialTransparency: true,
                        ),
                        actions: [
                          SignedOutAction((context) {
                            context.go('/signin');
                          }),
                        ],
                        children: [
                          ElevatedButton(
                              onPressed: () {
                                
                              },
                              child: const Text("Application History"))
                        ],
                      );
                    },
                  ),
                ])
          ]),''',"    return MaterialApp.router(")
    

    remove_line_contains(app_file, "home: ")

     # copy some files
    change_directory(script_directory)

    information_directory = os.path.join(project_directory, "lib/app/presentation/pages/information")
    print(f"information_directory : {information_directory}")
    os.makedirs(information_directory, exist_ok=True)
    copy_file(os.path.join(flutter_generator_dir,"information_page.dart.txt"), os.path.join(information_directory, "information_page.dart"))

    homepage_directory = os.path.join(project_directory, "lib/app/presentation/pages/home")
    print(f"homepage_directory : {homepage_directory}")
    os.makedirs(homepage_directory, exist_ok=True)
    copy_file(os.path.join(flutter_generator_dir,"home_page.dart.txt"), os.path.join(homepage_directory, "home_page.dart"))

    # import 'package:firebase_auth/firebase_auth.dart';
    # import 'package:firebase_ui_auth/firebase_ui_auth.dart';
    # import 'package:firebase_ui_oauth_google/firebase_ui_oauth_google.dart';
    # import 'package:nasab/app/presentation/pages/information/information_page.dart';
    # import 'package:go_router/go_router.dart';
    # import 'package:nasab/app/presentation/pages/home/home_page.dart';

    project_name = get_project_name(project_directory)

    if not exist_line_in_file(app_file, "import 'package:firebase_auth/firebase_auth.dart';"): 
        insert_strings_to_file_before(app_file, "import 'package:firebase_auth/firebase_auth.dart';\n", "class MyApp extends State")
    if not exist_line_in_file(app_file, "import 'package:firebase_ui_auth/firebase_ui_auth.dart';"): 
        insert_strings_to_file_before(app_file, "import 'package:firebase_ui_auth/firebase_ui_auth.dart';\n", "class MyApp extends State")
    if not exist_line_in_file(app_file, "import 'package:firebase_ui_oauth_google/firebase_ui_oauth_google.dart';"): 
        insert_strings_to_file_before(app_file, "import 'package:firebase_ui_oauth_google/firebase_ui_oauth_google.dart';\n", "class MyApp extends State")
    if not exist_line_in_file(app_file, f"import 'package:{project_name}/app/presentation/pages/information/information_page.dart';"): 
        insert_strings_to_file_before(app_file, f"import 'package:{project_name}/app/presentation/pages/information/information_page.dart';\n", "class MyApp extends State")
    if not exist_line_in_file(app_file, "import 'import 'package:go_router/go_router.dart';"): 
        insert_strings_to_file_before(app_file, "import 'package:go_router/go_router.dart';\n", "class MyApp extends State")
    if not exist_line_in_file(app_file, f"import 'package:{project_name}/app/presentation/pages/home/home_page.dart';"): 
        insert_strings_to_file_before(app_file, f"import 'package:{project_name}/app/presentation/pages/home/home_page.dart';\n", "class MyApp extends State")
    


    main_file = os.path.join(project_directory, "lib/main.dart")
    if not exist_line_in_file(main_file, "Future<void> registerFirebase() async {"):
        append_to_file(main_file, '''Future<void> registerFirebase() async {
    //firebase and the children
    await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);
    }''')

    if not exist_line_in_file(main_file, "await registerFirebase();"):
        insert_strings_to_file_before(main_file, '''  await registerFirebase();\n''', "  //DO NOT REMOVE/CHANGE THIS : SETUP SERVICES")

    if not exist_line_in_file(main_file, "import 'package:firebase_core/firebase_core.dart';"): 
        insert_strings_to_file_before(main_file, "import 'package:firebase_core/firebase_core.dart';\n", "Future<void> main() async {")
    if not exist_line_in_file(main_file, f"import 'package:{project_name}/firebase_options.dart';"): 
        insert_strings_to_file_before(main_file, f"import 'package:{project_name}/firebase_options.dart';\n", "Future<void> main() async {")
    


    change_directory(project_directory)


    run_flutterfire_configure = input("run  flutterfire configure (yes/no)")

    if(run_flutterfire_configure in "yes"):
        command = f"flutterfire configure"
        run_command(command)

    command = f"{flutter_command} pub get"
    pubget_success = run_command(command)
    
    if pubget_success:
        print(f"task '{task}' executed successfully.")
    else:
        print(f"Error: task '{task}' failed.")    
elif task=="14":
    print("14. enable path url for web")
    project_directory = input_directorypath("input project directory")
    print(f"project_directory : {project_directory}")
    print(f"flutter_generator_dir : {flutter_generator_dir}")

    
    pubspec_yaml_file = os.path.join(project_directory, "pubspec.yaml")
    

    replace_in_file_multiline_string(pubspec_yaml_file,'''  flutter:
    sdk: flutter''','''  flutter:
    sdk: flutter
  flutter_web_plugins:
    sdk: flutter''')

    
    main_file = os.path.join(project_directory, "lib/main.dart")

    if not exist_line_in_file(main_file, "  usePathUrlStrategy();"): 
        insert_strings_to_file_after(main_file, "  usePathUrlStrategy();", "Future<void> main() async {")
    if not exist_line_in_file(main_file, "  usePathUrlStrategy();"): 
        insert_strings_to_file_after(main_file, "  usePathUrlStrategy();", "void main() async {")
    if not exist_line_in_file(main_file, "  usePathUrlStrategy();"): 
        insert_strings_to_file_after(main_file, "  usePathUrlStrategy();", "void main() {")

    if not exist_line_in_file(main_file, "import 'package:flutter_web_plugins/url_strategy.dart';"): 
        insert_strings_to_file_before(main_file, "import 'package:flutter_web_plugins/url_strategy.dart';\n", "Future<void> main() async {")
    if not exist_line_in_file(main_file, "import 'package:flutter_web_plugins/url_strategy.dart';"): 
        insert_strings_to_file_before(main_file, "import 'package:flutter_web_plugins/url_strategy.dart';\n", "void main() async {")
    if not exist_line_in_file(main_file, "import 'package:flutter_web_plugins/url_strategy.dart';"): 
        insert_strings_to_file_before(main_file, "import 'package:flutter_web_plugins/url_strategy.dart';\n", "void main() {")
    
    change_directory(project_directory)
    command = f"{flutter_command} pub get"
    pubget_success = run_command(command)
    
    if pubget_success:
        print(f"task '{task}' executed successfully.")
    else:
        print(f"Error: task '{task}' failed.")
elif task=="15":
    print("15. change application name")
    project_directory = input_directorypath("input project directory")
    print(f"project_directory : {project_directory}")
    print(f"flutter_generator_dir : {flutter_generator_dir}")

    new_name = input("new name : ")

    change_directory(project_directory)
    command = f"{flutter_command} pub add dev:rename_app"
    run_command(command)

    command = f"{flutter_command} pub get"
    pubget_success = run_command(command)

    command = f'{dart_command} run rename_app:main all="{new_name}"'
    run_command(command)

    print(f"task '{task}' executed successfully.")
elif task=="16":
    print("16. change package name or application id")
    project_directory = input_directorypath("input project directory")
    print(f"project_directory : {project_directory}")
    print(f"flutter_generator_dir : {flutter_generator_dir}")

    new_package_name = input("new package name : ")

    change_directory(project_directory)
    command = f"{flutter_command} pub add dev:change_app_package_name "
    run_command(command)

    command = f"{flutter_command} pub get"
    pubget_success = run_command(command)

    command = f'{dart_command} run change_app_package_name:main {new_package_name}'
    run_command(command)

    print(f"task '{task}' executed successfully.")

else:
    print("Thanks for using flutter tool")
    print("managed by ahsailabs (https://ahsai.my.id)")
#!/usr/bin/env python3

import sys
import os

from ascommonlib import create_new_file, prepend_to_file, remove_multiline_strings

if len(sys.argv) == 2:
    print("migration start")

    flutter_app_folder = sys.argv[1]

    try:
        if not os.path.exists(flutter_app_folder):
            raise Exception("folder is not exist")
        android_folder = os.path.join(flutter_app_folder, "android")
        if not os.path.exists(android_folder):
            raise Exception("android folder is not exist")
        build_gradle_file= os.path.join(android_folder, "build.gradle")
        if not os.path.exists(build_gradle_file):
            raise Exception("build.gradle is not exist")
        
        # 1. get kotlin version and agp version
        print("1. get kotlin version, agp version, google service version and crashlytics version")
        # print(build_gradle_file)
        kotlin_version = ""
        agp_version = ""
        google_service_version = ""
        crashlytics_version = ""
        with open(build_gradle_file, 'r', encoding='utf-8') as file:
            for line in file:
                # print(line)
                if "ext.kotlin_version = " in line:
                    kotlin_version=line.replace("ext.kotlin_version = ","").replace("'", "").strip()
                if "classpath 'com.android.tools.build:gradle:" in line:
                    agp_version=line.replace("classpath 'com.android.tools.build:gradle:", "").replace("'","").strip()
                if "classpath 'com.google.gms:google-services:" in line:
                    google_service_version=line.replace("classpath 'com.google.gms:google-services:", "").replace("'","").strip()
                if "classpath 'com.google.firebase:firebase-crashlytics-gradle:" in line:
                    crashlytics_version=line.replace("classpath 'com.google.firebase:firebase-crashlytics-gradle:", "").replace("'","").strip()



        print(f"kotlin : {kotlin_version}")
        print(f"agp : {agp_version}")
        print(f"google service : {google_service_version}")
        print(f"crashlytics : {crashlytics_version}")


        # 2. replace content of settings.gradle with this
        print("2. replace content of settings.gradle with this")
        settings_gradle_content: str = '''pluginManagement {
    def flutterSdkPath = {
        def properties = new Properties()
        file("local.properties").withInputStream { properties.load(it) }
        def flutterSdkPath = properties.getProperty("flutter.sdk")
        assert flutterSdkPath != null, "flutter.sdk not set in local.properties"
        return flutterSdkPath
    }()

    includeBuild("$flutterSdkPath/packages/flutter_tools/gradle")

    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}

plugins {
    id "dev.flutter.flutter-plugin-loader" version "1.0.0"
    id "com.android.application" version "{agpVersion}" apply false
    id "org.jetbrains.kotlin.android" version "{kotlinVersion}" apply false'''

        if len(google_service_version) > 0:
           settings_gradle_content += '''
    id "com.google.gms.google-services" version "{googleServiceVersion}" apply false'''

        if len(crashlytics_version) > 0:
           settings_gradle_content += '''
    id "com.google.firebase.crashlytics" version "{crashlyticsVersion}" apply false'''
           
        settings_gradle_content += '''
}

include ":app"'''
        
        settings_gradle_content = settings_gradle_content.replace("{agpVersion}", agp_version).replace("{kotlinVersion}", kotlin_version).replace("{googleServiceVersion}", google_service_version).replace("{crashlyticsVersion}", crashlytics_version)

        

        # print(settings_gradle_content)


        settings_gradle_file= os.path.join(android_folder, "settings.gradle")
        create_new_file(settings_gradle_file, settings_gradle_content)

        # 3. remove buildscript from android/build.gradle
        print("3. remove buildscript from android/build.gradle")

        with open(build_gradle_file, 'r') as read_file, open(build_gradle_file + '.bak', 'w') as write_file:
            in_removal_zone = True  # Flag to track if we're before the keyword
            for line in read_file:
                if "allprojects {" in line:
                    in_removal_zone = False  # Stop removing content after keyword
                if not in_removal_zone:
                    write_file.write(line)

        # Rename the backup file to the original filename (optional)
        import os
        os.replace(build_gradle_file + '.bak', build_gradle_file)

        # 4. modify android/app/build.gradle
        print("4. modify android/app/build.gradle")
        
        android_app_folder = os.path.join(android_folder, "app")
        
        android_app_build_gradle_file = os.path.join(android_app_folder, "build.gradle")

        remove_multiline_strings(filename=android_app_build_gradle_file, strings='''def flutterRoot = localProperties.getProperty('flutter.sdk')
if (flutterRoot == null) {
    throw new GradleException("Flutter SDK not found. Define location with flutter.sdk in the local.properties file.")
}''')
        remove_multiline_strings(filename=android_app_build_gradle_file, strings='''apply plugin: 'com.android.application\'''')
        remove_multiline_strings(filename=android_app_build_gradle_file, strings='''apply plugin: 'kotlin-android\'''')
        remove_multiline_strings(filename=android_app_build_gradle_file, strings='''apply from: "$flutterRoot/packages/flutter_tools/gradle/flutter.gradle"''')
        remove_multiline_strings(filename=android_app_build_gradle_file, strings='''implementation "org.jetbrains.kotlin:kotlin-stdlib-jdk7:$kotlin_version"''')

        if len(google_service_version) > 0:
           remove_multiline_strings(filename=android_app_build_gradle_file, strings='''apply plugin: 'com.google.gms.google-services\'''')
        if len(crashlytics_version) > 0:
           remove_multiline_strings(filename=android_app_build_gradle_file, strings='''apply plugin: 'com.google.firebase.crashlytics\'''')

        content: str = '''plugins {
     id "com.android.application"
     id "dev.flutter.flutter-gradle-plugin"
     id "org.jetbrains.kotlin.android"'''
        if len(google_service_version) > 0:
           content += '''
     id "com.google.gms.google-services"'''
        if len(crashlytics_version) > 0:
           content += '''
     id "com.google.firebase.crashlytics"'''
        content += '''
 }
'''
        prepend_to_file(android_app_build_gradle_file, content)

        
        print("migration done")

    except Exception as e:
        print(f"Error: {str(e)}")

    

    print("migration finish")
else:
    print("Usage: python migrate_to_declarative_flutter_gradle_plugin.py <flutter_app_folder>")
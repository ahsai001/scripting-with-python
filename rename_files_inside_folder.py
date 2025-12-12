#!/usr/bin/env python3

from ascommonlib import input_directorypath, rename_files


project_dir = input_directorypath("input directory want to renamed")

rename_files(project_dir)

print("Succesfully rename all files")
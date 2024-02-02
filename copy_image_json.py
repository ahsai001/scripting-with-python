import json
import os
import shutil

def copy_images(json_file, source_folder, destination_folder):
    try:
        # Open the JSON file
        with open(json_file, 'r') as f:
            datas = json.load(f)
        
        # Create the destination folder if it doesn't exist
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        # Iterate through the image file paths in the JSON data
        for data in datas:
            # Construct source and destination paths
            if data["bacaan"].count(',') > 0:
                splits = data["bacaan"].split(',')
                for item in splits:
                    source_path = os.path.join(source_folder, item)
                    destination_path = os.path.join(destination_folder, os.path.basename(item))

                    # Copy the image file to the destination folder
                    shutil.copyfile(source_path, destination_path)
                    print(f"Copied {source_path} to {destination_path}")
            else:
                source_path = os.path.join(source_folder, data["bacaan"])
                destination_path = os.path.join(destination_folder, os.path.basename(data["bacaan"]))

                # Copy the image file to the destination folder
                shutil.copyfile(source_path, destination_path)
                print(f"Copied {source_path} to {destination_path}")

        print("Image copy completed successfully.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Define paths and filenames
    json_file = "/mnt/c/Users/ahmad/Documents/git/android/dzikirharian/dzikirHarianZL/src/main/res/raw/dzikirsesudahsholat_subuh.json"  # JSON file containing image paths
    source_folder = "/mnt/c/Users/ahmad/Documents/git/android/dzikirharian/dzikirHarianZL/src/main/res/drawable-nodpi/"  # Folder containing source images
    destination_folder = "/mnt/c/Users/ahmad/Documents/git/web/dzikirsubuh/"  # Destination folder for copied images

    # Call function to copy images
    copy_images(json_file, source_folder, destination_folder)


    # Define paths and filenames
    json_file = "/mnt/c/Users/ahmad/Documents/git/android/dzikirharian/dzikirHarianZL/src/main/res/raw/dzikirsesudahsholat_maghrib.json"  # JSON file containing image paths
    source_folder = "/mnt/c/Users/ahmad/Documents/git/android/dzikirharian/dzikirHarianZL/src/main/res/drawable-nodpi/"  # Folder containing source images
    destination_folder = "/mnt/c/Users/ahmad/Documents/git/web/dzikirmaghrib/"  # Destination folder for copied images

    # Call function to copy images
    copy_images(json_file, source_folder, destination_folder)

    # Define paths and filenames
    json_file = "/mnt/c/Users/ahmad/Documents/git/android/dzikirharian/dzikirHarianZL/src/main/res/raw/dzikirsesudahsholat_dz_a_i.json"  # JSON file containing image paths
    source_folder = "/mnt/c/Users/ahmad/Documents/git/android/dzikirharian/dzikirHarianZL/src/main/res/drawable-nodpi/"  # Folder containing source images
    destination_folder = "/mnt/c/Users/ahmad/Documents/git/web/dzikirzhuhur/"  # Destination folder for copied images

    # Call function to copy images
    copy_images(json_file, source_folder, destination_folder)



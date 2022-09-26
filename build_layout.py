import os
import json

project_directories = ["Effects", "html_ui", "SimObjects", "ModelBehaviorDefs", "AirTraffic", "Texture", "scenery"]


PATH = os.path.dirname(os.path.abspath(__file__))
from glob import glob
PATH_WITH_LAYOUT = [y for x in os.walk(PATH) for y in glob(os.path.join(x[0], 'layout.json'))]
for collect_path in PATH_WITH_LAYOUT:
    content_entries = list()
    total_package_size = 0
    work_path = os.path.abspath(os.path.join(collect_path, os.pardir))
    print(work_path)
    
    for project_directory in project_directories:
        for directory_path, directory_names, file_names in os.walk(os.path.join(work_path, project_directory)):
            for file_name in file_names:
                full_file_path = os.path.join(directory_path, file_name)
                file_path = os.path.relpath(os.path.join(directory_path, file_name), start=work_path)
                #file_path = os.path.join(directory_path, file_name)
                file_size = os.path.getsize(full_file_path)
                file_date = 116444736000000000 + int(os.path.getmtime(full_file_path) * 10000000.0)
                content_entry = {"path": file_path.replace(os.sep, "/"), "size": file_size, "date": file_date}
                content_entries.append(content_entry)
                total_package_size += file_size
                print("Added file: " + file_path)

    layout_entries = {"content": content_entries}

    layout_file = open(os.path.join(work_path, "layout.json"), "w")
    json.dump(layout_entries, layout_file, indent=4)

    manifest_file = open(os.path.join(work_path, "manifest.json"), "r")

    manifest_entries = json.load(manifest_file)
    manifest_entries["total_package_size"] = str(total_package_size).zfill(20)

    manifest_file = open(os.path.join(work_path, "manifest.json"), "w")
    json.dump(manifest_entries, manifest_file, indent=4)
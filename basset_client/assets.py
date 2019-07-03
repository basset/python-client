import os

from posixpath import join

from .generate_hash import generate_file_hash

IGNORE_FILE_EXISTS = [
    '.js',
    '.map'
]


def ignore_file(file):
    ext = os.path.splitext(file)[1].strip().lower()

    return ext in IGNORE_FILE_EXISTS


def walk_assets(static_dir, relative_dir):
    directory = join(os.getcwd(), static_dir, relative_dir)
    current_path, directories, files = os.walk(directory).next()
    assets = []
    filtered_files = [file for file in files if not ignore_file(file)]
    for file in filtered_files:
        file_path = os.path.join(current_path, file)
        relative_path = join(relative_dir, file)
        sha = generate_file_hash(file_path)
        assets.append([relative_path, sha])

    for found_directory in directories:
        directory_assets = walk_assets(
            static_dir, os.path.join(relative_dir, found_directory))
        assets = assets + directory_assets

    return assets


def get_assets(static_dir, relative_dir):
    assets_list = walk_assets(static_dir, relative_dir)
    assets = {}
    for [relative_path, sha] in assets_list:
        assets[relative_path] = sha
    return assets

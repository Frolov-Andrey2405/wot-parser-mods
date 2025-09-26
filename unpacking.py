"""
This script extracts modification archives and manages files and folders after unpacking. It scans the folder with downloaded archives, extracts ZIP and RAR files,
deletes unnecessary files and folders, and organizes the extracted content into
the correct directory structure for further use.
"""

import os
import shutil
import zipfile
from typing import List

import patoolib


class ArchiveExtractor:
    """
    Class for extracting archives and managing files and folders.
    """

    def __init__(self, folder_path: str, output_folder: str):
        """
        Initialize the ArchiveExtractor object.
        """
        self.folder_path = folder_path
        self.output_folder = output_folder

    def check_folder_exists(self, folder: str) -> bool:
        """
        Check if a folder exists.
        """
        return os.path.exists(folder)

    def create_folder(self, folder: str) -> None:
        """
        Create a folder if it does not exist.
        """
        if not self.check_folder_exists(folder):
            os.makedirs(folder)

    def list_files(self, folder: str) -> List[str]:
        """
        Get a list of files in a folder.
        """
        return os.listdir(folder)

    def filter_archive_files(self, files: List[str]) -> List[str]:
        """
        Filter archive files from a list of files.
        """
        return [file for file in files if file.endswith((".zip", ".rar"))]

    def extract_archive(self, archive_path: str, output_folder: str) -> None:
        """
        Extract an archive to the specified folder.
        """
        try:
            if archive_path.endswith(".zip"):
                with zipfile.ZipFile(archive_path, "r") as zip_ref:
                    zip_ref.extractall(output_folder)
                    print(
                        f"File {os.path.basename(archive_path)} successfully extracted to {output_folder}."
                    )
            elif archive_path.endswith(".rar"):
                patoolib.extract_archive(archive_path, outdir=output_folder)
                print(
                    f"File {os.path.basename(archive_path)} successfully extracted to {output_folder}."
                )
        except (zipfile.BadZipFile, patoolib.util.PatoolError) as e:
            print(f"File {os.path.basename(archive_path)} is not a valid archive: {e}")
        except Exception as e:
            print(f"Error extracting file {os.path.basename(archive_path)}: {e}")

    def delete_files(self, files: List[str], folder: str) -> None:
        """
        Delete files from a folder.
        """
        for file_name in files:
            file_path = os.path.join(folder, file_name)
            if self.check_folder_exists(file_path):
                os.remove(file_path)
                print(f"File {file_name} successfully deleted.")

    def delete_folders(self, folders: List[str], folder: str) -> None:
        """
        Delete folders from a folder.
        """
        for folder_name in folders:
            folder_path = os.path.join(folder, folder_name)
            if self.check_folder_exists(folder_path):
                shutil.rmtree(folder_path)
                print(f"Folder {folder_name} successfully deleted.")

    def move_folders(
        self, folders: List[str], source_folder: str, target_folder: str
    ) -> None:
        """
        Move folders from one folder to another.
        """
        self.create_folder(target_folder)
        for folder_name in folders:
            source_path = os.path.join(source_folder, folder_name)
            target_path = os.path.join(target_folder, folder_name)
            if self.check_folder_exists(source_path):
                if self.check_folder_exists(target_path):
                    for item in self.list_files(source_path):
                        s = os.path.join(source_path, item)
                        d = os.path.join(target_path, item)
                        if os.path.isdir(s):
                            shutil.copytree(s, d, dirs_exist_ok=True)
                        else:
                            shutil.copy2(s, d)
                    shutil.rmtree(source_path)
                else:
                    shutil.move(source_path, target_folder)
                print(f"Folder {folder_name} successfully moved to {target_folder}.")

    def move_file(self, file_name: str, source_folder: str, target_folder: str) -> None:
        """
        Move a file from one folder to another.
        """
        self.create_folder(target_folder)
        file_path = os.path.join(source_folder, file_name)
        if self.check_folder_exists(file_path):
            shutil.move(file_path, target_folder)
            print(f"File {file_name} successfully moved to {target_folder}.")

    def process_wg_folder(self, wg_folder: str) -> None:
        """
        If a 'WG' folder exists, move its 'res_mods' or 'mods' subfolders to the output folder and process them.
        """
        wg_path = os.path.join(self.output_folder, wg_folder)
        if not self.check_folder_exists(wg_path):
            return

        for subfolder in ["res_mods", "mods"]:
            subfolder_path = os.path.join(wg_path, subfolder)
            if self.check_folder_exists(subfolder_path):
                self.move_folders([subfolder], wg_path, self.output_folder)
        # Remove the WG folder after moving its contents
        if self.check_folder_exists(wg_path):
            shutil.rmtree(wg_path)
            print(f"Folder {wg_folder} successfully deleted.")

    def run(self) -> None:
        """
        Main method to start the extraction and file/folder management process.
        """
        if not self.check_folder_exists(self.folder_path):
            print(f"Folder {self.folder_path} does not exist.")
            return

        self.create_folder(self.output_folder)

        files = self.list_files(self.folder_path)
        archive_files = self.filter_archive_files(files)

        for archive_file in archive_files:
            archive_path = os.path.join(self.folder_path, archive_file)
            self.extract_archive(archive_path, self.output_folder)

        files_to_delete = [
            "Best mods.url",
            "install_mods_wotmod.txt",
            "install_mods.txt",
            "Скачать лучшие моды.url",
            "Установка.txt",
            "Установка .txt",
            "Установка_mods.txt",
            "ВНИМАНИЕ!!! WARNING!!!.txt",
            "ôßΓá¡«ó¬á .txt",
            "æ¬áτáΓ∞ ½πτΦ¿Ñ ¼«ñδ.url",
            "webSite.url",
            "Скачать лучшие моды_1.url",
        ]
        self.delete_files(files_to_delete, self.output_folder)

        folders_to_delete = [
            "2 4 8 16",
            "2 4 8 12 16 20 22 25 30",
            "2 4 8 12 16",
            "Lesta",
        ]
        self.delete_folders(folders_to_delete, self.output_folder)

        # Check and process WG folder if it exists
        if self.check_folder_exists(os.path.join(self.output_folder, "WG")):
            self.process_wg_folder("WG")

        target_folder = os.path.join(self.output_folder, "res_mods", "2.0.0.1")
        folders_to_move = ["objects", "scripts"]
        self.move_folders(folders_to_move, self.output_folder, target_folder)

        mods_target_folder = os.path.join(self.output_folder, "mods", "2.0.0.1")
        wotmod_file = "three-direction-indicator.wotmod"
        self.move_file(wotmod_file, self.output_folder, mods_target_folder)

        source_mods_folder = os.path.join(
            self.output_folder, "2 3 5 8 13 17 21 24 27 30", "mods"
        )
        target_mods_folder = os.path.join(self.output_folder, "mods")
        if self.check_folder_exists(source_mods_folder):
            self.move_folders(["mods"], source_mods_folder, target_mods_folder)
            empty_folder_path = os.path.join(
                self.output_folder, "2 3 5 8 13 17 21 24 27 30"
            )
            if self.check_folder_exists(empty_folder_path):
                shutil.rmtree(empty_folder_path)
                print("Folder 2 3 5 8 13 17 21 24 27 30 successfully deleted.")


if __name__ == "__main__":
    folder_path = "./download_mods"
    output_folder = "./unpacking_mods"
    extractor = ArchiveExtractor(folder_path, output_folder)
    extractor.run()

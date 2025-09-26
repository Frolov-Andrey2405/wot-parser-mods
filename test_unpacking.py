import os
import unittest
from unittest import mock

from unpacking import ArchiveExtractor


class TestArchiveExtractor(unittest.TestCase):
    def setUp(self):
        self.folder_path = "/fake/input"
        self.output_folder = "/fake/output"
        self.extractor = ArchiveExtractor(self.folder_path, self.output_folder)

    @mock.patch("os.path.exists")
    def test_check_folder_exists(self, mock_exists):
        mock_exists.return_value = True
        self.assertTrue(self.extractor.check_folder_exists("/some/folder"))
        mock_exists.assert_called_with("/some/folder")

    @mock.patch("os.makedirs")
    @mock.patch.object(ArchiveExtractor, "check_folder_exists")
    def test_create_folder(self, mock_check, mock_makedirs):
        mock_check.return_value = False
        self.extractor.create_folder("/some/folder")
        mock_makedirs.assert_called_with("/some/folder")

    @mock.patch("os.listdir")
    def test_list_files(self, mock_listdir):
        mock_listdir.return_value = ["file1.zip", "file2.rar", "file3.txt"]
        files = self.extractor.list_files("/some/folder")
        self.assertEqual(files, ["file1.zip", "file2.rar", "file3.txt"])
        mock_listdir.assert_called_with("/some/folder")

    def test_filter_archive_files(self):
        files = ["a.zip", "b.rar", "c.txt", "d.jpeg"]
        result = self.extractor.filter_archive_files(files)
        self.assertEqual(result, ["a.zip", "b.rar"])

    @mock.patch("zipfile.ZipFile.extractall")
    @mock.patch("zipfile.ZipFile.__init__", return_value=None)
    def test_extract_zip_archive(self, mock_zip_init, mock_extractall):
        archive_path = "/some/archive.zip"
        self.extractor.extract_archive(archive_path, "/output")
        mock_extractall.assert_called_with("/output")

    @mock.patch("shutil.rmtree")
    @mock.patch("os.path.exists")
    def test_delete_folders(self, mock_exists, mock_rmtree):
        mock_exists.return_value = True
        self.extractor.delete_folders(["folder1"], "/some/path")
        # Используем os.path.join для кроссплатформенности
        expected_path = os.path.join("/some/path", "folder1")
        mock_rmtree.assert_called_with(expected_path)

    @mock.patch("shutil.rmtree")
    @mock.patch("os.path.exists")
    def test_process_wg_folder(self, mock_exists, mock_rmtree):
        # Симулируем наличие WG папки
        def side_effect(path):
            if "WG" in path or "res_mods" in path:
                return True
            return False

        mock_exists.side_effect = side_effect
        with mock.patch.object(self.extractor, "move_folders") as mock_move:
            self.extractor.process_wg_folder("WG")
            mock_move.assert_called()  # Проверяем, что функция move_folders вызвалась
            mock_rmtree.assert_called_with(os.path.join(self.output_folder, "WG"))

import os

from devcli.core import project_root, traverse_search


def test_project_root_resolves_to_right_directory():
    assert str(project_root()) == os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def test_project_root_resolves_to_right_directory_with_filename():
    assert str(project_root(__file__)) == os.path.abspath(__file__)


def test_traverse_search_for_file_name(fs):
    files = [
        "/org/dept/project/module/file.txt",
        "/org/file.txt"
    ]
    for file in files:
        fs.create_file(file)

    assert traverse_search('file.txt', "/org/dept/project/module") == files


def test_traverse_search_for_directory(fs):
    expected = [
        "/org/dept/project/module/.devcli",
        "/org/dept/project/.devcli",
        "/org/dept/.devcli",
        "/org/.devcli",
        "/.devcli"
    ]
    for dir in expected:
        fs.create_dir(dir)

    assert traverse_search('.devcli', '/org/dept/project/module') == expected

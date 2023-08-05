import os
import re
from glob import glob


def tree_dir(root_path, excluded):
    """
    Creates a nested dictionary that represents the folder structure of an item.

    :param str root_path: Path of the root directory to explore.
    :param list[str] excluded: Regex strings of the directories to skip, if any.
    :return: The structure of the items of the given path, in a dictionary.
    :rtype: dict
    """
    if not os.path.isdir(root_path):
        raise OSError("Root path \"%s\" does not exist or is not a directory" % root_path)

    tree = {}
    excluded_regex = [] if excluded is None else [re.compile(e) for e in excluded]

    folder_index = root_path.replace("\\", "/").rstrip("/").rfind("/") + 1
    for path, dirs, files in os.walk(root_path):
        # Remove excluded directories from os walk
        dirs[:] = [d for d in dirs if not any([e.match(d) for e in excluded_regex])]

        # Place the gathered files in the tree dict at the retrieved address
        tree_addr = path.replace("\\", "/").rstrip("/")[folder_index:].split("/")
        gathered_items = {d: {} for d in dirs}
        gathered_items.update({f: None for f in files})
        parent = tree
        for addr in tree_addr[:-1]:
            parent = parent.get(addr)
        parent[tree_addr[-1]] = gathered_items

    return tree


def ls_dir(glob_path, content="ALL", excluded=None):
    """
    Obtain all contents of a directory, files & sub-directories that match a path.

    :param str glob_path: Absolute path to the target with glob filter format.
    :param str content: Content to return: FILE, DIR or ALL (default).
    :param list[str] excluded: Regex strings of the directories to skip, if any.
    :return: The resulting items from the search.
    :rtype: list[str]
    """
    e_regex = [] if excluded is None else [re.compile(e) for e in excluded]
    glob_result = [item.replace("\\", "/") for item in glob(glob_path) if not any([e.match(item) for e in e_regex])]

    if content == "FILE":
        return [item for item in glob_result if os.path.isfile(item)]
    elif content == "DIR":
        return [item for item in glob_result if os.path.isdir(item)]
    else:
        return glob_result

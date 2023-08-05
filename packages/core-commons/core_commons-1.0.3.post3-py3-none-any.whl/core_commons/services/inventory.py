import json
import logging
import os
import shutil
from datetime import datetime

import yaml

from core_commons.exceptions import InventoryManagerError, InventoryOperationError
from core_commons.handlers import file_handler
from core_commons.handlers.lockfile_handler import FileLock
from core_commons.services import GitClient

MANAGER_NONE = "NONE"
TIMEOUT = "timeout"
EXCLUDED_FOLDER_LIST = [r"\.git"]

MANAGER_GIT = "GIT"
GIT_URL = "url"
GIT_USER = "user"
GIT_PASSWORD = "password"
GIT_MESSAGE = "message"
GIT_REVERT_IF_ERR = "revert_if_err"


class Inventory:
    """
    Class that generates a context managed inventory for configuration items and bundles. To keep inventories secure
    and reliable, if a manager is declared the class must be context managed before any changes to the inventory can be
    made.
    """

    def __init__(self, inventory_path, manager, options):
        """
        Instantiates a new inventory.

        :param str inventory_path: The path to the local inventory in the current system.
        :param str manager: Type of the manager of the inventory. Can be "GIT" or "NONE" if inventory is not managed.
        :param dict options: Arguments for instancing and configuring the manager of the inventory.
        :rtype: Inventory
        """
        self.inventory_path = inventory_path.rstrip("/")
        self.manager_type = manager
        self.managed = False
        self.changed = False
        self._logger = logging.getLogger("Inventory(%s)@%s" % (manager, self.inventory_path.split("/")[-1]))

        if manager == MANAGER_GIT:
            self._load_git_manager(inventory_path, **options)
        elif manager == MANAGER_NONE:
            pass
        else:
            raise InventoryManagerError("Unknown inventory manager type [%s]" % manager)

    def __enter__(self):
        """
        Default context manager entry for a managed inventory.

        :return: self
        :rtype: Inventory
        """
        self.managed = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Default context manager exit for a managed inventory."""
        self.managed = False

    def resolve_tree(self, bundle_path=None):
        """
        Resolves the bundles of this inventory or of a given bundle on a tree like structure.

        :param str bundle_path: If set, will generate the tree structure with the given bundle path as root. Relative
                                tp inventory root.
        :return: Tree structure of the inventory or given bundle at full depth.
        :rtype: dict
        """
        root_bundle = bundle_path is None or bundle_path == ""
        full_path = self.inventory_path
        self._logger.debug("Resolving the tree structure of \"%s\"..." % (bundle_path if not root_bundle else "root"))
        if not root_bundle:
            full_path = "%s/%s" % (self.inventory_path, bundle_path)
        return file_handler.tree_dir(full_path, excluded=EXCLUDED_FOLDER_LIST)

    def list_bundles(self, bundle_path=None):
        """
        Lists the bundles of the inventory or of a given bundle.

        :param str bundle_path: If set, will list the bundles of the given bundle. Relative to inventory root.
        :return: List of the bundles of the inventory or given bundle.
        :rtype: list[str]
        """
        return self._list_content(bundle_path, True)

    def delete_bundle(self, bundle_path=None):
        """
        Deletes a bundle and all of it's contents.

        :param str bundle_path: Path of the bundle to delete relative to inventory root.
        """
        root_bundle = bundle_path is None or bundle_path == ""
        self._logger.debug("Listing item at \"%s\"..." % (bundle_path if not root_bundle else "root"))
        if root_bundle:
            raise InventoryManagerError("Cannot delete root bundle")
        full_path = "%s/%s" % (self.inventory_path, bundle_path)
        if not self.managed:
            raise InventoryOperationError("Cannot delete bundle on a non managed inventory")

        shutil.rmtree(full_path)
        self.changed = True

    def list_items(self, bundle_path=None):
        """
        Lists the items of the inventory or of a given bundle.

        :param str bundle_path: If set, will list the items of the given bundle. Relative to inventory root.
        :return: List of the items of the inventory or given bundle.
        :rtype: list[str]
        """
        return self._list_content(bundle_path, False)

    def create_item(self, item_path, data=None, item_type=None):
        """
        Creates a inventory item at a given path.

        :param str item_path: Path of the item to create relative to inventory root.
        :param dict data: Content of the inventory item.
        :param str item_type: Optional type of item to create. Can be "JSON" or "YAML". If set to None will try to infer
                              the file type from the extension, throwing an exception if it cannot.
        """
        self._logger.debug("Creating item at \"%s\"..." % item_path)
        full_path = "%s/%s" % (self.inventory_path, item_path)
        if not self.managed:
            raise InventoryOperationError("Cannot create item on a non managed inventory")
        if os.path.exists(full_path):
            raise InventoryOperationError("Cannot create item at \"%s\", item already exists" % item_path)

        self._write_inventory_file(full_path, data, item_type)
        self.changed = True

    def read_item(self, item_path, item_type=None):
        """
        Retrieves and returns the contents of an item.

        :param str item_path: Path of the item to read relative to inventory root.
        :param str item_type: Optional type of item to create. Can be "JSON" or "YAML". If set to None will try to infer
                              the file type from the extension, throwing an exception if it cannot.
        :return: The content of the inventory item
        :rtype: dict
        """
        self._logger.debug("Reading item at \"%s\"..." % item_path)
        full_path = "%s/%s" % (self.inventory_path, item_path)
        return self._read_inventory_file(full_path, item_type)

    def update_item(self, item_path, data=None, item_type=None):
        """
        Rewrites a inventory item at a given path.

        :param str item_path: Path of the item to rewrite relative to inventory root.
        :param dict data: New content of the inventory item.
        :param str item_type: Optional type of item to create. Can be "JSON" or "YAML". If set to None will try to infer
                              the file type from the extension, throwing an exception if it cannot.
        """
        self._logger.debug("Updating item at \"%s\"..." % item_path)
        full_path = "%s/%s" % (self.inventory_path, item_path)
        if not self.managed:
            raise InventoryOperationError("Cannot update item on a non managed inventory")
        if not os.path.isfile(full_path):
            raise InventoryOperationError("Cannot update item at \"%s\", item does not exist" % item_path)

        self._write_inventory_file(full_path, data, item_type)
        self.changed = True

    def patch_item(self, item_path, data=None, item_type=None, deep_merge=True):
        """
        Patches a inventory item at a given path.

        :param str item_path: Path of the item to patch relative to inventory root.
        :param dict data: Content to append to the inventory item.
        :param str item_type: Optional type of item to create. Can be "JSON" or "YAML". If set to None will try to infer
                              the file type from the extension, throwing an exception if it cannot.
        :param bool deep_merge: If set, will patch the dictionary recursively from the bottom by updating data entries
                                without replacing the data blocks.
        """
        def deep_merge_dict(source, patch):
            for key, value in patch.items():
                if key in source:
                    if hasattr(value, "items") and hasattr(patch, "items"):
                        value = deep_merge_dict(source[key], value)
                source[key] = value
            return source

        self._logger.debug("Patching item at \"%s\"..." % item_path)
        full_path = "%s/%s" % (self.inventory_path, item_path)
        patch_data = self._read_inventory_file(full_path, item_type)
        if not self.managed:
            raise InventoryOperationError("Cannot patch item on a non managed inventory")
        if patch_data is None:
            raise InventoryOperationError("Cannot patch item at \"%s\", item does not exist" % item_path)

        if data is not None:
            if deep_merge:
                patch_data = deep_merge_dict(patch_data, data)
            else:
                patch_data.update(data)
            self._write_inventory_file(full_path, patch_data, item_type)
            self.changed = True

    def delete_item(self, item_path):
        """
        Deletes a inventory item at a given path.

        :param str item_path: Path of the item to delete relative to inventory root.
        """
        self._logger.debug("Removing item at \"%s\"..." % item_path)
        full_path = "%s/%s" % (self.inventory_path, item_path)
        if not self.managed:
            raise InventoryOperationError("Cannot delete item on a non managed inventory")

        os.remove(full_path)
        self.changed = True

    def _load_git_manager(self, path, **kwargs):
        """
        Auxiliary method to generate the context manager methods of a GIT managed inventory.

        :param str path: The path to the local repository in the current system.
        :keyword str url: The url of the remote git repository. Required.
        :keyword str user: The user used to connect to the remote git repository. Required.
        :keyword str password: The password used to connect to the remote git repository. Required.
        :keyword int timeout: The optional timeout for the file lock. Default is 0.
        :keyword str message: The optional message for the git commit. Default is "Synchronized by Inventory Manager".
        :keyword bool revert_if_err: If set, will revert changes if context is broken by an error. Default is True.
        """
        for arg in [GIT_URL, GIT_USER, GIT_PASSWORD]:
            if arg not in kwargs:
                raise InventoryManagerError("Missing config [%s] for Git managed inventory" % arg)

        _lock_timeout = kwargs[TIMEOUT] if TIMEOUT in kwargs else 0
        _message = kwargs[GIT_MESSAGE] if GIT_MESSAGE in kwargs else "Synchronized by Inventory Manager"
        self._lock = FileLock(path + ".lock", _lock_timeout)
        self._manager = GitClient(path, kwargs["url"], kwargs["user"], kwargs["password"])
        self._revert_if_err = kwargs[GIT_REVERT_IF_ERR] if GIT_REVERT_IF_ERR in kwargs else True
        self._commit_message = "[%s] - %s" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), _message)
        self.__enter__ = self.__git_enter
        self.__exit__ = self.__git_exit

    def __git_enter(self):
        """Context manager entry for a Git managed inventory."""
        self.managed = True
        self._logger.debug("Managing inventory")

        self._lock.__enter__()
        self._manager.discard_changes_and_reset()
        self._manager.update_or_clone_from_repository()
        return self

    def __git_exit(self, exc_type, exc_val, exc_tb):
        """Context manager exit for a Git managed inventory."""
        if self.changed:
            if exc_type:
                if self._revert_if_err:
                    self._logger.warn("Exited inventory manager with errors, reverting changes...")
                    self._manager.discard_changes_and_reset()
            else:
                self._logger.debug("Uploading changes to repository...")
                self._manager.upload_to_repository(self._commit_message)
        self._lock.__exit__(exc_type, exc_val, exc_tb)

        self.managed = False
        self._logger.debug("Released inventory")

    def _list_content(self, bundle_path=None, list_bundles=True):
        """
        Lists the items or the bundles of the inventory or of a given bundle.

        :param str bundle_path: If set, will list the items of the given bundle. Relative to inventory root.
        :param bool list_bundles: If set, will list the bundles, otherwise will list the items.
        :return: List of the items of the inventory or given bundle.
        :rtype: list[str]
        """
        root_bundle = bundle_path is None or bundle_path == ""
        list_target = "bundles" if list_bundles else "items"
        ls_content = "DIR" if list_bundles else "FILE"
        full_path = self.inventory_path
        if not root_bundle:
            full_path = "%s/%s" % (self.inventory_path, bundle_path)
        if not os.path.isdir(full_path):
            raise OSError("\"%s\" does not exist or is not a directory" % full_path)

        self._logger.debug("Listing %s at \"%s\"..." % (list_target, bundle_path if not root_bundle else "root"))
        path_list = file_handler.ls_dir(full_path.rstrip("/") + "/*", content=ls_content, excluded=EXCLUDED_FOLDER_LIST)
        return [path.rstrip("/").split("/")[-1] for path in path_list]

    @staticmethod
    def _read_inventory_file(path, file_type=None):
        """
        Reads a file from a path. This convenience method is prepared to handle small inventory files.

        :param str path: Path of the configuration file to read.
        :param str file_type: Optional type of file to load. Can be "JSON" or "YAML". If set to None will try to infer
                              the file type from the extension, throwing an exception if it cannot.
        :return: The contents of the path. Will automatically parse json and yaml files into dictionaries.
        :rtype: dict
        """
        extension = None if "." not in path else path.split(".")[-1].lower()
        if not os.path.isfile(path):
            return None

        if file_type == "JSON" or (file_type is None and extension == "json"):
            with open(path, "r") as json_file:
                return json.load(json_file)
        elif file_type == "YAML" or (file_type is None and extension == "yaml"):
            with open(path, "r") as yaml_file:
                return yaml.safe_load(yaml_file)
        elif file_type is None:
            raise OSError("Could not infer file type from extension")
        else:
            raise OSError("Unknown file type [%s]" % file_type)

    @staticmethod
    def _write_inventory_file(path, content=None, file_type=None):
        """
        Creates or replaces a file from a path. This convenience method is prepared to handle small inventory files.

        :param str path: Path where the file should be written with file extension.
        :param dict content: The content of the configuration file.
        :param str file_type: Optional type of file to write. Can be "JSON" or "YAML". If set to None will try to infer
                              the file type from the extension, throwing an exception if it cannot.
        """
        dir_path = "/".join(path.split("/")[:-1])
        extension = None if "." not in path else path.split(".")[-1].lower()
        file_content = content if content is not None else {}
        if os.path.exists(dir_path):
            if not os.path.isdir(dir_path):
                raise OSError("Cannot write to a file, target folder exists and is not a folder")
        else:
            os.makedirs(dir_path)

        if file_type == "YAML" or (file_type is None and extension == "yaml"):
            with open(path, "w") as yaml_file:
                yaml.safe_dump(file_content, yaml_file)
        elif file_type == "JSON" or (file_type is None and extension == "json"):
            with open(path, "w") as json_file:
                json.dump(file_content, json_file)
        elif file_type is None:
            raise OSError("Could not infer file type from extension")
        else:
            raise OSError("Unknown file type [%s]" % file_type)

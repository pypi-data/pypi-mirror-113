import yaml

from core_commons.exceptions import MissingConfigurationError, BadConfigurationError

__ID_LABEL = "id"


def retrieve_by_reference(config, reference):
    """
    Retrieves a configuration element by a dotted reference.

    :param dict config: The configuration map to retrieve the data from.
    :param str reference: The reference of the item to retrieve, separated by dots.
    :return: The element retrieved.
    """
    keys = reference.split(".")
    aux = config
    try:
        for key in keys:
            aux = aux[key]
        return aux
    except (KeyError, TypeError) as e:
        raise MissingConfigurationError("Missing element [%s] from configuration" % reference, e)


def get_configuration(config_path, parse_map=None, reference_map=None, type_reference_map=None):
    """
    Retrieves the configuration file data, parses it, and unloads it into a data map.

    :param str config_path: Path to the configuration file.
    :param dict[str, function] parse_map: The configuration parse method for each required item. Parsing methods take
                                          the variable as first parameter and configuration as second parameter.
    :param dict[str, str] reference_map: The reference unload map for each item. Should declare the source of the data.
    :param dict[str, str] type_reference_map: Identical to the reference map, but takes item types too.
    :return: A configuration map with all data unloaded.
    :rtype: dict
    """
    with open(config_path) as config_file:
        raw_config = yaml.safe_load(config_file)
    return parse_and_unload_configuration(raw_config, parse_map, reference_map, type_reference_map)


def parse_and_unload_configuration(config, parse_map, reference_map, type_reference_map):
    """
    Utility method to parse and unload configuration elements.

    :param dict config: The base configuration data.
    :param dict[str, function] parse_map: The configuration parse method for each required item. Parsing methods take
                                          the variable as first parameter and configuration as second parameter.
    :param dict[str, str] reference_map: The reference unload map for each item. Should declare the source of the data.
    :param dict[str, str] type_reference_map: Identical to the reference map, but takes item types too.
    :return: The parsed and unloaded configuration data.
    :rtype: dict
    """
    if parse_map is not None:
        for key, parse_method in parse_map.items():
            __recursive_map_matching(config, key, parse_method)

    if reference_map is not None:
        for key, source_addr in reference_map.items():
            source_data = retrieve_by_reference(config, source_addr)
            __recursive_unload_matching(config, key, source_data)

    if type_reference_map is not None:
        for key, source_addr in type_reference_map.items():
            type_source_data = retrieve_by_reference(config, source_addr)
            __recursive_unload_matching_type(config, key, type_source_data)

    return config


def __recursive_unload_matching(source, element_key, element_data):
    """
    Recursively unloads any element from the reference element data into the source. Does not return a new dictionary,
    but modifies the one passed to the function.

    :param source: The source to unload.
    :param str element_key: The key to match.
    :param dict element_data: A group of elements keyed by element id that will be the reference for the unloading.
    """
    __recursive_map_matching(source, element_key, __unload_data_generator(element_key), element_data)


def __recursive_unload_matching_type(source, element_key, element_data):
    """
    Recursively unloads any element from the reference element data into the source by type. Does not return a new
    dictionary, but modifies the one passed to the function.

    :param source: The source to unload.
    :param str element_key: The key to match.
    :param dict element_data: A group of elements keyed by element id that will be the reference for the unloading.
    """
    __recursive_map_matching(source, element_key, __unload_data_type_generator(element_key), element_data)


def __unload_data_generator(element_key):
    """
    Generator for an unloader method. If unloaded id is missing will throw a configuration error.

    :param str element_key: The element type being unloaded.
    :return: A unloader method for the given element key.
    :rtype: function
    """

    def unload_data(value, data):
        try:
            if isinstance(value, list):
                return [data[item] for item in value]
            else:
                return data[value]
        except IndexError:
            raise MissingConfigurationError("Missing configuration element [%s] with name [%s]" % (element_key, value))

    return unload_data


def __unload_data_type_generator(element_key):
    """
    Generator for an unloader method that can handle types. If unloaded id is missing will throw a configuration error.

    :param str element_key: The element type being unloaded.
    :return: A class type unloader method for the given element key.
    :rtype: function
    """

    def unload_data_type(value, data):
        def __retrieve_ref(reference, source):
            if not hasattr(reference, "items"):
                raise BadConfigurationError("%s [%s] should be a reference or reference list" % (element_key, item))
            try:
                return {ref_type: source[ref_type][ref_id] for ref_type, ref_id in reference.items()}
            except IndexError as e:
                raise MissingConfigurationError("Missing element [%s] with name [%s]" % (element_key, value), e)

        if isinstance(value, list):
            return [__retrieve_ref(item, data) for item in value]
        else:
            return __retrieve_ref(value, data)

    return unload_data_type


def __recursive_map_matching(block, element_key, map_method, reference=None):
    """
    Recursively applies a map method to elements in a map if the key matches the one specified. Does not return a new
    dictionary, but modifies the one passed to the function

    :param block: The current block being mapped.
    :param str element_key: The key to match.
    :param function map_method: The method to apply once a matching key is found.
    :param reference: Reference data to use for the map method. By default the base dictionary being mapped.
    """
    ref = reference if reference is not None else block
    if hasattr(block, "items"):
        for key, value in block.items():
            if key == element_key:
                block[key] = map_method(value, reference)
            else:
                __recursive_map_matching(value, element_key, map_method, ref)
    elif isinstance(block, list) and len(block) > 0:
        [__recursive_map_matching(element, element_key, map_method, ref) for element in block]

from copy import copy


class ErrorEntity:
    """
    This class implements functionality for items to relay errors and warnings on a controlled environment without
    breaking execution.
    """

    def __init__(self, prefix="", child_entities=None):
        """
        Instantiates a new error entity. Child entities will report their errors when getting the issues from their
        parent, and will also be reset when their parent is.

        :param prefix: The prefix of this entity's error.
        :param list[ErrorEntity] child_entities: List of component entities of this error entity.
        :raises ValueError: If a entity is a child of itself
        """

        children = child_entities if child_entities is not None else []
        if not self.__check_valid_connection(children):
            raise ValueError("Circular dependency caused by child entities")

        self.__child_entities = children
        self.__prefix = prefix
        self.__errors = []
        self.__warnings = []

    def get_issues(self):
        """
        Method used to get the issues raised (if any) from this entity.

        :return: A tuple containing a list of errors and a list of warnings.
        :rtype: (list[str], list[str])
        """
        errors = [error for error in self.__errors]
        warnings = [warning for warning in self.__warnings]

        for child in self.__child_entities:
            c_errors, c_warnings = child.get_issues()
            errors.extend(c_errors)
            warnings.extend(c_warnings)

        return errors, warnings

    def reset_issues(self):
        """Resets errors and warnings of this entity and child entities"""
        self.__errors = []
        self.__warnings = []
        for child in self.__child_entities:
            child.reset_issues()

    def add_error(self, error):
        """
        Adds an error to the entity error list.

        :param str error: The error to add.
        """
        self.__errors.append(self.__prefix + error)

    def add_warning(self, warning):
        """
        Adds an warning to the entity warning list.

        :param str warning: The error to add.
        """
        self.__warnings.append(self.__prefix + warning)

    def __check_valid_connection(self, children):
        """
        Auxiliary method to check whether an entity can have the given children entities.

        :param list[ErrorEntity] children: The expected children entities.
        :return: True if the resulting directed graph is non cyclic and only passes through each entity once.
        :rtype: bool
        """
        return ErrorEntity.__check_valid_connection_cycle(copy(children), [self])

    @staticmethod
    def __check_valid_connection_cycle(entity_queue, visited_entities):
        """
        Utility cycle for checking whether an entity can have the given children entities.

        :param list[ErrorEntity] entity_queue: Entities not yet checked.
        :param list[ErrorEntity] visited_entities: Entities already visited once.
        :return:
        """
        # If there are no more nodes to test, the entity tree is valid.
        if len(entity_queue) == 0:
            return True

        # Fail if the next entity has been visited
        next_entity = entity_queue.pop()
        if next_entity in visited_entities:
            return False

        # Append node children to queue and go to next cycle
        visited_entities.append(next_entity)
        entity_queue.extend(next_entity.__child_entities)
        return ErrorEntity.__check_valid_connection_cycle(entity_queue, visited_entities)

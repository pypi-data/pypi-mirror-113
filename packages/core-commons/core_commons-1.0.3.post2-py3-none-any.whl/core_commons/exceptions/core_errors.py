from core_commons.exceptions.base_error import BaseError

# CONFIGURATION ERROR CODES
CONFIGURATION_ERROR = "CONF000"
MISSING_CONFIGURATION_ERROR = "CONF010"
BAD_CONFIGURATION_ERROR = "CONF020"

# INVENTORY ERROR CODES
INVENTORY_ERROR = "INV000"
INVENTORY_MANAGER_ERROR = "INV010"
INVENTORY_OPERATION_ERROR = "INV020"


class ConfigurationError(BaseError):
    """General configuration error."""

    def __init__(self, message, caused_by=None):
        BaseError.__init__(self, message, CONFIGURATION_ERROR, caused_by)


class MissingConfigurationError(BaseError):
    """Missing configuration element or reference."""

    def __init__(self, message, caused_by=None):
        BaseError.__init__(self, message, MISSING_CONFIGURATION_ERROR, caused_by)


class BadConfigurationError(BaseError):
    """Configuration element is badly formatted or unexpected."""

    def __init__(self, message, caused_by=None):
        BaseError.__init__(self, message, BAD_CONFIGURATION_ERROR, caused_by)


class InventoryError(BaseError):
    """General inventory error."""

    def __init__(self, message, caused_by=None):
        BaseError.__init__(self, message, INVENTORY_ERROR, caused_by)


class InventoryManagerError(BaseError):
    """Inventory manager missing or badly configured."""

    def __init__(self, message, caused_by=None):
        BaseError.__init__(self, message, INVENTORY_MANAGER_ERROR, caused_by)


class InventoryOperationError(BaseError):
    """Inventory manager operation failed."""

    def __init__(self, message, caused_by=None):
        BaseError.__init__(self, message, INVENTORY_OPERATION_ERROR, caused_by)

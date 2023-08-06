"""Version information for this package."""
### IMPORTS
### ============================================================================
## Standard Library

## Installed

## Application

### CONSTANTS
### ============================================================================
## Version Information - DO NOT EDIT
## -----------------------------------------------------------------------------
# These variables will be set during the build process. Do not attempt to edit.
PACKAGE_VERSION = "0.2.0"
BUILD_VERSION = "0.2.0.1626539599"
BUILD_GIT_HASH = "6b6b15403db89e549bd43fc40788085283a4950d"
BUILD_GIT_HASH_SHORT = "6b6b154"
BUILD_GIT_BRANCH = "master"
BUILD_TIMESTAMP = 1626539599
BUILD_DATETIME = datetime.datetime.utcfromtimestamp(1626539599)

VERSION_VARS = vars()  # Don't have f-strings until py36

## Version Information Templates
## -----------------------------------------------------------------------------
# You can customise the templates used for version information here.
VERSION_INFO_TEMPLATE_SHORT = "{BUILD_VERSION}"
VERSION_INFO_TEMPLATE = "{PACKAGE_VERSION} ({BUILD_VERSION})"
VERSION_INFO_TEMPLATE_LONG = (
    "{PACKAGE_VERSION} ({BUILD_VERSION}) ({BUILD_GIT_BRANCH}@{BUILD_GIT_HASH_SHORT})"
)
VERSION_INFO_TEMPLATE_FULL = (
    "{PACKAGE_VERSION} ({BUILD_VERSION})\n"
    "{BUILD_GIT_BRANCH}@{BUILD_GIT_HASH}\n"
    "Built: {BUILD_DATETIME}"
)

### FUNCTIONS
### ============================================================================
def get_version_info_short() -> str:  # pylint: disable=missing-function-docstring
    return VERSION_INFO_TEMPLATE_SHORT.format(**VERSION_VARS)


def get_version_info() -> str:  # pylint: disable=missing-function-docstring
    return VERSION_INFO_TEMPLATE.format(**VERSION_VARS)


def get_version_info_long() -> str:  # pylint: disable=missing-function-docstring
    return VERSION_INFO_TEMPLATE_LONG.format(**VERSION_VARS)


def get_version_info_full() -> str:  # pylint: disable=missing-function-docstring
    return VERSION_INFO_TEMPLATE_FULL.format(**VERSION_VARS)

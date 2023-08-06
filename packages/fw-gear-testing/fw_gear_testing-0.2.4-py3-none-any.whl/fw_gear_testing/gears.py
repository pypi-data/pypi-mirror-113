import flywheel
import pytest
from dotty_dict import dotty

default_gear = {
    "name": "a-gear",
    "version": "0.0.0",
    "inputs": {
        "api-key": {"base": "api-key"},
        "file0": {"base": "file", "description": "a file"},
    },
    "config": {"config0": {"type": "string", "default": False, "description": ""}},
    "custom": {
        "gear-builder": {"image": "image-name"},
        "docker-image": "image-name",
    },
}


def make_gear(updates=None):
    """Make a gear manifest.

    Default values:
        {
            name: "a-gear",
            version: "0.0.0",
            inputs: {
                "api-key": {"base": "api-key"},
                "file0": {"base": "file", "description": "a file"},
            },
            config: {"config0": {"type": "string", "default": False, "description": ""}},
            custom: {
                "gear-builder": {"image": "image-name"},
                "docker-image": "image-name",
            },
        }

    Pass in dictionary of dotty keys to update the default dictionary, i.e.:
    ```python
    >>> gear = make_gear({'config.debug':{'type':'boolean','default': False}})
    ```
    """
    my_gear = dotty(default_gear)
    if updates:
        for k, v in updates.items():
            my_gear[k] = v
    print(my_gear)
    return flywheel.Gear(**my_gear)


@pytest.fixture
def gear_fixture():
    return make_gear


@pytest.fixture(scope="function")
def gear_doc(gear_fixture):
    default_category = "utility"

    def get_gear_doc(category=None, gear=None):
        if not gear:
            gear = gear_fixture()
        if not category:
            category = default_category
        return flywheel.GearDoc(category=category, gear=gear)

    return get_gear_doc

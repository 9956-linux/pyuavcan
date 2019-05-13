#
# Copyright (c) 2019 UAVCAN Development Team
# This software is distributed under the terms of the MIT License.
# Author: Pavel Kirienko <pavel.kirienko@zubax.com>
#

import sys
import typing
import shutil
import pytest
import pathlib
import logging
import pyuavcan.dsdl


# Please maintain these carefully if you're changing the project's directory structure.
PROJECT_ROOT_DIR = pathlib.Path(__file__).parent.parent.parent
DESTINATION_DIRECTORY = PROJECT_ROOT_DIR / pathlib.Path('.test_dsdl_generated')
PUBLIC_REGULATED_DATA_TYPES = PROJECT_ROOT_DIR / 'public_regulated_data_types.cache'
TEST_DATA_TYPES = pathlib.Path(__file__).parent / 'namespaces'


# https://docs.pytest.org/en/latest/fixture.html#conftest-py-sharing-fixture-functions
@pytest.fixture('session')  # type: ignore
def generated_packages() -> typing.Iterator[typing.List[pyuavcan.dsdl.GeneratedPackageInfo]]:
    original_sys_path = sys.path
    sys.path.insert(0, str(DESTINATION_DIRECTORY))
    logging.getLogger('pydsdl').setLevel(logging.WARNING)

    if DESTINATION_DIRECTORY.exists():  # pragma: no cover
        shutil.rmtree(DESTINATION_DIRECTORY, ignore_errors=True)
    DESTINATION_DIRECTORY.mkdir(parents=True, exist_ok=True)

    yield [
        pyuavcan.dsdl.generate_package_from_dsdl_namespace(
            DESTINATION_DIRECTORY,
            PUBLIC_REGULATED_DATA_TYPES / 'uavcan',
            []),
        pyuavcan.dsdl.generate_package_from_dsdl_namespace(
            DESTINATION_DIRECTORY,
            TEST_DATA_TYPES / 'test',
            [
                PUBLIC_REGULATED_DATA_TYPES / 'uavcan'
            ]),
    ]

    logging.getLogger('pydsdl').setLevel(logging.DEBUG)
    sys.path = original_sys_path
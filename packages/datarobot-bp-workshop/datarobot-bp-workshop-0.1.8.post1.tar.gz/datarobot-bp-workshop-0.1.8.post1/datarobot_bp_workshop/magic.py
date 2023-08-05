"""
Copyright 2021 DataRobot, Inc. and its affiliates.

All rights reserved.

DataRobot, Inc. Confidential.

This is unpublished proprietary source code of DataRobot, Inc. and its affiliates.

The copyright notice above does not evidence any actual or intended publication of such source code.

Released under the terms of DataRobot Tool and Utility Agreement.
"""

import os
import tempfile

from IPython.core import magic_arguments
from IPython.core.magic import register_cell_magic
from datarobot import CustomModelVersion
from datarobot._experimental import CustomTrainingModel


@magic_arguments.magic_arguments()
@magic_arguments.argument(
    "custom_model_id", type=str, help="Environment to use with the custom task"
)
@register_cell_magic
def update_custom(line, cell):
    args = magic_arguments.parse_argstring(update_custom, line)
    return update_custom_task(code=cell, custom_model_id=args.custom_model_id)


def update_custom_task(code: str, custom_model_id: str = None):
    with tempfile.TemporaryDirectory() as d:
        with open(os.path.join(d, "custom.py"), mode="w") as f:
            f.write(code)

        custom_model = CustomTrainingModel.get(custom_model_id)
        previous_version = custom_model.latest_version
        environment_id = previous_version.base_environment_id

        return CustomModelVersion.create_from_previous(
            custom_model_id, environment_id, is_major_update=False, files=[f.name]
        ).custom_model_id

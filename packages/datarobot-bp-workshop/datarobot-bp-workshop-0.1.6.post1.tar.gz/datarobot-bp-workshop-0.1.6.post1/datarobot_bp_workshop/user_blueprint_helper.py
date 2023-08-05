"""
Copyright 2021 DataRobot, Inc. and its affiliates.

All rights reserved.

DataRobot, Inc. Confidential.

This is unpublished proprietary source code of DataRobot, Inc. and its affiliates.

The copyright notice above does not evidence any actual or intended publication of such source code.

Released under the terms of DataRobot Tool and Utility Agreement.
"""

from typing import List

from datarobot._experimental.models.user_blueprints.models import (
    UserBlueprintTaskArgument,
    UserBlueprintTaskCustomTaskMetadata,
)


class UserBlueprintHelper(object):
    @staticmethod
    def get_arguments(arguments: List[UserBlueprintTaskArgument]):
        return [
            a
            for a in sorted(arguments, key=lambda a: a.argument.name)
            if a.argument.tunable is not False and not a.key.startswith("pp_")
        ]

    @staticmethod
    def get_docstring_for_parameter(
        argument: UserBlueprintTaskArgument, minified=False
    ):
        key = argument.key
        value = argument.argument
        template = "{name} ({key}): {type}, (Default={default})\n"
        if not minified:
            template += "    Possible Values: {values}\n"
        return template.format(
            name=value.name,
            key=key,
            type=value.type,
            default=value.default.__repr__(),
            values=value.values,
        )

    @staticmethod
    def get_docstring_for_arguments(
        arguments: List[UserBlueprintTaskArgument], title: str, minified=False
    ):
        return UserBlueprintHelper.get_docstring_for_lines(
            lines=[
                UserBlueprintHelper.get_docstring_for_parameter(
                    entry, minified=minified
                )
                for entry in arguments
            ],
            title=title,
            minified=minified,
        )

    @staticmethod
    def get_docstring_for_versions(
        versions: List[UserBlueprintTaskCustomTaskMetadata], title: str, minified=False
    ):
        template = "{} ({}): str\n"
        if not minified:
            template += (
                "    The version id used to determine "
                "which version of a custom task to use.\n"
            )
        return UserBlueprintHelper.get_docstring_for_lines(
            lines=[template.format(version.label, version.id) for version in versions],
            title=title,
            minified=minified,
        )

    @staticmethod
    def get_docstring_for_lines(lines: List[str], title: str, minified=False):
        docstring_definitions = []

        if not minified:
            if title:
                docstring_definitions = [title, ""]

            docstring_definitions += ["Parameters", "----------"]

        docstring_definitions += lines

        return "\n".join(docstring_definitions)

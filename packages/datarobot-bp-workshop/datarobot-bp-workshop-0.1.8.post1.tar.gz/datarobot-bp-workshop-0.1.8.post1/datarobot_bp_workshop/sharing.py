"""
Copyright 2021 DataRobot, Inc. and its affiliates.

All rights reserved.

DataRobot, Inc. Confidential.

This is unpublished proprietary source code of DataRobot, Inc. and its affiliates.

The copyright notice above does not evidence any actual or intended publication of such source code.

Released under the terms of DataRobot Tool and Utility Agreement.
"""

from typing import Union, List

from datarobot._experimental import UserBlueprint
from datarobot._experimental.models.user_blueprints.models import (
    GrantAccessControlWithUsernameValidator,
    GrantAccessControlWithIdValidator,
)
from datarobot.errors import ClientError

from datarobot_bp_workshop.exceptions import FeatureUnavailable
from datarobot_bp_workshop.utils import RecipientType, Roles


class SharingInterface(object):
    """ Methods for sharing User Blueprints """

    def share(
        self,
        user_blueprint_id: str,
        usernames: Union[str, List[str]],
        role: str = Roles.CONSUMER,
    ):
        """ Share a User Blueprint with a user or list of other users by username. """
        if not isinstance(usernames, list):
            usernames = [usernames]

        try:
            return UserBlueprint.update_shared_roles(
                user_blueprint_id,
                [
                    GrantAccessControlWithUsernameValidator(
                        role=role,
                        share_recipient_type=RecipientType.USER,
                        username=username,
                    )
                    for username in usernames
                ],
            )
        except ClientError as e:
            if e.status_code != 403:
                raise e
            raise FeatureUnavailable(
                "Unable to share or sharing is not available on this account."
            )

    def share_with_group(
        self,
        user_blueprint_id: str,
        group_ids: Union[str, List[str]],
        role: str = Roles.CONSUMER,
    ):
        """ Share a User Blueprint with a group or list of groups by id. """
        return self._share_with(
            user_blueprint_id=user_blueprint_id,
            recipient_ids=group_ids,
            recipient_type=RecipientType.GROUP,
            role=role,
        )

    def share_with_org(
        self,
        user_blueprint_id: str,
        org_ids: Union[str, List[str]],
        role: str = Roles.CONSUMER,
    ):
        """ Share a User Blueprint with a group or list of organizations by id. """
        return self._share_with(
            user_blueprint_id=user_blueprint_id,
            recipient_ids=org_ids,
            recipient_type=RecipientType.ORGANIZATION,
            role=role,
        )

    def _share_with(
        self,
        user_blueprint_id: str,
        recipient_type: str,
        recipient_ids: Union[str, List[str]],
        role: str,
    ):
        if not isinstance(recipient_ids, list):
            recipient_ids = [recipient_ids]
        try:
            return UserBlueprint.update_shared_roles(
                user_blueprint_id,
                [
                    GrantAccessControlWithIdValidator(
                        role=role, share_recipient_type=recipient_type, id=recipient_id
                    )
                    for recipient_id in recipient_ids
                ],
            )
        except ClientError as e:
            if e.status_code != 403:
                raise e
            raise FeatureUnavailable(
                "Unable to share or sharing is not available on this account."
            )

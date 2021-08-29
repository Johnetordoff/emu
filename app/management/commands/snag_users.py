from web.utils import get_paginated_data
from django_extensions.management.commands import shell_plus
import asyncio
import json
from spam_scan.models import SpamUserData
from web.models.user import User


def snag_users(user_guid, page_range=None):
    user = User.load(user_guid)

    user_json = asyncio.run(
        get_paginated_data(
            user.token,
            "https://api.osf.io/v2/users/?page[size]=100&fields[users]=full_name,social,employment,education,id",
            page_range=page_range,
        )
    )
    with open("user_data.json", "w") as outfile:
        json.dump(user_json, outfile)

    for i, user in enumerate(user_json):
        print(f"#{i}")
        data, created = SpamUserData.objects.get_or_create(
            guid=user["id"], **user["attributes"]
        )
        print(f"{i} {data, created }")


class Command(shell_plus.Command):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--flag",
            action="store_true",
            dest="flag",
            help="Update records in the database",
        )
        parser.add_argument(
            "--guid",
            dest="guid",
            type=str,
        )

    def handle(self, *args, **options):
        flag = options.get("flag", False)
        guid = options.get("guid", False)

        snag_users(guid, page_range=(1, 100))

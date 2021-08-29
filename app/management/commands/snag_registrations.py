from web.utils import get_paginated_data
from django_extensions.management.commands import shell_plus
import asyncio
import json
from spam_scan.models import SpamRegistrationData
from app import settings
from web.models import User


def snag_registrations(user_guid, page_range=None):
    user = User.load(user_guid)

    registrations_json = asyncio.run(
        get_paginated_data(
            user.token,
            f"{settings.OSF_API_URL}v2/registrations/?fields[registrations]=description,title&page=2&page[size]=100",
            page_range=page_range,
        )
    )
    with open("registrations_json.json", "w") as outfile:
        json.dump(registrations_json, outfile)

    for i, user in enumerate(registrations_json):
        data, created = SpamRegistrationData.objects.get_or_create(
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

    def handle(self, *args, **options):
        flag = options.get("flag", False)
        snag_registrations(page_range=(1, 100))

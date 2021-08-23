import requests
from web.utils import get_paginated_data
from django_extensions.management.commands import shell_plus
import asyncio
import json
from web.models.spam import SpamUserData

def snag_users(page_range=None):
    user_json = asyncio.run(
        get_paginated_data(
            'yJIpAwnKBGuvVsm7zkXUxqh0LvYDshEr0hboJU9rZh828xvgCHSRyaRtQw22n0jKLv5Vkw',
            'https://api.osf.io/v2/users/?page[size]=100&fields[users]=full_name,social,employment,education,id',
            page_range=page_range
        )
    )
    with open('user_data.json', 'w') as outfile:
        json.dump(user_json, outfile)

    for i, user in enumerate(user_json):
        print(f'#{i}')
        data, created = SpamUserData.objects.get_or_create(
            guid=user['id'],
            **user['attributes']

        )
        print(f'{i} {data, created }')

class Command(shell_plus.Command):

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--flag',
            action='store_true',
            dest='flag',
            help='Update records in the database',
        )

    def handle(self, *args, **options):
        flag = options.get('flag', False)

        snag_users(page_range=(1,100))
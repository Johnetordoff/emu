import requests
from web.utils import get_paginated_data
from django_extensions.management.commands import shell_plus
import asyncio
import json
from web.models.spam import SpamUserData

def flatten(A):
    rt = []
    for i in A:
        if isinstance(i,list):
            rt.extend(flatten(i))
        else: rt.append(i)
    return rt

def score_spam():
    for user in SpamUserData.objects.exclude(social={}):
        data = [item for item in flatten(user.social.values()) if item]


        for item in data:
            payload = {
                "content": str(item),
            }
            resp = requests.post(
                'https://api.oopspam.com/v1/spamdetection',
                headers={'X-Api-Key': 'pJHBCCCDMVhGH8OZOw3WDchbdDX9esVrSu8FB4Eq'},
                json=payload,
            )
            print(resp._content)




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

        score_spam()
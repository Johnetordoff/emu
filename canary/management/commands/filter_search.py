import datetime
import logging
import requests
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)
from web.utils import get_paginated_data
from asyncio import run

async def filter_search(filter, value, fields, output='html'):
    data = await get_paginated_data(
        token=None,
        url=f'https://api.osf.io/v2/users/?filter[{filter}]={value}&fields={fields}'
    )
    if output == 'html':
        html = '<table>'
        for field in fields:
            html += f'<th>{field}</th>'
        for item in data:
            columns = []
            for field in fields:
                if field == '_id':
                    stuff = item['id']
                else:
                    stuff = item["attributes"][field]
                columns += f'<td>{stuff}</td>'

            html += f'<tr>{"".join(columns)}</tr>'
        html += '</table>'
        return html

    if output == 'CSV':
        rows = []
        for item in data:
            columns = []
            for field in fields:
                if field == '_id':
                    stuff = item['id']
                else:
                    stuff = item["attributes"][field]
                columns.append(stuff)
            rows.append(columns)
        rows.insert(0, fields)
        return rows

class Command(BaseCommand):
    help = '''Populates new deleted field for various models. Ensure you have run migrations
    before running this script.'''

    def add_arguments(self, parser):
        parser.add_argument(
            '--filter',
            type=str,
            required=True,
        )
        parser.add_argument(
            '--value',
            type=str,
            required=True,
        )

    def handle(self, *args, **options):
        fields = options['fields']
        filter = options['filter']
        output = options['output']
        value = options['value']
        return run(filter_search(filter, value, fields, output))
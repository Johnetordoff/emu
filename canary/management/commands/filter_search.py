import logging
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)
from web.utils import get_paginated_data
from asyncio import run


async def user_filter_search(filter, value, fields, output='html'):
    data = await get_paginated_data(
        token=None,
        url=f'https://api.osf.io/v2/users/?filter[{filter}]={value}&fields[users]={",".join(fields)}&page[size]=100'
    )
    if 'data' in data:
        data = data['data']

    if output == 'HTML':
        html = '<table class="table" >'
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


async def node_filter_search(filter, value, fields, output='html'):
    data = await get_paginated_data(
        token=None,
        url=f'https://api.osf.io/v2/nodes/?filter[{filter}]={value}&fields[nodes]={",".join(fields)}&page[size]=100'
    )
    if 'data' in data:
        data = data['data']

    if output == 'HTML':
        html = '<table class="table" >'
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
        return run(user_filter_search(filter, value, fields, output))

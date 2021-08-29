import asyncio
import requests
import math


async def get_with_retry(token, url, headers=None):
    if not headers:
        headers = {}

    headers["Authorization"] = f"Bearer {token}"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()


async def get_pages(token, url, page, result={}):
    url = f"{url}?page={page}&page={page}"
    data = await get_with_retry(token, url)
    result[page] = data["data"]
    return result


async def get_paginated_data(token, url, page_range=None):
    data = await get_with_retry(token, url)
    tasks = []
    is_paginated = data.get("links", {}).get("next")

    if is_paginated:
        if page_range:
            result = {page_range[0]: data["data"]}
        else:
            result = {1: data["data"]}
        total = data["links"].get("meta", {}).get("total") or data["meta"].get("total")
        per_page = data["links"].get("meta", {}).get("per_page") or data["meta"].get(
            "per_page"
        )

        if not page_range:
            page_range = range(1, math.ceil(int(total) / int(per_page))) or page_range
        for i in range(*page_range):
            task = get_pages(token, url, i, result)
            tasks.append(task)

        await asyncio.gather(*tasks)
        pages_as_list = []
        # through the magic of async all our pages have loaded.
        for page in list(result.values()):
            pages_as_list += page
        return pages_as_list
    else:
        return data

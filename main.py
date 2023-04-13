import asyncio
import json
from urllib.parse import quote
from typing import Union

import aiohttp
from aiohttp import ClientSession

import parse
from spider import fetch_json
from store import store


async def get_images(session: ClientSession, cursor: Union[int, None] = None):
    payload = {
        "json": {
            "period": "AllTime",
            "browsingMode": "SFW",
            "sort": "Most Reactions",
            "cursor": cursor
        },
        "meta": {"values": {"cursor": ["undefined" if not cursor else "bigint"]}}
    }

    url = "https://civitai.com/api/trpc/image.getInfinite"
    json_data = await fetch_json(session, f"{url}?input={quote(json.dumps(payload))}")
    return json_data


async def run():
    headers = {
        "referer": "https://civitai.com",
        "content-type": "application/json"
    }
    async with aiohttp.ClientSession(
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=30),
    ) as session:
        cursor = 383018
        while True:
            json_data = await get_images(session, cursor)
            data = json_data["result"]["data"]["json"]
            for item in data["items"]:
                images = parse.images(item)
                await store(cursor or 0, images)

            _cursor = data["nextCursor"]
            print(_cursor)
            if not _cursor:
                return

            cursor = int(data["nextCursor"])
            await asyncio.sleep(0.3)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())

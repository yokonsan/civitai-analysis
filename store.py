import os
import aiofiles
from typing import List

from _typing import ModelImage


async def model_path(model_id: int) -> str:
    path = f"data/{model_id}"
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except FileExistsError:
            pass

    return path


async def store(model_id: int, images: List[ModelImage]):
    path = await model_path(model_id)
    async with aiofiles.open(f"{path}/images.txt", "a") as w:
        for image in images:
            # print(image, type(image))
            await w.write(str(image) + "\n")

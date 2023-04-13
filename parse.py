import json
import traceback
from typing import Any, Dict, List

from _typing import ModelImage, ImageMeta


def items(body):
    data = json.loads(body)
    items = []
    try:
        items = data["result"]["data"]["json"]["items"]
    except KeyError:
        print(f"parse items error: {body}")

    return items


def images(item: Dict[str, Any]) -> List[ModelImage]:
    _images = []
    try:
        _meta = item.get("meta") or {}
        _images.append(ModelImage(
            id=item.get("id"),
            url=item.get("url"),
            nsfw=item.get("nsfw"),
            width=item.get("width"),
            height=item.get("height"),
            meta=ImageMeta(
                size=_meta.get("Size"),
                seed=_meta.get("seed"),
                steps=_meta.get("steps"),
                sampler=_meta.get("sampler"),
                prompt=_meta.get("prompt"),
                negative_prompt=_meta.get("negativePrompt"),
                cfg_scale=_meta.get("cfgScale"),
                model=_meta.get("Model"),
                model_hash=_meta.get("Model hash"),
            )
        ))
    except KeyError:
        print(f"parse user error: {item}, {traceback.format_exc()}")

    return _images

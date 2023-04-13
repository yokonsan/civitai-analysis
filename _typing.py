import json
from typing import NamedTuple, Any


class ImageMeta(NamedTuple):
    size: str
    seed: int
    steps: int
    sampler: str
    prompt: str
    negative_prompt: str
    cfg_scale: float
    model: str
    model_hash: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "size": self.size,
            "seed": self.seed,
            "steps": self.steps,
            "prompt": self.prompt,
            "negative_prompt": self.negative_prompt,
            "sampler": self.sampler,
            "cfg_scale": self.cfg_scale,
            "model": self.model,
            "model_hash": self.model_hash,
        }


class ModelImage(NamedTuple):
    """用户上传图片"""
    id: int
    url: str
    nsfw: bool
    width: int
    height: int
    meta: ImageMeta

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "url": self.url,
            "nsfw": self.nsfw,
            "width": self.width,
            "height": self.height,
            "meta": self.meta.to_dict()
        }

    def __str__(self) -> str:
        return json.dumps(self.to_dict())

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ModelImage):
            return False
        return self.id == other.id

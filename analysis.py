import functools
import json
import os
import re
from collections import Counter

clean_pattern = "<.*?>|:[ 0-9.]+|[({\[\]})\r\n]"  # 清除模型词、权重词


def get_prompt_words(prompt):
    return [word.strip() for word in re.sub(clean_pattern, "", prompt).split(",")] if prompt else []


def prompt_words():
    cnt = Counter()

    def counter(prompt):
        for word in filter(lambda x: x, get_prompt_words(prompt)):
            cnt[word] += 1

        return cnt

    return counter


negative_prompt_words = prompt_words


def counter(func):
    cnt = Counter()

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        result = func(*args, **kwargs)
        if result:
            cnt[result] += 1
        return cnt
    return wrapped


@counter
def size(meta):
    return meta.get("size")


@counter
def steps(meta):
    return meta.get("steps")


@counter
def sampler(meta):
    return meta.get("sampler")


@counter
def cfg_scale(meta):
    return meta.get("cfg_scale")


model_map = {}


@counter
def model(meta):
    model_hash = meta.get("model_hash")
    if not model_hash:
        return

    _model = meta.get("model") or model_map.get(model_hash)
    if not _model:
        return

    if model_hash not in model_map and _model:
        model_map[model_hash] = _model

    return f"{_model}_{model_hash}"


def loads_data():
    size_cnt, steps_cnt, sampler_cnt, cfg_scale_cnt, model_cnt \
        = size({}), steps({}), sampler({}), cfg_scale({}), model({})
    prompt_words_cnt, negative_prompt_words_cnt = prompt_words(), negative_prompt_words()

    for path in os.listdir("data"):
        with open(f"data/{path}/images.txt", "r") as r:
            for line in r:
                meta = json.loads(line)["meta"]
                size(meta)
                steps(meta)
                sampler(meta)
                cfg_scale(meta)
                model(meta)

                prompt_words_counter = prompt_words_cnt(meta["prompt"])
                negative_prompt_words_counter = negative_prompt_words_cnt(meta["negative_prompt"])

    return (
        size_cnt,
        steps_cnt,
        sampler_cnt,
        cfg_scale_cnt,
        model_cnt,
        prompt_words_counter,
        negative_prompt_words_counter
    )


if __name__ == '__main__':
    (
        size_cnt,
        steps_cnt,
        sampler_cnt,
        cfg_scale_cnt,
        model_cnt,
        prompt_words_cnt,
        negative_prompt_words_cnt
    ) = loads_data()

    for cnt in (
        size_cnt,
        steps_cnt,
        sampler_cnt,
        cfg_scale_cnt,
        model_cnt,
        prompt_words_cnt,
        negative_prompt_words_cnt
    ):
        print(cnt.most_common(10))

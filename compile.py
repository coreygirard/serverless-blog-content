import os
import re

import requests


def gen_markdown(s):
    s = re.sub(
        r"\!\[\]\(([^)]*?)\)",
        r"![https://raw.githubusercontent.com/coreygirard/serverless-blog-content/master](\1)",
        s,
    )

    url = "https://api.github.com/markdown/raw"

    headers = {"Content-Type": "text/plain"}
    o = requests.post(url, headers=headers, data=s).text
    return o


def compile_md(from_path, to_path):
    with open(from_path, "r") as f:
        before = f.read()
    after = gen_markdown(before)
    with open(to_path, "w") as f:
        f.write(after)


for path, _, filenames in os.walk("./posts"):
    for filename in filenames:
        if not filename.endswith(".md"):
            continue
        from_path = os.path.join(path, filename)
        to_path = os.path.join(path, filename[: -len(".md")] + ".html")
        compile_md(from_path, to_path)

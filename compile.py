import os
import re

import requests
from jinja2 import Template


def render(dir_path, from_path, to_path, template):
    with open(from_path, "r") as f:
        s = f.read()

    s = parse_image_links(dir_path, s)
    s = parse_github(s)
    s = parse_template(template, s)

    with open(to_path, "w") as f:
        f.write(s)


def walk_md_files():
    for dir_path, _, filenames in os.walk("./posts"):
        for filename in filenames:
            if not filename.endswith(".md"):
                continue
            from_path = os.path.join(dir_path, filename)
            to_path = os.path.join(dir_path, filename[: -len(".md")] + ".html")
            yield dir_path, from_path, to_path


def parse_image_links(dir_path, s):
    for img_name in os.listdir(os.path.join(dir_path, "images")):
        url = "/".join(
            [
                "https://raw.githubusercontent.com",
                "coreygirard",
                "serverless-blog-content",
                "master",
                dir_path[2:],  # remove initial "./"
                "images",
                img_name,
            ]
        )
        s = s.replace(
            f"![]({img_name})", f'<img src="{url}" width="200" height="200" />'
        )
    return s


def parse_github(s):
    url = "https://api.github.com/markdown/raw"
    headers = {"Content-Type": "text/plain"}
    return requests.post(url, headers=headers, data=s).text


def parse_template(template, body):
    return template.render(body=body)


if __name__ == "__main__":
    with open("./templates/post.html.jinja", "r") as f:
        template = Template(f.read())

    for dir_path, from_path, to_path in walk_md_files():
        render(dir_path, from_path, to_path, template)

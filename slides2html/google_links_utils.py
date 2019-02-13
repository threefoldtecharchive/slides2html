
import re


def get_presentation_id(url):
    """
        https://docs.google.com/presentation/d/1N8YWE7ShqmhQphT6L29-AcEKZfZg2QripM4L0AK8mSU/edit#slide=id.g4c7fe486b7_0_0
        https://docs.google.com/presentation/d/1N8YWE7ShqmhQphT6L29-AcEKZfZg2QripM4L0AK8mSU/edit#slide=id.g4f00846b3a_0_0
        https://docs.google.com/presentation/d/1N8YWE7ShqmhQphT6L29-AcEKZfZg2QripM4L0AK8mSU/edit
    """

    res = re.findall("presentation/d/(.+?)/edit", url)
    if res:
        return res[0]
    return None


def get_slide_id(url):
    """
        https://docs.google.com/presentation/d/1N8YWE7ShqmhQphT6L29-AcEKZfZg2QripM4L0AK8mSU/edit#slide=id.g4c7fe486b7_0_0
        https://docs.google.com/presentation/d/1N8YWE7ShqmhQphT6L29-AcEKZfZg2QripM4L0AK8mSU/edit#slide=id.g4f00846b3a_0_0
        https://docs.google.com/presentation/d/1N8YWE7ShqmhQphT6L29-AcEKZfZg2QripM4L0AK8mSU/edit
    """
    res = re.findall("edit#slide=id.(.+?)$", url)
    if res:
        return res[0]
    return None


def link_info(url):
    if not url.startswith("http"):
        raise ValueError("invalid url.")
    presentation_id = get_presentation_id(url)
    slide_id = get_slide_id(url)
    if presentation_id is None:
        raise ValueError("invalid presentation url.")
    return presentation_id, slide_id

import re

from django import template
from apis_ontology.models import ZoteroEntry

register = template.Library()


@register.filter
def linebreak_split(value):
    if not value:
        return ""
    return value.splitlines()


@register.filter
def parse_comment(value):
    if not value:
        return ""
    pattern = r"<<(.*?) \[(.*?)\]>>"

    # subbed = re.sub(pattern, r'<a href="\2">\1</a>', value)
    # pattern = r"<<(.*?) \[([^\]]+)/([^]]+)]>>"

    # TODO: Where should it link?
    subbed = re.sub(
        pattern,
        r'<a target="_BLANK" href="https://www.zotero.org/groups/4394244/tibschol/items/\2/item-details#">\1</a>',
        value,
    )

    return subbed

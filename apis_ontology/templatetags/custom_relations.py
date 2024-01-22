from django import template
from apis_core.relations import utils
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from apis_ontology.tables import CustomRelationTableEdit, CustomRelationTableView
from django_tables2.tables import table_factory

register = template.Library()


@register.simple_tag
def custom_relations_table_edit(relationtype=None, instance=None, tocontenttype=None):
    """
    List all relations of type `relationtype` that go from `instance` to
    something with type `contenttype`.
    If no `tocontenttype` is passed, it lists all relations from and to
    instance.
    If no `relationtype` is passed, it lists all relations.
    """
    model = None
    existing_relations = list()

    if tocontenttype:
        model = tocontenttype.model_class()

    if relationtype:
        relation_types = [relationtype]
    else:
        # special case: when the contenttype is the same as the contenttype of
        # the instance, we don't want *all* the relations where the instance
        # occurs, but only those where it occurs together with another of its
        # type
        if instance and ContentType.objects.get_for_model(instance) == tocontenttype:
            relation_types = utils.relation_content_types(combination=(model, model))
        else:
            relation_types = utils.relation_content_types(any_model=model)

    for rel in relation_types:
        if instance:
            existing_relations.extend(
                list(
                    rel.model_class().objects.filter(Q(subj=instance) | Q(obj=instance))
                )
            )
        else:
            existing_relations.extend(list(rel.model_class().objects.all()))

    cssid = "table"
    if model:
        cssid += f"_{tocontenttype.name}"
    else:
        cssid += "_relations"
    attrs = {
        "class": "table table-hover table-striped table-condensed",
        "hx-swap-oob": "true",
        "id": cssid,
    }

    table = CustomRelationTableEdit
    if model:
        table = table_factory(model, CustomRelationTableEdit)
    return table(existing_relations, attrs=attrs)


@register.simple_tag
def custom_relations_table_view(relationtype=None, instance=None, tocontenttype=None):
    """
    List all relations of type `relationtype` that go from `instance` to
    something with type `contenttype`.
    If no `tocontenttype` is passed, it lists all relations from and to
    instance.
    If no `relationtype` is passed, it lists all relations.
    """
    model = None
    existing_relations = list()

    if tocontenttype:
        model = tocontenttype.model_class()

    if relationtype:
        relation_types = [relationtype]
    else:
        # special case: when the contenttype is the same as the contenttype of
        # the instance, we don't want *all* the relations where the instance
        # occurs, but only those where it occurs together with another of its
        # type
        if instance and ContentType.objects.get_for_model(instance) == tocontenttype:
            relation_types = utils.relation_content_types(combination=(model, model))
        else:
            relation_types = utils.relation_content_types(any_model=model)

    for rel in relation_types:
        if instance:
            existing_relations.extend(
                list(
                    rel.model_class().objects.filter(Q(subj=instance) | Q(obj=instance))
                )
            )
        else:
            existing_relations.extend(list(rel.model_class().objects.all()))

    cssid = "table"
    if model:
        cssid += f"_{tocontenttype.name}"
    else:
        cssid += "_relations"
    attrs = {
        "class": "table table-hover table-striped table-condensed",
        "hx-swap-oob": "true",
        "id": cssid,
    }

    table = CustomRelationTableView
    if model:
        table = table_factory(model, CustomRelationTableView)
    return table(existing_relations, attrs=attrs)

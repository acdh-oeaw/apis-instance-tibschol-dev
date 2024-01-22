import django_tables2 as tables
from apis_core.relations.tables import RelationTable
from apis_core.relations.models import Relation


class CustomRelationTableEdit(RelationTable):

    id = tables.TemplateColumn(
        "<a href='{% url 'apis:relationupdate' record.id %}'>{{ record.id }}</a>"
    )
    subject = tables.TemplateColumn("{{ record.subj }}")
    object = tables.TemplateColumn("{{ record.obj }}")
    description = tables.TemplateColumn("{{ record.name }}")
    edit = tables.TemplateColumn(
        "<a href='{% url 'apis:relationupdate' record.id %}'>Edit</a>"
    )
    delete = tables.TemplateColumn(template_name="tables/delete.html")

    class Meta:
        model = Relation
        fields = ["id", "subject", "description", "object", "edit"]
        sequence = tuple(fields)


class CustomRelationTableView(RelationTable):

    id = tables.TemplateColumn("{{ record.id }}")
    subject = tables.TemplateColumn("{{ record.subj }}")
    object = tables.TemplateColumn("{{ record.obj }}")
    description = tables.TemplateColumn("{{ record.name }}")

    class Meta:
        model = Relation
        fields = ["id", "subject", "description", "object"]
        exclude = ["edit", "delete"]
        sequence = tuple(fields)

import django_tables2 as tables
from apis_core.relations.tables import RelationTable
from apis_core.relations.models import Relation


class CustomRelationTableEdit(RelationTable):

    id = tables.TemplateColumn("{{ record.id }}")
    subject = tables.TemplateColumn(
        "<a href='/apis/entities/entity/{{ record.subject_type  }}/{{ record.subj.pk }}/detail'>{{record.subj}} ({{record.subj.pk}})</a>"
    )
    object = tables.TemplateColumn(
        "<a href='/apis/entities/entity/{{ record.object_type  }}/{{ record.obj.pk }}/detail'>{{record.obj}} ({{record.obj.pk}})</a>"
    )
    description = tables.TemplateColumn("{{ record.name }}")
    edit = tables.TemplateColumn(
        "<a href='{% url 'apis:relationupdate' record.id %}'>Edit</a>"
    )
    delete = tables.TemplateColumn(template_name="tables/delete.html")
    confidence = tables.TemplateColumn("{{ record.confidence }}")
    support_notes = tables.TemplateColumn(
        "{{ record.support_notes|default:''|truncatechars:30 }}\n{{record.notes|default:''|truncatechars:30}}"
    )
    tei_refs = tables.TemplateColumn("<a href='#{{record.tei_refs}}'>TEI</a>")
    zotero = tables.TemplateColumn("{{ record.zotero_refs|default:'' }}")

    class Meta:
        model = Relation
        fields = [
            "id",
            "subject",
            "description",
            "object",
            "confidence",
            "support_notes",
            "tei_refs",
            "zotero",
            "edit",
        ]
        exclude = ["confidence"]
        sequence = tuple(fields)


class CustomRelationTableView(RelationTable):

    id = tables.TemplateColumn("{{ record.id }}")
    subject = tables.TemplateColumn(
        "<a href='/apis/entities/entity/{{ record.subject_type  }}/{{ record.subj.pk }}/detail'>{{record.subj}} ({{record.subj.pk}})</a>"
    )
    object = tables.TemplateColumn(
        "<a href='/apis/entities/entity/{{ record.object_type  }}/{{ record.obj.pk }}/detail'>{{record.obj}} ({{record.obj.pk}})</a>"
    )
    description = tables.TemplateColumn("{{ record.name }}")
    confidence = tables.TemplateColumn("{{ record.confidence }}")
    support_notes = tables.TemplateColumn(
        "{{ record.support_notes|default:''|truncatechars:30 }}\n{{record.notes|default:''|truncatechars:30}}"
    )
    tei_refs = tables.TemplateColumn("<a href='#{{record.tei_refs}}'>TEI</a>")
    zotero = tables.TemplateColumn("{{ record.zotero_refs|default:'' }}")

    class Meta:
        model = Relation
        fields = [
            "id",
            "subject",
            "description",
            "object",
            "confidence",
            "support_notes",
            "zotero",
            "tei_refs",
        ]
        exclude = ["edit", "delete", "confidence"]
        sequence = tuple(fields)

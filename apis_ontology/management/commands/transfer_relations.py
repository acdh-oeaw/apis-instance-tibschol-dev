import logging

from apis_core.apis_relations.models import TempTriple
from django.core.management.base import BaseCommand
from tqdm.auto import tqdm
from django.apps import apps

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        all_triples = TempTriple.objects.all()
        for tt in tqdm(all_triples, unit="item"):
            obj_model = type(tt.obj).__name__
            subj_model = type(tt.subj).__name__
            prop = (
                tt.prop.name_forward.title()
                .replace(" ", "")
                .replace("(", "")
                .replace(")", "")
                .replace("/", "")
                .replace(",", "")
            )
            new_model_name = f"{subj_model}{prop}{obj_model}"
            # print(tt, obj_model, subj_model)
            new_model = apps.get_model(
                app_label="apis_ontology", model_name=new_model_name
            )
            new_rel = new_model.objects.filter(subj=tt.subj, obj=tt.obj).first()

            if new_rel is not None:
                continue

            new_rel = new_model(subj=tt.subj,
                                obj=tt.obj, notes=tt.notes, start_date=tt.start_date, start_start_date=tt.start_start_date,start_end_date=tt.start_end_date,start_date_written=tt.start_date_written,)

            # Save the object to the database
            new_rel.save()




        print("Temp triples copied into new relations classes")

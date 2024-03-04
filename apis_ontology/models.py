import logging

import reversion
from apis_core.apis_entities.models import TempEntityClass
from apis_core.apis_relations.models import Property, Triple
from django.db import models
from django.utils.functional import cached_property
from apis_core.relations.models import Relation

logger = logging.getLogger(__name__)


@reversion.register(follow=["tempentityclass_ptr"])
class Instance(TempEntityClass):
    class_uri = "http://id.loc.gov/ontologies/bibframe/Instance"
    SETS = [
        ("Set 1", "Set 1"),
        ("Set 2", "Set 2"),
        ("Set 3", "Set 3"),
        ("Set 4", "Set 4"),
    ]
    AVAILABILITY = [
        ("lost", "lost"),
        ("available", "available"),
        ("non-accessible", "non-accessible"),
    ]
    set_num = models.CharField(
        max_length=5, choices=SETS, null=True, blank=True, verbose_name="Set"
    )
    volume = models.CharField(max_length=255, blank=True, null=True)
    sb_text_number = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Number ascribed to item by Tibschol",
    )
    pp_kdsb = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Page numbers in print",
    )
    num_folios = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Number of folios"
    )

    signature_letter = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Signature letter (category)",
    )
    signature_number = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Signature number"
    )
    drepung_number = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Drepung catalogue number"
    )
    provenance = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Provenance"
    )
    comments = models.TextField(blank=True, null=True)
    external_link = models.TextField(
        blank=True, null=True, verbose_name="External links"
    )
    zotero_ref = models.TextField(blank=True, null=True, verbose_name="Zotero")

    @property
    def citation(self):
        if self.set_num == "Set 1":
            return f"bKa' gdams gsung ‘bum phyogs bsgrigs theng dang po, vol. {self.volume}, dPal brtsegs bod yig dpe rnying zhib 'jug khang [dPe sgrig 'gan 'khur ba: dByang can lha mo et al.], Chengdu [khreng tu’u]: Si khron mi rigs dpe skrun khang, 2006, pp. {self.pp_kdsb}."

        if self.set_num == "Set 2":
            return f"bKa' gdams gsung ‘bum phyogs bsgrigs theng gnyis pa, vol. {self.volume}, dPal brtsegs bod yig dpe rnying zhib 'jug khang [dPe sgrig 'gan 'khur ba: dByang can lha mo et al.], Chengdu [khreng tu’u]: Si khron mi rigs dpe skrun khang, 2007, pp. {self.pp_kdsb}."

        if self.set_num == "Set 3":
            return f"bKa' gdams gsung ‘bum phyogs bsgrigs theng gsum pa, vol. {self.volume}, dPal brtsegs bod yig dpe rnying zhib 'jug khang [dPe sgrig 'gan 'khur ba: dByang can lha mo et al.], Chengdu [khreng tu’u]: Si khron mi rigs dpe skrun khang, 2009, pp. {self.pp_kdsb}."

        if self.set_num == "Set 4":
            return f"bKa' gdams gsung ‘bum phyogs bsgrigs thengs bzhi pa, vol. {self.volume}, dPal brtsegs bod yig dpe rnying zhib 'jug khang [dPe sgrig 'gan 'khur ba: dByang can lha mo et al.], Chengdu [khreng tu’u]: Si khron mi rigs dpe skrun khang, 2015, pp. {self.pp_kdsb}."

        logger.warn(f"Unknown {self.set_num}. Cannot build citation.")
        return f"Unknown {self.set_num}. Cannot build citation."

    tibschol_ref = models.TextField(
        blank=True, null=True, verbose_name="Tibschol reference"
    )
    alternative_names = models.TextField(
        blank=True, null=True, verbose_name="Alternative names"
    )
    availability = models.CharField(
        max_length=15, choices=AVAILABILITY, blank=True, null=True
    )
    item_description = models.TextField(
        blank=True, null=True, verbose_name="Item description"
    )

    @cached_property
    def work(self):
        try:
            work_has_as_instance = WorkHasAsAnInstanceInstance.objects.filter(obj=self)
            return work_has_as_instance[0].subj
        except Exception as e:
            print("Error while fetching work associated with instance:", e)
            return

    @cached_property
    def author(self):
        try:
            return Work.objects.get(id=self.work.id).author
        except Exception as e:
            print("Error while getting author info for instance", e)
            return


@reversion.register(follow=["tempentityclass_ptr"])
class Person(TempEntityClass):
    class_uri = "http://id.loc.gov/ontologies/bibframe/Person"
    GENDERS = [
        ("male", "Male"),
        ("female", "Female"),
    ]
    NATIONALITY = [("Indic", "Indic"), ("Tibetan", "Tibetan")]
    gender = models.CharField(max_length=6, choices=GENDERS, default="male")
    comments = models.TextField(blank=True, null=True)
    external_link = models.TextField(
        blank=True, null=True, verbose_name="External links"
    )
    alternative_names = models.TextField(
        blank=True, null=True, verbose_name="Alternative names"
    )
    nationality = models.CharField(
        max_length=10, choices=NATIONALITY, blank=True, null=True
    )


@reversion.register(follow=["tempentityclass_ptr"])
class Work(TempEntityClass):
    LANGUAGES = [
        ("Sanskrit", "Sanskrit"),
        ("Tibetan", "Tibetan"),
        ("Tangut", "Tangut"),
        ("Other", "Other"),
    ]

    class_uri = "http://id.loc.gov/ontologies/bibframe/Work"
    subject = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="subject",
    )  # should be a controlled vocabulary field
    comments = models.TextField(blank=True, null=True)
    external_link = models.TextField(
        blank=True, null=True, verbose_name="External links"
    )
    alternative_names = models.TextField(
        blank=True, null=True, verbose_name="Alternative names"
    )
    sde_dge_ref = models.CharField(
        max_length=25, blank=True, null=True, verbose_name="Derge reference"
    )
    original_language = models.CharField(
        max_length=10, choices=LANGUAGES, blank=True, null=True
    )
    isExtant = models.BooleanField(default=True, verbose_name="Is extant")

    @cached_property
    def author(self):
        try:
            author = PersonAuthorOfWork.objects.filter(obj=self)
            return author[0].subj
        except Exception as e:
            print(e)
            return


@reversion.register(follow=["tempentityclass_ptr"])
class Place(TempEntityClass):
    class_uri = "http://id.loc.gov/ontologies/bibframe/Place"
    longitude = models.DecimalField(
        max_digits=22, decimal_places=16, blank=True, null=True
    )
    latitude = models.DecimalField(
        max_digits=22, decimal_places=16, blank=True, null=True
    )
    external_link = models.TextField(
        blank=True, null=True, verbose_name="External links"
    )
    comments = models.TextField(blank=True, null=True)
    alternative_names = models.TextField(
        blank=True, null=True, verbose_name="Alternative names"
    )


class ZoteroEntry(models.Model):
    zoteroId = models.CharField(max_length=255, verbose_name="Zotero ID")
    shortTitle = models.TextField(blank=True, null=True, verbose_name="Short title")
    fullCitation = models.TextField(blank=True, null=True, verbose_name="Full Citation")
    year = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Year of publication"
    )


class TibScholRelation(models.Model):
    CONFIDENCE = [
        ("Positive", "Positive"),
        ("Uncertain", "Uncertain"),
        ("Negative", "Negative"),
    ]

    zotero_refs = models.TextField(blank=True, null=True, verbose_name="Zotero")
    tei_refs = models.TextField(blank=True, null=True, verbose_name="Excerpts")
    support_notes = models.TextField(
        blank=True, null=True, verbose_name="Support notes"
    )
    confidence = models.CharField(
        blank=True,
        null=True,
        default="Positive",
        choices=CONFIDENCE,
        verbose_name="Confidence",
        max_length=1000,
    )
    start_date = models.DateField(blank=True, null=True, editable=False)
    start_start_date = models.DateField(blank=True, null=True, editable=False)
    start_end_date = models.DateField(blank=True, null=True, editable=False)
    end_date = models.DateField(blank=True, null=True, editable=False)
    end_start_date = models.DateField(blank=True, null=True, editable=False)
    end_end_date = models.DateField(blank=True, null=True, editable=False)
    start_date_written = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Start",
    )
    end_date_written = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="End",
    )
    notes = models.TextField(blank=True, null=True)

    temptriple_field_list = [
        "notes",
        "start_date",
        "start_start_date",
        "start_end_date",
        "end_date",
        "end_start_date",
        "end_end_date",
        "start_date_written",
        "end_date_written",
    ]

    @property
    def subject_type(self):
        return str(self.subj_model.__name__).lower()

    @property
    def object_type(self):
        return str(self.obj_model.__name__).lower()

    class Meta:
        abstract = True


class PersonActiveAtPlace(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Place
    name = "active at"
    reverse_name = "place of activity of"
    temptriple_name = "active at"
    temptriple_name_reverse = "place of activity of"


class PersonAddresseeOfWork(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Work
    name = "addressee of"
    reverse_name = "addressed to"
    temptriple_name = "addressee of"
    temptriple_name_reverse = "addressed to"


class PersonAuntMaternalPaternalOfPerson(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Person
    name = "aunt (maternal/paternal) of"
    reverse_name = "nephew (maternal/paternal) of"
    temptriple_name = "aunt (maternal/paternal) of"
    temptriple_name_reverse = "nephew (maternal/paternal) of"


class PersonAuthorOfWork(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Work
    name = "author of"
    reverse_name = "composed by"
    temptriple_name = "author of"
    temptriple_name_reverse = "composed by"


class PersonBiographedInWork(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Work
    name = "biographed in"
    reverse_name = "biography of"
    temptriple_name = "biographed in"
    temptriple_name_reverse = "biography of"


class PersonBiographerOfPerson(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Person
    name = "biographer of"
    reverse_name = "biographed by"
    temptriple_name = "biographer of"
    temptriple_name_reverse = "biographed by"


class PersonCitesWork(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Work
    name = "cites"
    reverse_name = "is cited by"
    temptriple_name = "cites"
    temptriple_name_reverse = "is cited by"


class WorkCommentaryOnWork(Relation, TibScholRelation):
    subj_model = Work
    obj_model = Work
    name = "commentary on"
    reverse_name = "has as a commentary"
    temptriple_name = "commentary on"
    temptriple_name_reverse = "has as a commentary"


class WorkComposedAtPlace(Relation, TibScholRelation):
    subj_model = Work
    obj_model = Place
    name = "composed at"
    reverse_name = "place of composition for"
    temptriple_name = "composed at"
    temptriple_name_reverse = "place of composition for"


class WorkContainsCitationsOfWork(Relation, TibScholRelation):
    subj_model = Work
    obj_model = Work
    name = "contains citations of"
    reverse_name = "is cited in"
    temptriple_name = "contains citations of"
    temptriple_name_reverse = "is cited in"


class InstanceCopiedWrittenDownAtPlace(Relation, TibScholRelation):
    subj_model = Instance
    obj_model = Place
    name = "copied/written down at"
    reverse_name = "place of scribing for"
    temptriple_name = "copied/written down at"
    temptriple_name_reverse = "place of scribing for"


class PersonDirectPredecessorInLineageOfPerson(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Person
    name = "direct predecessor (in lineage) of"
    reverse_name = "direct successor (in lineage) of"
    temptriple_name = "direct predecessor (in lineage) of"
    temptriple_name_reverse = "direct successor (in lineage) of"
    subject_of_teaching = (
        models.CharField(  # TODO: Controlled vocabulary with Work.Subject
            max_length=255,
            blank=True,
            null=True,
            verbose_name="subject of teaching",
        )
    )


class PersonDiscipleOfPerson(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Person
    name = "disciple of"
    reverse_name = "spiritual teacher of"
    temptriple_name = "disciple of"
    temptriple_name_reverse = "spiritual teacher of"
    subject_of_teaching = (
        models.CharField(  # TODO: Controlled vocabulary with Work.Subject
            max_length=255,
            blank=True,
            null=True,
            verbose_name="subject of teaching",
        )
    )


class PersonEditorOfInstance(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Instance
    name = "editor of"
    reverse_name = "edited by"
    temptriple_name = "editor of"
    temptriple_name_reverse = "edited by"


class PersonFellowMonkOfPerson(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Person
    name = "fellow monk of"
    reverse_name = "fellow monk of"
    temptriple_name = "fellow monk of"
    temptriple_name_reverse = "fellow monk of"


class PersonFellowStudentOfPerson(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Person
    name = "fellow student of"
    reverse_name = "fellow student of"
    temptriple_name = "fellow student of"
    temptriple_name_reverse = "fellow student of"


class WorkHasAsAnInstanceInstance(Relation, TibScholRelation):
    subj_model = Work
    obj_model = Instance
    name = "has as an instance"
    reverse_name = "instance of"
    temptriple_name = "has as an instance"
    temptriple_name_reverse = "instance of"


class PersonHasOtherTypeOfPersonalRelationToPerson(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Person
    name = "has other type of personal relation to"
    reverse_name = "has other type of personal relation to"
    temptriple_name = "has other type of personal relation to"
    temptriple_name_reverse = "has other type of personal relation to"


class PersonIllustratorOfInstance(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Instance
    name = "illustrator of"
    reverse_name = "illustrated by"
    temptriple_name = "illustrator of"
    temptriple_name_reverse = "illustrated by"


class InstanceIsCopiedFromInstance(Relation, TibScholRelation):
    subj_model = Instance
    obj_model = Instance
    name = "is copied from"
    reverse_name = "is source for"
    temptriple_name = "is copied from"
    temptriple_name_reverse = "is source for"


class PlaceIsLocatedWithinPlace(Relation, TibScholRelation):
    subj_model = Place
    obj_model = Place
    name = "is located within"
    reverse_name = "contains"
    temptriple_name = "is located within"
    temptriple_name_reverse = "contains"


class PersonLenderOfInstance(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Instance
    name = "lender of"
    reverse_name = "lent by"
    temptriple_name = "lender of"
    temptriple_name_reverse = "lent by"


class WorkNamesPerson(Relation, TibScholRelation):
    subj_model = Work
    obj_model = Person
    name = "names"
    reverse_name = "is named in"
    temptriple_name = "names"
    temptriple_name_reverse = "is named in"


class WorkNamesWork(Relation, TibScholRelation):
    subj_model = Work
    obj_model = Work
    name = "names"
    reverse_name = "is named in"
    temptriple_name = "names"
    temptriple_name_reverse = "is named in"


class PersonOrdinatorOfPerson(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Person
    name = "ordinator of"
    reverse_name = "ordained by"
    temptriple_name = "ordinator of"
    temptriple_name_reverse = "ordained by"


class PersonOwnerOfInstance(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Instance
    name = "owner of"
    reverse_name = "owned by"
    temptriple_name = "owner of"
    temptriple_name_reverse = "owned by"


class PersonParentOfPerson(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Person
    name = "parent of"
    reverse_name = "child of"
    temptriple_name = "parent of"
    temptriple_name_reverse = "child of"


class PersonPatronOfPerson(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Person
    name = "patron of"
    reverse_name = "protegee of"
    temptriple_name = "patron of"
    temptriple_name_reverse = "protegee of"


class PersonPromoterOfWork(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Work
    name = "promoter of"
    reverse_name = "promoted by"
    temptriple_name = "promoter of"
    temptriple_name_reverse = "promoted by"


class PersonPrompterOfWork(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Work
    name = "prompter of"
    reverse_name = "prompted by"
    temptriple_name = "prompter of"
    temptriple_name_reverse = "prompted by"


class WorkQuotesWithNameTheViewsOfPerson(Relation, TibScholRelation):
    subj_model = Work
    obj_model = Person
    name = "quotes (with name) the views of"
    reverse_name = "has views quoted (with name) in"
    temptriple_name = "quotes (with name) the views of"
    temptriple_name_reverse = "has views quoted (with name) in"


class WorkQuotesWithoutNameTheViewsOfPerson(Relation, TibScholRelation):
    subj_model = Work
    obj_model = Person
    name = "quotes (without name) the views of"
    reverse_name = "has views quoted (without name) in"
    temptriple_name = "quotes (without name) the views of"
    temptriple_name_reverse = "has views quoted (without name) in"


class WorkRecordsTheTeachingOfPerson(Relation, TibScholRelation):
    subj_model = Work
    obj_model = Person
    name = "records the teaching of"
    reverse_name = "has their teaching recorded in"
    temptriple_name = "records the teaching of"
    temptriple_name_reverse = "has their teaching recorded in"


class PersonRefersWithNameToTheViewsOfPerson(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Person
    name = "refers (with name) to the views of"
    reverse_name = "has views referred to (with name) by"
    temptriple_name = "refers (with name) to the views of"
    temptriple_name_reverse = "has views referred to (with name) by"
    subject_of_teaching = (
        models.CharField(  # TODO: Controlled vocabulary with Work.Subject
            max_length=255,
            blank=True,
            null=True,
            verbose_name="subject of teaching",
        )
    )


class PersonRefersWithoutNameToTheViewsOfPerson(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Person
    name = "refers (without name) to the views of"
    reverse_name = "has views referred to (without name) by"
    temptriple_name = "refers (without name) to the views of"
    temptriple_name_reverse = "has views referred to (without name) by"
    subject_of_teaching = (
        models.CharField(  # TODO: Controlled vocabulary with Work.Subject
            max_length=255,
            blank=True,
            null=True,
            verbose_name="subject of teaching",
        )
    )


class PersonRequestorOfPerson(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Person
    name = "requestor of"
    reverse_name = "requested by"
    temptriple_name = "requestor of"
    temptriple_name_reverse = "requested by"
    subject_of_teaching = (
        models.CharField(  # TODO: Controlled vocabulary with Work.Subject
            max_length=255,
            blank=True,
            null=True,
            verbose_name="subject of teaching",
        )
    )


class PersonScribeOfInstance(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Instance
    name = "scribe of"
    reverse_name = "copied/written down by"
    temptriple_name = "scribe of"
    temptriple_name_reverse = "copied/written down by"


class PersonSiblingOfPerson(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Person
    name = "sibling of"
    reverse_name = "sibling of"
    temptriple_name = "sibling of"
    temptriple_name_reverse = "sibling of"


class PersonSpiritualFriendOfPerson(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Person
    name = "spiritual friend of"
    reverse_name = "has as spiritual friend"
    temptriple_name = "spiritual friend of"
    temptriple_name_reverse = "has as spiritual friend"


class PersonSponsorOfInstance(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Instance
    name = "sponsor of"
    reverse_name = "sponsored by"
    temptriple_name = "sponsor of"
    temptriple_name_reverse = "sponsored by"


class PersonStudentOfPerson(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Person
    name = "student of"
    reverse_name = "teacher of"
    temptriple_name = "student of"
    temptriple_name_reverse = "teacher of"
    subject_of_teaching = (
        models.CharField(  # TODO: Controlled vocabulary with Work.Subject
            max_length=255,
            blank=True,
            null=True,
            verbose_name="subject of teaching",
        )
    )


class PersonStudiedWork(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Work
    name = "studied"
    reverse_name = "studied by"
    temptriple_name = "studied"
    temptriple_name_reverse = "studied by"


class PersonTeachesWork(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Work
    name = "teaches"
    reverse_name = "taught by"
    temptriple_name = "teaches"
    temptriple_name_reverse = "taught by"


class PersonUncleMaternalPaternalOfPerson(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Person
    name = "uncle (maternal/paternal) of"
    reverse_name = "nephew (maternal/paternal) of"
    temptriple_name = "uncle (maternal/paternal) of"
    temptriple_name_reverse = "nephew (maternal/paternal) of"


class WorkTaughtAtPlace(Relation, TibScholRelation):
    subj_model = Work
    obj_model = Place
    name = "taught at"
    reverse_name = "place of teaching of"


class PersonTranslatorOfWork(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Work
    name = "translator of"
    reverse_name = "translated by"


class PersonAnnotatorOfWork(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Work
    name = "annotator of"
    reverse_name = "annotated by"

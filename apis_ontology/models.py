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
    zotero_ref = models.CharField(max_length=255, blank=True, null=True)

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
            WORK_REL = Property.objects.get(name="has as an instance")
            work = Triple.objects.filter(prop=WORK_REL, obj=self)
            return work[0].subj
        except Exception as e:
            return

    @cached_property
    def author(self):
        try:
            print(self.work, self.work.author)
            return self.work.author
        except Exception as e:
            print(e)
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
            # TODO: Should this be within property?
            AUTHOR_REL = Property.objects.get(name="author of")
            author = Triple.objects.filter(prop=AUTHOR_REL, obj=self)
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

    class Meta:
        abstract = True


class PersonActiveAtPlace(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Place
    name = "active at"
    name_reverse = "place of activity of"


class PersonAddresseeOfWork(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Work
    name = "addressee of"
    name_reverse = "addressed to"


class PersonAuntMaternalPaternalOfPerson(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Person
    name = "aunt (maternal/paternal) of"
    name_reverse = "nephew (maternal/paternal) of"


class PersonAuthorOfWork(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Work
    name = "author of"
    name_reverse = "composed by"


class PersonBiographedInWork(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Work
    name = "biographed in"
    name_reverse = "biography of"


class PersonBiographerOfPerson(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Person
    name = "biographer of"
    name_reverse = "biographed by"


class PersonCitesWork(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Work
    name = "cites"
    name_reverse = "is cited by"


class WorkCommentaryOnWork(Relation, TibScholRelation):
    subj_model = Work
    obj_model = Work
    name = "commentary on"
    name_reverse = "has as a commentary"


class WorkComposedAtPlace(Relation, TibScholRelation):
    subj_model = Work
    obj_model = Place
    name = "composed at"
    name_reverse = "place of composition for"


class WorkContainsCitationsOfWork(Relation, TibScholRelation):
    subj_model = Work
    obj_model = Work
    name = "contains citations of"
    name_reverse = "is cited in"


class InstanceCopiedWrittenDownAtPlace(Relation, TibScholRelation):
    subj_model = Instance
    obj_model = Place
    name = "copied/written down at"
    name_reverse = "place of scribing for"


class PersonDirectPredecessorInLineageOfPerson(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Person
    name = "direct predecessor (in lineage) of"
    name_reverse = "direct successor (in lineage) of"


class PersonDiscipleOfPerson(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Person
    name = "disciple of"
    name_reverse = "spiritual teacher of"


class PersonEditorOfInstance(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Instance
    name = "editor of"
    name_reverse = "edited by"


class PersonFellowMonkOfPerson(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Person
    name = "fellow monk of"
    name_reverse = "fellow monk of"


class PersonFellowStudentOfPerson(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Person
    name = "fellow student of"
    name_reverse = "fellow student of"


class WorkHasAsAnInstanceInstance(Relation, TibScholRelation):
    subj_model = Work
    obj_model = Instance
    name = "has as an instance"
    name_reverse = "instance of"


class PersonHasOtherTypeOfPersonalRelationToPerson(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Person
    name = "has other type of personal relation to"
    name_reverse = "has other type of personal relation to"


class PersonIllustratorOfInstance(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Instance
    name = "illustrator of"
    name_reverse = "illustrated by"


class InstanceIsCopiedFromInstance(Relation, TibScholRelation):
    subj_model = Instance
    obj_model = Instance
    name = "is copied from"
    name_reverse = "is source for"


class PlaceIsLocatedWithinPlace(Relation, TibScholRelation):
    subj_model = Place
    obj_model = Place
    name = "is located within"
    name_reverse = "contains"


class PersonLenderOfInstance(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Instance
    name = "lender of"
    name_reverse = "lent by"


class WorkNamesPerson(Relation, TibScholRelation):
    subj_model = Work
    obj_model = Person
    name = "names"
    name_reverse = "is named in"


class WorkNamesWork(Relation, TibScholRelation):
    subj_model = Work
    obj_model = Work
    name = "names"
    name_reverse = "is named in"


class PersonOrdinatorOfPerson(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Person
    name = "ordinator of"
    name_reverse = "ordained by"


class PersonOwnerOfInstance(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Instance
    name = "owner of"
    name_reverse = "owned by"


class PersonParentOfPerson(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Person
    name = "parent of"
    name_reverse = "child of"


class PersonPatronOfPerson(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Person
    name = "patron of"
    name_reverse = "protegee of"


class PersonPromoterOfWork(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Work
    name = "promoter of"
    name_reverse = "promoted by"


class PersonPrompterOfWork(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Work
    name = "prompter of"
    name_reverse = "prompted by"


class WorkQuotesWithNameTheViewsOfPerson(Relation, TibScholRelation):
    subj_model = Work
    obj_model = Person
    name = "quotes (with name) the views of"
    name_reverse = "has views quoted (with name) in"


class WorkQuotesWithoutNameTheViewsOfPerson(Relation, TibScholRelation):
    subj_model = Work
    obj_model = Person
    name = "quotes (without name) the views of"
    name_reverse = "has views quoted (without name) in"


class WorkRecordsTheTeachingOfPerson(Relation, TibScholRelation):
    subj_model = Work
    obj_model = Person
    name = "records the teaching of"
    name_reverse = "has their teaching recorded in"


class PersonRefersWithNameToTheViewsOfPerson(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Person
    name = "refers (with name) to the views of"
    name_reverse = "has views referred to (with name) by"


class PersonRefersWithoutNameToTheViewsOfPerson(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Person
    name = "refers (without name) to the views of"
    name_reverse = "has views referred to (without name) by"


class PersonRequestorOfPerson(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Person
    name = "requestor of"
    name_reverse = "requested by"


class PersonScribeOfInstance(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Instance
    name = "scribe of"
    name_reverse = "copied/written down by"


class PersonSiblingOfPerson(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Person
    name = "sibling of"
    name_reverse = "sibling of"


class PersonSpiritualFriendOfPerson(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Person
    name = "spiritual friend of"
    name_reverse = "has as spiritual friend"


class PersonSponsorOfInstance(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Instance
    name = "sponsor of"
    name_reverse = "sponsored by"


class PersonStudentOfPerson(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Person
    name = "student of"
    name_reverse = "teacher of"


class PersonStudiedWork(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Work
    name = "studied"
    name_reverse = "studied by"


class PersonTeachesWork(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Work
    name = "teaches"
    name_reverse = "taught by"


class PersonUncleMaternalPaternalOfPerson(Relation, TibScholRelation):
    subj_model = Person
    obj_model = Person
    name = "uncle (maternal/paternal) of"
    name_reverse = "nephew (maternal/paternal) of"

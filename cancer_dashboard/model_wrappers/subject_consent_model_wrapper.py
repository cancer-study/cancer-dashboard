from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from edc_model_wrapper import ModelWrapper

from .subject_screening_model_wrapper import SubjectScreeningModelWrapper


class SubjectConsentModelWrapper(ModelWrapper):

    screening_model_wrapper_cls = SubjectScreeningModelWrapper
    model = 'cancer_subject.subjectconsent'
    next_url_name = settings.DASHBOARD_URL_NAMES.get('subject_listboard_url')
    next_url_attrs = ['subject_identifier']
    querystring_attrs = ['gender', 'first_name', 'initials', 'modified']

    @property
    def subject_screening_model_obj(self):
        """Returns a subject screening model instance or None.
        """
        try:
            return self.subject_screening_cls.objects.get(**self.subject_screening_options)
        except ObjectDoesNotExist:
            return None

    @property
    def subject_screening(self):
        """Returns a wrapped saved or unsaved subject screening.
        """
        model_obj = self.subject_screening_model_obj or self.subject_screening_cls(
            **self.create_subject_screening_options)
        return SubjectScreeningModelWrapper(model_obj=model_obj)

    @property
    def subject_screening_cls(self):
        return django_apps.get_model('cancer_subject.subjectscreening')

    @property
    def create_subject_screening_options(self):
        """Returns a dictionary of options to create a new
        unpersisted cancer subject model instance.
        """
        options = dict(
            subject_identifier=self.subject_identifier)
        return options

    @property
    def subject_screening_options(self):
        """Returns a dictionary of options to get an existing
        subject screening model instance.
        """
        options = dict(
            subject_identifier=self.subject_identifier)
        return options

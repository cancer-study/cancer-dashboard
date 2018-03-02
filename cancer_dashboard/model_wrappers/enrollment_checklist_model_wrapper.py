from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
from edc_consent import ConsentModelWrapperMixin

from edc_model_wrapper import ModelWrapper

from .subject_consent_model_wrapper import SubjectConsentModelWrapper


class EnrollmentChecklistModelWrapper(ConsentModelWrapperMixin, ModelWrapper):

    consent_model_wrapper_cls = SubjectConsentModelWrapper
    model = 'cancer_subject.enrollmentchecklist'
    next_url_name = django_apps.get_app_config(
        'cancer_dashboard').checklist_listboard_url_name
    next_url_attrs = ['subject_identifier']
    querystring_attrs = ['gender']

    @property
    def html_reason(self):
        if not self.eligible:
            html = '<BR>'.join(self.object.reasons_ineligible.split(','))
            return mark_safe('<BR>'.join(['No:', html]))
        else:
            return 'Yes.'

    @property
    def consented(self):
        return self.object.subject_identifier

    @property
    def consent_model_obj(self):
        consent_model_cls = django_apps.get_model(
            self.consent_model_wrapper_cls.model)
        try:
            return consent_model_cls.objects.get(**self.consent_options)
        except ObjectDoesNotExist:
            return None

from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.base import ContextMixin
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.views import DashboardView as BaseDashboardView
from edc_subject_dashboard.view_mixins import SubjectDashboardViewMixin

from edc_navbar import NavbarViewMixin

from ....model_wrappers import (
    SubjectVisitModelWrapper, SubjectConsentModelWrapper,
    SubjectScreeningModelWrapper, AppointmentModelWrapper,
    SubjectLocatorModelWrapper)


class AddSubjectScreening(ContextMixin):

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(subject_screening=self.subject_screening)
        return context


class DashboardView(
        AddSubjectScreening, EdcBaseViewMixin,
        SubjectDashboardViewMixin, NavbarViewMixin,
        BaseDashboardView):

    dashboard_url = 'subject_dashboard_url'
    dashboard_template = 'subject_dashboard_template'
    appointment_model = 'cancer_subject.appointment'
    appointment_model_wrapper_cls = AppointmentModelWrapper
    consent_model = 'cancer_subject.subjectconsent'
    consent_model_wrapper_cls = SubjectConsentModelWrapper
    navbar_name = 'cancer_dashboard'
    navbar_selected_item = 'consented_subject'
    subject_locator_model = 'edc_locator.subjectlocator'
    subject_locator_model_wrapper_cls = SubjectLocatorModelWrapper
    visit_model_wrapper_cls = SubjectVisitModelWrapper
    special_forms_include_value = "cancer_dashboard/subject/dashboard/special_forms.html"

# from django.apps import apps as django_apps
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.views import DashboardView as BaseDashboardView
from edc_navbar import NavbarViewMixin
from edc_subject_dashboard.view_mixins import SubjectDashboardViewMixin


from .visit_schedule_view_mixin import VisitScheduleViewMixin
# from ....model_wrappers import CrfModelWrapper, RequisitionModelWrapper
from ....model_wrappers import SubjectVisitModelWrapper, SubjectConsentModelWrapper
from ....model_wrappers import AppointmentModelWrapper, SubjectLocatorModelWrapper
# from .base_dashboard_view import BaseDashboardView


class DashboardView(
        EdcBaseViewMixin, VisitScheduleViewMixin,
        SubjectDashboardViewMixin,
        NavbarViewMixin, BaseDashboardView):

    dashboard_url = 'subject_dashboard_url'
    dashboard_template = 'subject_dashboard_template'
    appointment_model = 'edc_appointment.appointment'
    appointment_model_wrapper_cls = AppointmentModelWrapper
    consent_model = 'cancer_subject.subjectconsent'
    consent_model_wrapper_cls = SubjectConsentModelWrapper
    navbar_name = 'cancer_dashboard'
    navbar_selected_item = 'consented_subject'
#     offstudy_model = 'cancer_subject.subjectoffstudy'
#     crf_model_wrapper_cls = CrfModelWrapper
#     requisition_model_wrapper_cls = RequisitionModelWrapper
    subject_locator_model = 'edc_locator.subjectlocator'
    subject_locator_model_wrapper_cls = SubjectLocatorModelWrapper
    visit_model_wrapper_cls = SubjectVisitModelWrapper

#     @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         dashboard_url_name = django_apps.get_app_config(
#             'cancer_dashboard').dashboard_url_name
#         context.update(
#             subject_offstudy=self.subject_offstudy,
#             dashboard_url_name=dashboard_url_name)
#         return context
#
#     def offstudy_required(self):
#         """ OffStudy evaluation criteria, result True or False. """
#         return False

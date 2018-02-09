from django.test import TestCase, tag
from edc_model_wrapper.tests import ModelWrapperTestHelper

from ..model_wrappers import AppointmentModelWrapper
# from ..model_wrappers import RequisitionModelWrapper
# from ..model_wrappers import SubjectConsentModelWrapper
# from ..model_wrappers import SubjectLocatorModelWrapper
# from ..model_wrappers import SubjectVisitModelWrapper
# from .models import Appointment, SubjectVisit


class TestModelWrappers(TestCase):

    model_wrapper_helper_cls = ModelWrapperTestHelper

    def test_1(self):
        pass

#     def test_subject_consent(self):
#         helper = self.model_wrapper_helper_cls(
#             model_wrapper=SubjectConsentModelWrapper,
#             app_label='cancer_dashboard',
#             subject_identifier='092-12345',
#             subject_screening=subject_screening)
#         helper.test(self)

#     def test_subject_locator(self):
#         helper = self.model_wrapper_helper_cls(
#             model_wrapper=SubjectLocatorModelWrapper,
#             app_label='cancer_dashboard',
#             subject_identifier='092-12345')
#         helper.test(self)
#
#     def test_appointment(self):
#         helper = self.model_wrapper_helper_cls(
#             model_wrapper=AppointmentModelWrapper,
#             app_label='cancer_dashboard',
#             subject_identifier='092-12345')
#         helper.test(self)
#
#     def test_subject_visit(self):
#         appointment = Appointment.objects.create(
#             subject_identifier='092-12345',)
#         helper = self.model_wrapper_helper_cls(
#             model_wrapper=SubjectVisitModelWrapper,
#             app_label='cancer_dashboard',
#             subject_identifier='092-12345',
#             appointment=appointment)
#         helper.test(self)
#
#     def test_subject_requisition(self):
#         appointment = Appointment.objects.create(
#             subject_identifier='092-12345')
#         subject_visit = SubjectVisit.objects.create(
#             subject_identifier='092-12345',
#             appointment=appointment)
#         helper = self.model_wrapper_helper_cls(
#             model_wrapper=RequisitionModelWrapper,
#             app_label='cancer_dashboard',
#             subject_visit=subject_visit)
#         helper.test(self)

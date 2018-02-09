from cancer_subject.models import Appointment
from edc_appointment.view_mixins import AppointmentViewMixin as BaseAppointmentMixin

from ....model_wrappers import AppointmentModelWrapper


class AppointmentViewMixin(BaseAppointmentMixin):

    appointment_model_wrapper_cls = AppointmentModelWrapper

    def empty_appointment(self, **kwargs):
        return Appointment()

    @property
    def appointment_model(self):
        return Appointment

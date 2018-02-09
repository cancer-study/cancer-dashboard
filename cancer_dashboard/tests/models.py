from django.db import models
from edc_base.model_mixins import BaseUuidModel


class Appointment(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)


class SubjectVisit(BaseUuidModel):

    appointment = models.OneToOneField(
        Appointment, on_delete=models.PROTECT)

    subject_identifier = models.CharField(max_length=25)


class SubjectRequisition(BaseUuidModel):

    subject_visit = models.ForeignKey(
        SubjectVisit, on_delete=models.PROTECT)

    panel_name = models.CharField(max_length=25)


class EnrollmentChecklist(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)


class SubjectConsent(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    gender = models.CharField(max_length=25, default='M')

    initials = models.CharField(max_length=25, default='XX')

    first_name = models.CharField(max_length=25, default='NOAM')


class SubjectLocator(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

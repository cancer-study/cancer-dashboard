from .crf_model_wrapper import CrfModelWrapper


class RequisitionModelWrapper(CrfModelWrapper):

    model = 'cancer_subject.subjectrequisition'
    requisition_panel_name = None
    next_url_attrs = ['appointment', 'subject_identifier']
    querystring_attrs = ['subject_visit', 'panel_name']

    @property
    def appointment(self):
        try:
            return str(self.object.subject_visit.appointment.id)
        except AttributeError:
            return ''

    @property
    def subject_identifier(self):
        return self.object.subject_visit.subject_identifier

    @property
    def panel_name(self):
        return self.requisition_panel_name

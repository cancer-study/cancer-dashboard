import re

from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import ListboardFilterViewMixin
from edc_dashboard.views import ListboardView
from edc_navbar import NavbarViewMixin

from cancer_dashboard.views.screening.filters import ListboardViewFilters

from ...model_wrappers import SubjectEligibilityModelWrapper


class SubjectEligibilityListBoardView(EdcBaseViewMixin, NavbarViewMixin,
                                      ListboardFilterViewMixin, ListboardView):

    listboard_template = 'screening_listboard_template'
    listboard_url = 'subject_listboard_url'
    listboard_panel_style = 'info'
    listboard_fa_icon = "fa-user-plus"

    app_config_name = 'cancer_dashboard'
    listboard_view_filters = ListboardViewFilters()
    model = 'cancer_subject.subjecteligibility'
    model_wrapper_cls = SubjectEligibilityModelWrapper
    navbar_name = 'cancer_dashboard'
    navbar_selected_item = 'subject_eligibility'
    ordering = '-modified'
    paginate_by = 10
    search_form_url = 'subject_listboard_url'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_template_names(self):
        return [django_apps.get_app_config(
            self.app_config_name).checklist_listboard_template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            enrollment_checklist_add_url=self.model_cls().get_absolute_url())
        return context

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        if kwargs.get('subject_identifier'):
            options.update(
                {'subject_identifier': kwargs.get('subject_identifier')})
        return options

    def extra_search_options(self, search_term):
        q = Q()
        if re.match('^[A-Z]+$', search_term):
            q = Q(first_name__exact=search_term)
        return q

import re

from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import AppConfigViewMixin, ListboardFilterViewMixin
from edc_dashboard.views import ListboardView

from cancer_dashboard.views.checklist.filters import ListboardViewFilters

from ...model_wrappers import EnrollmentChecklistModelWrapper


class EnrollmentCheckListBoardView(AppConfigViewMixin, EdcBaseViewMixin,
                                   ListboardFilterViewMixin, ListboardView):

    model = 'cancer_subject.enrollmentchecklist'
    model_wrapper_cls = EnrollmentChecklistModelWrapper
    listboard_url_name = django_apps.get_app_config(
        'cancer_dashboard').checklist_listboard_url_name
    paginate_by = 10
    app_config_name = 'cancer_dashboard'
    ordering = '-modified'
    listboard_view_filters = ListboardViewFilters()

    navbar_name = 'cancer_dashboard'
    navbar_selected_item = 'enrollment_checklist'

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

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
from datetime import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, UpdateView, View
import tablib
from .forms import ContactModelForm, generate_submission_form
from .models import *
from .filters import *

COMPLETION_STATUS = (
    (0, 'Complete'),
    (1, 'Partial'),
    (2, 'Empty'),
)

export_formats = ['csv', 'xls', 'xlsx', 'ods']


class TemplatePreview(TemplateView):
    page_title = ''

    def dispatch(self, request, *args, **kwargs):
        self.template_name = kwargs['template_name']
        return super(TemplateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TemplatePreview, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context


class DashboardView(TemplateView):
    template_name = 'core/dashboard.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.page_title = 'Dashboard'
        return super(DashboardView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context


class SubmissionAnalysisView(TemplateView):
    template_name = 'core/checklist_analysis.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.page_title = 'Elections Checklist Analysis'
        return super(SubmissionAnalysisView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SubmissionAnalysisView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context


class SubmissionListView(ListView):
    context_object_name = 'submissions'
    template_name = 'core/submission_list.html'
    paginate_by = settings.PAGE_SIZE
    page_title = ''

    def get_queryset(self):
        self.page_title = self.form.name
        return self.filter_set.qs.order_by('-date', 'observer__observer_id')

    def get_context_data(self, **kwargs):
        context = super(SubmissionListView, self).get_context_data(**kwargs)
        context['form'] = self.form
        context['filter_form'] = self.filter_set.form
        context['page_title'] = self.page_title
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.form = get_object_or_404(Form, pk=kwargs['form'])
        self.submission_filter = generate_submission_filter(self.form)
        return super(SubmissionListView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.filter_set = self.submission_filter(self.request.POST,
            queryset=Submission.objects.filter(form=self.form).exclude(observer=None))
        request.session['submission_filter_%d' % self.form.pk] = self.filter_set.form.data
        return super(SubmissionListView, self).get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        initial_data = request.session.get('submission_filter_%d' % self.form.pk, None)
        self.filter_set = self.submission_filter(initial_data,
            queryset=Submission.objects.filter(form=self.form).exclude(observer=None))
        return super(SubmissionListView, self).get(request, *args, **kwargs)


class SubmissionEditView(UpdateView):
    template_name = 'core/submission_edit.html'
    page_title = 'Submission Edit'

    def get_object(self, queryset=None):
        return self.submission.master if self.submission.form.type == 'CHECKLIST' else self.submission

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.submission = get_object_or_404(Submission, pk=kwargs['pk'])
        self.form_class = generate_submission_form(self.submission.form)

        # submission_form_class allows for the rendering of form elements that are readonly
        # and disabled by default. It's only useful for rendering submission and submission
        # sibling records. Only the master submission should be editable.
        self.submission_form_class = generate_submission_form(self.submission.form, readonly=True)
        return super(SubmissionEditView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SubmissionEditView, self).get_context_data(**kwargs)
        context['submission'] = self.submission

        # A prefix is defined to prevent a confusion with the naming
        # of the form field with other forms with the same field name
        context['submission_form'] = self.submission_form_class(instance=self.submission, prefix=self.submission.pk)

        # uses list comprehension to generate a list of forms that can be rendered to display
        # submission sibling form fields.
        context['submission_sibling_forms'] = [self.submission_form_class(instance=x, prefix=x.pk) for x in self.submission.siblings]
        context['location_types'] = LocationType.objects.filter(on_display=True)
        context['page_title'] = self.page_title
        return context

    def get_success_url(self):
        return reverse('submissions_list', args=[self.submission.form.pk])


class SubmissionListExportView(View):
    collection = 'observers'

    # TODO: refactor to support custom field labels
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        form = get_object_or_404(Form, pk=kwargs['form'])
        self.submission_filter = generate_submission_filter(form)
        initial_data = request.session.get('submission_filter_%d' % form.pk, None)
        if self.collection == 'master':
            self.filter_set = self.submission_filter(initial_data,
                queryset=Submission.objects.filter(form=form, observer=None))
        else:
            self.filter_set = self.submission_filter(initial_data,
                queryset=Submission.objects.filter(form=form).exclude(observer=None))
        qs = self.filter_set.qs.order_by('-date', 'observer__observer_id')

        data_fields = FormField.objects.filter(group__form=form).order_by('id').values_list('tag', flat=True)
        datalist_fields = ['observer__observer_id', 'observer__name', 'location'] + list(data_fields) + ['updated']
        export_fields = ['observer__observer_id', 'observer__name', 'loc:location__province', 'loc:location__district'] + list(data_fields) + ['updated']
        field_labels = ['PSZ', 'Name', 'Province', 'District'] + list(data_fields) + ['Timestamp']
        datalist = qs.data(data_fields).values(*datalist_fields)

        filename = slugify('%s %s %s' % (form.name, datetime.now().strftime('%Y %m %d %H%M%S'), self.collection))
        response = HttpResponse(export(datalist, fields=export_fields, labels=field_labels), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s.xls' % (filename,)

        return response


class ContactListView(ListView):
    context_object_name = 'contacts'
    template_name = 'core/contact_list.html'
    model = Observer
    paginate_by = settings.PAGE_SIZE
    page_title = 'Contacts List'

    def get_queryset(self):
        return self.filter_set.qs.order_by('observer_id')

    def get_context_data(self, **kwargs):
        context = super(ContactListView, self).get_context_data(**kwargs)
        context['filter_form'] = self.filter_set.form
        context['page_title'] = self.page_title
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.contacts_filter = generate_contacts_filter()
        return super(ContactListView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.filter_set = self.contacts_filter(request.POST,
            queryset=Observer.objects.all())
        request.session['contacts_filter'] = self.filter_set.form.data
        return super(ContactListView, self).get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        initial_data = request.session.get('contacts_filter', None)
        self.filter_set = self.contacts_filter(initial_data,
            queryset=Observer.objects.all())
        return super(ContactListView, self).get(request, *args, **kwargs)


class ContactEditView(UpdateView):
    template_name = 'core/contact_edit.html'
    model = Observer
    form_class = ContactModelForm
    success_url = '/contacts/'
    page_title = 'Contact Edit'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ContactEditView, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(Observer, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(ContactEditView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context


def make_item_row(record, fields, locations_graph):
    row = []
    pattern = re.compile(r'^loc:(?P<field>\w+?)__(?P<location_type>\w+)$')  # pattern for location specification

    for field in fields:
        match = pattern.match(field)

        if match:
            # if there's a match, retrieve the location name from the graph
            location_id = record[match.group('field')]
            row.append(get_location_ancestor_by_type(locations_graph, location_id, match.group('location_type'))[0]['name'])
        else:
            row.append(record[field])

    return row


def export(datalist, fields, labels=[], **kwargs):
    '''Handles exporting a datalist to a (c)StringIO instance, with its
    contents being a spreadsheet in a specified format.

    `datalist` is the queryset to be exported with values already retrieved,
    the fields to be exported are specified as an array in the `fields` argument
    and there's an optional `labels` parameter for specifying column labels.

    location fields are specified as such:
        'loc:location__province'
    which enable the exporter to retrieve the location name in the progeny of
    the location of the specified location type.

    Also, a `format` keyword argument may be specified (defaulting to 'xls')
    that specifies the format to which the spreadsheet should be exported.
    Allowed values for the `format` argument are: 'ods', 'xls', 'xlsx', 'csv'
    '''
    locations_graph = get_locations_graph()
    dataset = tablib.Dataset()

    # grab keyword argument
    format = kwargs.pop('format', 'xls')
    format = 'xls' if format not in export_formats else format

    # set headers
    dataset.headers = labels or fields

    # retrieve data and build table
    for record in datalist:
        dataset.append(make_item_row(record, fields[:len(labels) if labels else len(fields)], locations_graph))

    return StringIO(getattr(dataset, format))
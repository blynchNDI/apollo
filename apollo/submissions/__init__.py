from ..core import Service
from .models import Submission, SubmissionComment, SubmissionVersion
from ..locations.models import LocationType, Sample
from datetime import datetime
from flask import g
import unicodecsv
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO


def export_field(form, submission, field_name):
    field = form.get_field_by_tag(field_name)

    if not field.allows_multiple_values:
        return getattr(submission, field_name, '')

    data = getattr(submission, field_name, '')
    if isinstance(data, list) and data:
        # only export if there's a non empty list
        return ','.join(sorted([str(i) for i in data]))

    return ''


class SubmissionsService(Service):
    __model__ = Submission

    def _set_default_filter_parameters(self, kwargs):
        """Updates the kwargs by setting the default filter parameters
        if available.

        :param kwargs: a dictionary of parameters
        """
        try:
            deployment = kwargs.get('deployment', g.get('deployment'))
            event = kwargs.get('event', g.get('event'))
            if deployment:
                kwargs.update({'deployment': deployment})
            if event:
                kwargs.update({'event': event})
        except RuntimeError:
            pass

        return kwargs

    def export_list(self, queryset, deployment):
        if queryset.count() < 1:
            yield
        else:
            submission = queryset.first()
            sample_kwargs = {}
            if hasattr(g, 'event'):
                sample_kwargs['event'] = g.event
            if hasattr(g, 'deployment'):
                sample_kwargs['deployment'] = g.deployment
            samples = Sample.objects(**sample_kwargs)
            form = submission.form
            fields = [
                field.name for group in form.groups for field in group.fields]
            location_types = LocationType.objects(
                is_administrative=True, deployment=deployment)

            sample_headers = list(samples.scalar('name'))

            if submission.submission_type == 'O':
                ds_headers = [
                    'Participant ID', 'Name', 'DB Phone', 'Recent Phone'] + \
                    map(lambda location_type: location_type.name,
                        location_types)
                if form.form_type == 'INCIDENT':
                    ds_headers += [
                        'Location', 'Location Code', 'PS Code', 'RV'
                    ] + fields + \
                        ['Timestamp', 'Witness', 'Status', 'Description']
                else:
                    ds_headers += [
                        'Location', 'Location Code', 'PS Code', 'RV'
                    ] + fields + ['Timestamp']
                    ds_headers.extend(sample_headers)
                    ds_headers.append('Comment')
            else:
                ds_headers = [
                    'Participant ID', 'Name', 'DB Phone', 'Recent Phone'] + \
                    map(lambda location_type: location_type.name,
                        location_types)
                ds_headers += [
                    'Location', 'Location Code', 'PS Code', 'RV'] + \
                    fields + ['Timestamp']

                ds_headers.extend(sample_headers)
                ds_headers.extend(map(lambda f: '%s-CONFIDENCE' % f, fields))

            output = StringIO()
            writer = unicodecsv.writer(output, encoding='utf-8')
            writer.writerow([unicode(i) for i in ds_headers])
            yield output.getvalue()
            output.close()

            for submission in queryset:
                if submission.submission_type == 'O':
                    record = [
                        getattr(submission.contributor, 'participant_id', '')
                        if getattr(
                            submission.contributor, 'participant_id', '')
                        else '',
                        getattr(submission.contributor, 'name', '')
                        if getattr(submission.contributor, 'name', '') else '',
                        getattr(submission.contributor, 'phone', '')
                        if getattr(
                            submission.contributor, 'phone', '') else '',
                        submission.contributor.phones[-1].number
                        if getattr(submission.contributor, 'phones', None)
                        else ''] + \
                        [submission.location_name_path.get(
                         location_type.name, '')
                         for location_type in location_types] + \
                        [getattr(submission.location, 'name', '')
                         if submission.location else '',
                         getattr(submission.location, 'code', '')
                         if submission.location else '',
                         getattr(submission.location, 'political_code', '')
                         if submission.location else '',
                         getattr(submission.location, 'registered_voters', '')
                         if submission.location else ''] + \
                        [export_field(form, submission, f) for f in fields]
                    record += \
                        [submission.updated.strftime('%Y-%m-%d %H:%M:%S'),
                         getattr(submission, 'witness', '')
                         if getattr(submission, 'witness', '') else '',
                         getattr(submission, 'status', '')
                         if getattr(submission, 'status', '') else '',
                         getattr(submission, 'description', '')
                         if getattr(submission, 'description', '') else ''] \
                        if form.form_type == 'INCIDENT' else \
                        ([submission.updated.strftime('%Y-%m-%d %H:%M:%S')] +
                            [1 if sample in submission.location.samples else 0
                                for sample in samples] +
                            [submission.comments.first().comment
                             if submission.comments.first() else ''])
                else:
                    sib = submission.siblings.first()
                    record = [
                        getattr(sib.contributor, 'participant_id', '') or ''
                        if sib and hasattr(sib, 'contributor') else '',
                        getattr(sib.contributor, 'name', '') or ''
                        if sib and hasattr(sib, 'contributor') else '',
                        getattr(sib.contributor, 'phone', '') or ''
                        if sib and hasattr(sib, 'contributor') else '',
                        sib.contributor.phones[-1].number
                        if hasattr(sib, 'contributor') and getattr(
                            sib.contributor, 'phones', None)
                        else '' if sib else ''] + \
                        [submission.location_name_path.get(
                            location_type.name, '')
                         for location_type in location_types] + \
                        [getattr(submission.location, 'name', '')
                         if submission.location else '',
                         getattr(submission.location, 'code', '')
                         if submission.location else '',
                         getattr(submission.location, 'political_code', '')
                         if submission.location else '',
                         getattr(submission.location, 'registered_voters', '')
                         if submission.location else ''] + \
                        [export_field(form, submission, f) for f in fields] + \
                        [submission.updated.strftime('%Y-%m-%d %H:%M:%S')] + \
                        [1 if hasattr(submission.location, 'samples') and
                         sample in submission.location.samples else 0
                         for sample in samples] + \
                        [submission.confidence.get(field, '') or ''
                         for field in fields]

                output = StringIO()
                writer = unicodecsv.writer(output, encoding='utf-8')
                writer.writerow([unicode(i) for i in record])
                yield output.getvalue()
                output.close()


class SubmissionCommentsService(Service):
    __model__ = SubmissionComment

    def create_comment(self, submission, comment, user=None):
        return self.create(
            submission=submission, user=user, comment=comment,
            submit_date=datetime.utcnow())


class SubmissionVersionsService(Service):
    __model__ = SubmissionVersion

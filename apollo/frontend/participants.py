# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from flask import (
    Blueprint, g, redirect, render_template, request, url_for
)
from flask.ext.babel import lazy_gettext as _
from flask.ext.menu import register_menu
from ..models import Location, Participant, ParticipantPartner, ParticipantRole
from ..services import participants
from . import route
from .filters import ParticipantFilterSet
from .forms import generate_participant_edit_form

PAGE_SIZE = 25
bp = Blueprint('participants', __name__, template_folder='templates',
               static_folder='static', static_url_path='/core/static')


@route(bp, '/participants')
@register_menu(bp, 'participants', _('Participants'))
def participant_list_default():
    return participant_list(1)


@route(bp, '/participants/<int:page>')
def participant_list(page=1):
    page_title = _('Participants')
    queryset = participants.find()
    queryset_filter = ParticipantFilterSet(queryset)
    template_name = 'frontend/participant_list.html'

    # load form context
    context = {}

    pager = queryset_filter.qs.paginate(page=page, per_page=PAGE_SIZE)

    context.update(
        filter_form=queryset_filter.form,
        page_title=page_title,
        participants=pager
    )

    return render_template(
        template_name,
        **context
    )


@route(bp, '/participant/<pk>', methods=['GET', 'POST'])
def participant_edit(pk):
    deployment = g.get('deployment')
    participant = Participant.objects.get_or_404(pk=pk, deployment=deployment)
    page_title = _(
        'Edit participant: %(participant_id)s',
        participant_id=participant.participant_id
    )
    template_name = 'core/participant_edit.html'

    if request.method == 'GET':
        form = generate_participant_edit_form(participant)
    else:
        form = generate_participant_edit_form(participant, request.form)

        if form.validate():
            participant.participant_id = form.participant_id.data
            participant.name = form.name.data
            participant.gender = form.gender.data
            participant.role = ParticipantRole.objects.with_id(form.role.data)
            participant.supervisor = Participant.objects.with_id(
                form.supervisor.data)
            participant.location = Location.objects.with_id(form.location.data)
            participant.partner = ParticipantPartner.objects.with_id(
                form.partner.data)
            participant.save()

            return redirect(url_for('core.participant_list'))

    return render_template(template_name, form=form, page_title=page_title)

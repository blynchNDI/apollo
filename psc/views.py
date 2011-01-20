# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from models import *
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from rapidsms.contrib.messagelog.tables import MessageTable
from rapidsms.contrib.messagelog.models import Message
from forms import VRChecklistForm, VRIncidentForm, DCOIncidentForm, VRChecklistFilterForm, VRIncidentFilterForm, DCOIncidentFilterForm, DCOChecklistFilterForm, DCOChecklistForm
from forms import DCOIncidentUpdateForm, VRIncidentUpdateForm, MessagelogFilterForm
from datetime import datetime
from django.contrib.auth.decorators import login_required, permission_required
import stats

# paginator settings
items_per_page = 25

@login_required()
def home(request):
    context = {'page_title': 'PSC 2011 SwiftCount Dashboard'}
    
    #vr first missing sms
    context['missing_first_sms'] = stats.model_sieve(VRChecklist, ['submitted'], exclude=True).filter(date=datetime.date(datetime.today())).count()
    context['received_first_sms'] = stats.model_sieve(VRChecklist, ['submitted']).filter(date=datetime.date(datetime.today())).count()

    # second missing sms
    context['missing_second_sms'] = stats.model_sieve(VRChecklist, ['A', 'B', 'C', 'F', 'G', ['D1', 'D2', 'D3', 'D4'], ['E1', 'E2', 'E3', 'E4', 'E5']], exclude=True).filter(date=datetime.date(datetime.today())).count()
    context['complete_second_sms'] = stats.model_sieve(VRChecklist, ['A', 'B', 'C', 'F', 'G', ['D1', 'D2', 'D3', 'D4'], ['E1', 'E2', 'E3', 'E4', 'E5']]).exclude(A=4).filter(date=datetime.date(datetime.today())).count()
    context['incomplete_second_sms'] = stats.model_sieve(VRChecklist, [['A', 'B', 'C', 'F', 'G', 'D1', 'D2', 'D3', 'D4', 'E1', 'E2', 'E3', 'E4', 'E5']]).exclude(A=4).filter(date=datetime.date(datetime.today())).count() - context['complete_second_sms']
    context['unverified_second_sms'] = stats.model_sieve(VRChecklist, [('A', 4), ('verified_second', False), 'B', 'C', 'F', 'G', ['D1', 'D2', 'D3', 'D4'], ['E1', 'E2', 'E3', 'E4', 'E5']]).filter(date=datetime.date(datetime.today())).count()
    context['not_open_second_sms'] = stats.model_sieve(VRChecklist, ['B', 'C', 'F', 'D1', 'D2', 'D3', 'D4', 'E1', 'E2', 'E3', 'E4', 'E5'], exclude=True).filter(A=4).filter(date=datetime.date(datetime.today())).count() + stats.model_sieve(VRChecklist, [('A', 4), ('verified_second', True)]).filter(date=datetime.date(datetime.today())).count()

    # third missing sms
    context['complete_third_sms'] = stats.model_sieve(VRChecklist, ['H', 'J', 'K', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA']).exclude(A=4).filter(date=datetime.date(datetime.today())).count()
    context['complete_third_sms'] += stats.model_sieve(VRChecklist, ['H', 'J', 'K', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', ('A', 4), ('verified_third', True)]).filter(date=datetime.date(datetime.today())).count()
    context['missing_third_sms'] = context['complete_second_sms'] - context['complete_third_sms'] 
    context['blank_third_sms'] = stats.model_sieve(VRChecklist, ['H', 'J', 'K', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA'], exclude=True).filter(A=4).filter(date=datetime.date(datetime.today())).count()
    third_partial_qs_include = Q(H__isnull=False) | Q(J__isnull=False) | Q(K__isnull=False) | Q(M__isnull=False) | \
          Q(N__isnull=False) | Q(P__isnull=False) | Q(Q__isnull=False) | Q(R__isnull=False) | \
          Q(S__isnull=False) | Q(T__gt=0) & Q(U__gt=0) | Q(V__gt=0) | Q(W__gt=0) | Q(X__gt=0) | Q(Y__isnull=False) | \
          Q(Z__isnull=False) | Q(AA__isnull=False) 
    third_partial_qs_exclude = ~Q(A=4) & Q(H__isnull=False) & Q(J__isnull=False) & Q(K__isnull=False) & Q(M__isnull=False) & \
          Q(N__isnull=False) & Q(P__isnull=False) & Q(Q__isnull=False) & Q(R__isnull=False) & \
          Q(S__isnull=False) & Q(T__gt=0) & Q(U__gt=0) & Q(V__gt=0) & Q(W__gt=0) & Q(X__gt=0) & Q(Y__isnull=False) & \
          Q(Z__isnull=False) & Q(AA__isnull=False) | Q(A=4)
    context['partial_third_sms'] = VRChecklist.objects.filter(date=datetime.date(datetime.today())).filter(third_partial_qs_include).exclude(third_partial_qs_exclude).count()
    third_unverified_qs = Q(A=4) & Q(verified_third=False) & (Q(H__isnull=False) | Q(J__isnull=False) | Q(K__isnull=False) | Q(M__isnull=False) | \
          Q(N__isnull=False) | Q(P__isnull=False) | Q(Q__isnull=False) | Q(R__isnull=False) | \
          Q(S__isnull=False) | Q(T__gt=0) & Q(U__gt=0) | Q(V__gt=0) | Q(W__gt=0) | Q(X__gt=0) | Q(Y__isnull=False) | \
          Q(Z__isnull=False) | Q(AA__isnull=False))
    context['unverified_third_sms'] = VRChecklist.objects.filter(date=datetime.date(datetime.today())).filter(third_unverified_qs).count()
    context['not_open_third_sms'] = stats.model_sieve(VRChecklist, [('A', 4), ('verified_third', True)]).filter(date=datetime.date(datetime.today())).count()

    context['vr_incidents_count'] = VRIncident.objects.all().count()
    context['vr_incidents_today'] = VRIncident.objects.filter(date=datetime.date(datetime.today())).count()

    #dco checklist sent today
    context['dco_checklist_today'] = DCOChecklist.objects.filter(date=datetime.date(datetime.today())).count()
    context['dco_incidents_count'] = DCOIncident.objects.all().count()
    context['dco_incidents_today'] = DCOIncident.objects.filter(date=datetime.date(datetime.today())).count()

    context['dco_checklist_first_today'] = DCOChecklist.objects.filter(sms_serial=1,date=datetime.date(datetime.today())).count()
    context['dco_checklist_second_today'] = DCOChecklist.objects.filter(sms_serial=2,date=datetime.date(datetime.today())).count()
    context['dco_checklist_third_today'] = DCOChecklist.objects.filter(sms_serial=3,date=datetime.date(datetime.today())).count()

    #render
    return render_to_response('psc/home.html', context,  context_instance=RequestContext(request))

@login_required()
def vr_checklist_list(request):
    #qs = Q(date__in=[d[0] for d in VR_DAYS if d[0]])
    qs_include = Q()
    qs_exclude = Q()
    if not request.session.has_key('vr_checklist_filter'):
        request.session['vr_checklist_filter'] = {}

    if request.method == 'GET':
        if filter(lambda key: request.GET.has_key(key), ['zone', 'state', 'first', 'second', 'third', 'day', 'observer_id']):
            request.session['vr_checklist_filter'] = request.GET
        filter_form = VRChecklistFilterForm(request.session['vr_checklist_filter'])

        if filter_form.is_valid():
            data = filter_form.cleaned_data

            if data['zone']:
                qs_include &= Q(observer__location_id__in=LGA.objects.filter(parent__parent__parent__code__iexact=data['zone']).values_list('id', flat=True))
            if data['state']:
                qs_include &= Q(observer__location_id__in=LGA.objects.filter(parent__parent__code__exact=data['state']).values_list('id', flat=True))
            if data['day']:
                qs_include &= Q(date=data['day'])

            if data['first'] == u'1':
                qs_include &= Q(submitted=True)
            elif data['first'] == u'2':
                qs_include &= Q(submitted=False)

            if data['second'] == u'1': # complete
                qs_include &= ~Q(A=4) & Q(B__gt=0) & Q(C__isnull=False) & Q(F__isnull=False) & Q(G__gt=0) & \
                      (Q(D1__isnull=False) | Q(D2__isnull=False) | Q(D3__isnull=False) | Q(D4__isnull=False)) & \
                      (Q(E1__isnull=False) | Q(E2__isnull=False) | Q(E3__isnull=False) | Q(E4__isnull=False) | \
                      Q(E5__isnull=False))
            elif data['second'] == u'2': # missing
                qs_include &= Q(A__isnull=True) & Q(B=0) & Q(C__isnull=True) & Q(F__isnull=True) & Q(G=0) & \
                      (Q(D1__isnull=True) | Q(D2__isnull=True) | Q(D3__isnull=True) | Q(D4__isnull=True)) & \
                      (Q(E1__isnull=True) | Q(E2__isnull=True) | Q(E3__isnull=True) | Q(E4__isnull=True) | \
                      Q(E5__isnull=True))
            elif data['second'] == u'3': # partial
                qs_include &= (~Q(B=0) | Q(C__isnull=False) | Q(F__isnull=False) | ~Q(G=0) | \
                      Q(D1__isnull=False) | Q(D2__isnull=False) | Q(D3__isnull=False) | Q(D4__isnull=False) | \
                      Q(E1__isnull=False) | Q(E2__isnull=False) | Q(E3__isnull=False) | Q(E4__isnull=False) | \
                      Q(E5__isnull=False)) & ~Q(A=4) 
                qs_exclude &= ~Q(A=4) & Q(B__gt=0) & Q(C__isnull=False) & Q(F__isnull=False) & Q(G__gt=0) & \
                      (Q(D1__isnull=False) | Q(D2__isnull=False) | Q(D3__isnull=False) | Q(D4__isnull=False)) & \
                      (Q(E1__isnull=False) | Q(E2__isnull=False) | Q(E3__isnull=False) | Q(E4__isnull=False) | \
                      Q(E5__isnull=False))
            elif data['second'] == u'4': # not open unverified
                qs_include &= (~Q(B=0) | Q(C__isnull=False) | Q(F__isnull=False) | ~Q(G=0) | \
                      Q(D1__isnull=False) | Q(D2__isnull=False) | Q(D3__isnull=False) | Q(D4__isnull=False) | \
                      Q(E1__isnull=False) | Q(E2__isnull=False) | Q(E3__isnull=False) | Q(E4__isnull=False) | \
                      Q(E5__isnull=False)) & Q(A=4) & Q(verified_second=False)
            elif data['second'] == u'5': # not open verified
                qs_include &= (Q(A=4) & Q(verified_second=True)) | ((Q(B=0) & Q(C__isnull=True) & Q(F__isnull=True) & Q(G=0) & \
                      (Q(D1__isnull=True) | Q(D2__isnull=True) | Q(D3__isnull=True) | Q(D4__isnull=True)) & \
                      (Q(E1__isnull=True) | Q(E2__isnull=True) | Q(E3__isnull=True) | Q(E4__isnull=True) | \
                      Q(E5__isnull=True))) & Q(A=4))

            if data['third'] == u'1': # complete
                qs_include &= ~Q(A=4) & Q(H__isnull=False) & Q(J__isnull=False) & Q(K__isnull=False) & Q(M__isnull=False) & \
                      Q(N__isnull=False) & Q(P__isnull=False) & Q(Q__isnull=False) & Q(R__isnull=False) & \
                      Q(S__isnull=False) & Q(T__gt=0) & Q(U__gt=0) & Q(V__gt=0) & Q(W__gt=0) & Q(X__gt=0) & Q(Y__isnull=False) & \
                      Q(Z__isnull=False) & Q(AA__isnull=False)
            elif data['third'] == u'2': # incomplete
                qs_include &= ~Q(A=4) & Q(H__isnull=True) & Q(J__isnull=True) & Q(K__isnull=True) & Q(M__isnull=True) & \
                      Q(N__isnull=True) & Q(P__isnull=True) & Q(Q__isnull=True) & Q(R__isnull=True) & \
                      Q(S__isnull=True) & Q(T=0) & Q(U=0) & Q(V=0) & Q(W=0) & Q(X=0) & Q(Y__isnull=True) & \
                      Q(Z__isnull=True) & Q(AA__isnull=True)
            elif data['third'] == u'3': # partial
                qs_include &= Q(H__isnull=False) | Q(J__isnull=False) | Q(K__isnull=False) | Q(M__isnull=False) | \
                      Q(N__isnull=False) | Q(P__isnull=False) | Q(Q__isnull=False) | Q(R__isnull=False) | \
                      Q(S__isnull=False) | Q(T__gt=0) & Q(U__gt=0) | Q(V__gt=0) | Q(W__gt=0) | Q(X__gt=0) | Q(Y__isnull=False) | \
                      Q(Z__isnull=False) | Q(AA__isnull=False) 
                qs_exclude &= ~Q(A=4) & Q(H__isnull=False) & Q(J__isnull=False) & Q(K__isnull=False) & Q(M__isnull=False) & \
                      Q(N__isnull=False) & Q(P__isnull=False) & Q(Q__isnull=False) & Q(R__isnull=False) & \
                      Q(S__isnull=False) & Q(T__gt=0) & Q(U__gt=0) & Q(V__gt=0) & Q(W__gt=0) & Q(X__gt=0) & Q(Y__isnull=False) & \
                      Q(Z__isnull=False) & Q(AA__isnull=False) | Q(A=4)
            elif data['third'] == u'4': # not open unverified
                qs_include &= Q(A=4) & Q(verified_third=False) & (Q(H__isnull=False) | Q(J__isnull=False) | Q(K__isnull=False) | Q(M__isnull=False) | \
                      Q(N__isnull=False) | Q(P__isnull=False) | Q(Q__isnull=False) | Q(R__isnull=False) | \
                      Q(S__isnull=False) | Q(T__gt=0) & Q(U__gt=0) | Q(V__gt=0) | Q(W__gt=0) | Q(X__gt=0) | Q(Y__isnull=False) | \
                      Q(Z__isnull=False) | Q(AA__isnull=False))
            elif data['third'] == u'5': # not open verified
                qs_include &= Q(A=4) & Q(verified_third=True)
            elif data['third'] == u'6': # blank
                qs_include &= Q(A=4) & Q(H__isnull=True) & Q(J__isnull=True) & Q(K__isnull=True) & Q(M__isnull=True) & \
                      Q(N__isnull=True) & Q(P__isnull=True) & Q(Q__isnull=True) & Q(R__isnull=True) & \
                      Q(S__isnull=True) & Q(T=0) & Q(U=0) & Q(V=0) & Q(W=0) & Q(X=0) & Q(Y__isnull=True) & \
                      Q(Z__isnull=True) & Q(AA__isnull=True)
            
            if data['observer_id']:
                qs_include = Q(observer__observer_id__exact=data['observer_id'])
    else:
        filter_form = VRChecklistFilterForm()

    #get all objects
    global items_per_page
    if request.GET.get('export'):
	    items_per_page = VRChecklist.objects.filter(qs_include).exclude(qs_exclude).count()
    
    paginator = Paginator(VRChecklist.objects.filter(qs_include).exclude(qs_exclude), items_per_page)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # an invalid range will retrieve the last page of results
    try:
        checklists = paginator.page(page)
    except (EmptyPage, InvalidPage):
        checklists = paginator.page(paginator.num_pages)

    page_details = {}
    page_details['first'] = paginator.page_range[0]
    page_details['last'] = paginator.page_range[len(paginator.page_range) - 1]
    return render_to_response('psc/vr_checklist_list.html', {'page_title': "Voter Registration Data Management", 'checklists': checklists, 'filter_form': filter_form, 'page_details' : page_details }, context_instance=RequestContext(request))

@login_required()
def dco_checklist_list(request):
    #qs = Q(date__in=[d[0] for d in DCO_DAYS if d[0]])
    qs = Q()
    if request.method == 'GET':
        filter_form = DCOChecklistFilterForm(request.GET)

        if filter_form.is_valid():
            data = filter_form.cleaned_data
            if data['zone']:
                qs &= Q(observer__location_id__in=LGA.objects.filter(parent__parent__parent__code__iexact=data['zone']).values_list('id', flat=True))
            if data['state']:
                qs &= Q(observer__location_id__in=LGA.objects.filter(parent__parent__code__exact=data['state']).values_list('id', flat=True))
            if data['district']:
                qs &= Q(observer__location_id__in=LGA.objects.filter(parent__code__exact=data['district']).values_list('id', flat=True))
            if data['day']:
                qs &= Q(date=data['day'])
            if data['observer_id']:
                qs = Q(observer__observer_id__exact=data['observer_id'])
    else:
        filter_form = DCOChecklistFilterForm()

    paginator = Paginator(DCOChecklist.objects.filter(qs).order_by('date', 'observer', 'sms_serial'), items_per_page)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # an invalid range will retrieve the last page of results
    try:
        checklists = paginator.page(page)
    except (EmptyPage, InvalidPage):
        checklists = paginator.page(paginator.num_pages)

    page_details = {}
    page_details['first'] = paginator.page_range[0]
    page_details['last'] = paginator.page_range[len(paginator.page_range) - 1]
    return render_to_response('psc/dco_checklist_list.html', {'page_title': "Display, Claims & Objections Data Management", 'checklists': checklists, 'filter_form': filter_form, 'page_details': page_details }, context_instance=RequestContext(request))

@login_required()
def vr_checklist(request, checklist_id=0):
    checklist = get_object_or_404(VRChecklist, pk=checklist_id)
    rcs = RegistrationCenter.objects.filter(parent=checklist.location.parent)
    location = checklist.observer.location
    if (request.POST):
        f = VRChecklistForm(request.POST, instance=checklist)
        if f.is_valid():
            f.save()
        return HttpResponseRedirect(reverse('psc.views.vr_checklist_list'))
    else:
        f = VRChecklistForm(instance=checklist)
        return render_to_response('psc/vr_checklist_form.html', {'page_title': "Voter Registration Checklist", 'checklist': checklist, 'rcs': rcs, 'location': location, 'form': f }, context_instance=RequestContext(request))

@login_required()
def dco_checklist(request, checklist_id=0):   
    checklist = get_object_or_404(DCOChecklist, pk=checklist_id)
    rcs = RegistrationCenter.objects.filter(parent=checklist.location.parent)
    location = checklist.observer.location
    if (request.POST):
        f = DCOChecklistForm(request.POST, instance=checklist)
        if f.is_valid():
            f.save()
        return HttpResponseRedirect(reverse('psc.views.dco_checklist_list'))
    else:
        f = DCOChecklistForm(instance=checklist)
    return render_to_response('psc/dco_checklist_form.html', {'page_title': 'Display, Claims & Objections Checklist', 'checklist': checklist, 'rcs': rcs, 'location': location, 'form': f}, context_instance=RequestContext(request))

@login_required()
def vr_incident_update(request, incident_id=0):
    incident = get_object_or_404(VRIncident, pk=incident_id)
    #rc location for incident observer
    location = incident.observer.location
    lga_list = LGA.objects.all()
    rc_list_by_lga = RegistrationCenter.objects.filter(parent=incident.location.parent.id)
    
    if request.POST:        
        f = VRIncidentUpdateForm(request.POST, instance=incident)
        if f.is_valid():
            f.save()
        return HttpResponseRedirect(reverse('psc.views.vr_incident_list'))    
    else:
        f = VRIncidentForm(instance=incident)   
        return render_to_response('psc/vr_incident_update_form.html', {'page_title': "Voter Registration Critrical Incident", 'incident': incident, 'location': location, 'form': f, 'lga_list': lga_list, 'rc_list_by_lga': rc_list_by_lga }, context_instance=RequestContext(request))

@login_required()
def dco_incident_update(request, incident_id=0):
    incident = get_object_or_404(DCOIncident, pk=incident_id)
    location = incident.observer.location
    if request.POST:
        f = DCOIncidentUpdateForm(request.POST, instance=incident)    
        if f.is_valid():
            f.save()
        return HttpResponseRedirect(reverse('psc.views.dco_incident_list'))
    else:
        f = DCOIncidentForm(instance=incident)
        return render_to_response('psc/dco_incident_update_form.html', {'page_title': 'Display, Claims & Objections Critical Incident', 'incident': incident, 'location': location, 'form': f }, context_instance=RequestContext(request))

@login_required()
def vr_incident_add(request):
    if request.POST:
        f = VRIncidentForm(request.POST, VRIncident)
        f.save()
        return HttpResponseRedirect(reverse('psc.views.vr_incident_list'))
    else:
        f = VRIncidentForm()
        return render_to_response('psc/vr_incident_add_form.html', {'page_title': "Add Voter Registration Critrical Incident", 'form': f }, context_instance=RequestContext(request))

@login_required()
def dco_incident_add(request):
    if request.POST:
        f = DCOIncidentForm(request.POST)                    
        f.save()
        return HttpResponseRedirect(reverse('psc.views.dco_incident_list'))
    else:
        f = DCOIncidentForm()
        return render_to_response('psc/dco_incident_add_form.html', {'page_title': "Add Display, Claims & Objections Critrical Incident", 'form': f }, context_instance=RequestContext(request))

@login_required()
def vr_incident_list(request):
    qs = Q()
    if not request.session.has_key('vr_incident_filter'):
        request.session['vr_incident_filter'] = {}

    if request.method == 'GET':
        if filter(lambda key: request.GET.has_key(key), ['zone', 'state', 'district', 'day', 'observer_id']):
            request.session['vr_incident_filter'] = request.GET
        filter_form = VRIncidentFilterForm(request.session['vr_incident_filter'])

        if filter_form.is_valid():
            data = filter_form.cleaned_data
            if data['zone']:
                qs &= Q(location_id__in=RegistrationCenter.objects.filter(parent__parent__parent__parent__code__exact=data['zone']).values_list('id', flat=True))
            if data['state']:
                qs &= Q(location_id__in=RegistrationCenter.objects.filter(parent__parent__parent__code__exact=data['state']).values_list('id', flat=True))
            if data['district']:
                qs &= Q(location_id__in=RegistrationCenter.objects.filter(parent__parent__code__exact=data['district']).values_list('id', flat=True))
            if data['day']:
                qs &= Q(date=data['day'])
            if data['observer_id']:
                qs = Q(observer__observer_id__exact=data['observer_id'])
    else:
        filter_form = VRIncidentFilterForm()

    if request.GET.get('export'):
        global items_per_page
	items_per_page = VRIncident.objects.filter(qs).count()

    paginator = Paginator(VRIncident.objects.filter(qs).order_by('-id'), items_per_page)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # an invalid range will retrieve the last page of results
    try:
        checklists = paginator.page(page)
    except (EmptyPage, InvalidPage):
        checklists = paginator.page(paginator.num_pages)
    
    page_details = {}
    page_details['first'] = paginator.page_range[0]
    page_details['last'] = paginator.page_range[len(paginator.page_range) - 1]
    return render_to_response('psc/vr_incident_list.html', {'page_title': "Voter Registration Critical Incidents", 'checklists': checklists, 'filter_form': filter_form, 'page_details': page_details}, context_instance=RequestContext(request))

@login_required()
def dco_incident_list(request):
    qs = Q()
    if request.method == 'GET':
        filter_form = DCOIncidentFilterForm(request.GET)

        if filter_form.is_valid():
            data = filter_form.cleaned_data
            if data['zone']:
                qs &= Q(observer__location_id__in=LGA.objects.filter(parent__parent__parent__code__iexact=data['zone']).values_list('id', flat=True))
            if data['state']:
                qs &= Q(observer__location_id__in=LGA.objects.filter(parent__parent__code__exact=data['state']).values_list('id', flat=True))
            if data['district']:
                qs &= Q(observer__location_id__in=LGA.objects.filter(parent__code__exact=data['district']).values_list('id', flat=True))
            if data['day']:
                qs &= Q(date=data['day'])
            if data['observer_id']:
                qs = Q(observer__observer_id__exact=data['observer_id'])
    else:
        filter_form = DCOIncidentFilterForm()

    paginator = Paginator(DCOIncident.objects.filter(qs).order_by('-id'), items_per_page)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # an invalid range will retrieve the last page of results
    try:
        checklists = paginator.page(page)
    except (EmptyPage, InvalidPage):
        checklists = paginator.page(paginator.num_pages)

    page_details = {}
    page_details['first'] = paginator.page_range[0]
    page_details['last'] = paginator.page_range[len(paginator.page_range) - 1]
    return render_to_response('psc/dco_incident_list.html', {'page_title': "Display, Claims & Objections Critical Incidents", 'checklists': checklists, 'filter_form': filter_form, 'page_details': page_details}, context_instance=RequestContext(request))

@login_required()
@permission_required('psc.can_administer', login_url='/')
def message_log(request):
    qs = Q()
    if not request.session.has_key('messagelog_filter'):
        request.session['messagelog_filter'] = {}

    if request.method == 'GET':
        if filter(lambda key: request.GET.has_key(key), ['phone', 'message']):
            request.session['messagelog_filter'] = request.GET
        filter_form = MessagelogFilterForm(request.session['messagelog_filter'])

        if filter_form.is_valid():
            data = filter_form.cleaned_data

            if data['phone']:
                qs &= Q(connection__identity__icontains=data['phone'].strip())
            if data['message']:
                qs &= Q(text__icontains=data['message'])
    else:
        filter_form = MessagelogFilterForm()
    
    messages = MessageTable(Message.objects.filter(qs), request=request)
    return render_to_response('psc/msg_log.html', { 'page_title': 'Message Log', 'messages_list' : messages, 'filter_form': filter_form }, context_instance=RequestContext(request))

@login_required()
@permission_required('psc.can_administer', login_url='/')
def action_log(request):
    from itertools import chain
    #get action log for vr and dco 
    vr_checklist_log = VRChecklist.audit_log.all()
    vr_incident_log = VRIncident.audit_log.all()
    dco_checklist_log = DCOChecklist.audit_log.all()
    dco_incident_log = DCOIncident.audit_log.all()

    object_list = list(chain(dco_checklist_log, dco_incident_log, vr_incident_log, vr_checklist_log))
    
    paginator = Paginator(object_list, items_per_page)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # an invalid range will retrieve the last page of results
    try:
        logs = paginator.page(page)
    except (EmptyPage, InvalidPage):
        logs = paginator.page(paginator.num_pages)
    return render_to_response('psc/action_log.html', {'page_title': 'Action Log', 'logs' : logs},  context_instance=RequestContext(request))

def ajax_fetch_rcs(request, method, lga_id=0):
    if lga_id:
        rcs = RegistrationCenter.objects.filter(parent__id=lga_id)

@login_required()
@permission_required('psc.can_analyse', login_url='/')
def export(request, model):
    import csv
    
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % model
    writer = csv.writer(response)

    def export_messagelog(writer):
        header =  ["Date","Phone","Direction","Text"]
        writer.writerow(header)
        
        messages = Message.objects.all().order_by('-date')        
        for message in messages:
            date = message.date.strftime('%Y-%m-%d %H:%M:%S')
            phone = message.connection.identity
            direction = message.direction
            text = message.text
            writer.writerow([date, phone, direction, text.replace('"', "'")])

    def export_vri(writer):
        header = ["PSC ID","Zone","State","LGA","VR","RC","A","B","C","D","E","F","G","H","J","K","M","N","P","Q","Comment"]
        writer.writerow(header)

        vris = VRIncident.objects.all()
        for vri in vris:
            pscid = vri.observer.observer_id
            lga = vri.location.parent.name
            if vri.location.parent.code == '999':
                if vri.observer.role == 'SDC':
                    zone = vri.observer.location.parent.parent.name
                    state = vri.observer.location.parent.name
                else:
                    zone = vri.observer.location.parent.name
                    state = vri.observer.location.name
            else:
                zone = vri.location.parent.parent.parent.parent.name
                state = vri.location.parent.parent.parent.name
            vr = vri.date.day
            rc = vri.location.code
            A = vri.A if vri.A else ""
            B = vri.B if vri.B else ""
            C = vri.C if vri.C else ""
            D = vri.D if vri.D else ""
            E = vri.E if vri.E else ""
            F = vri.F if vri.F else ""
            G = vri.G if vri.G else ""
            H = vri.H if vri.H else ""
            J = vri.J if vri.J else ""
            K = vri.K if vri.K else ""
            M = vri.M if vri.M else ""
            N = vri.N if vri.N else ""
            P = vri.P if vri.P else ""
            Q = vri.Q if vri.Q else ""
            comment = vri.comment if vri.comment else ""
            writer.writerow([pscid, zone, state, lga, vr, rc, A, B, C, D, E, F, G, H, J, K, M, N, P, Q, comment.replace('"', "'")])

    def export_vrc(writer):
        header =  ["PSC ID","Zone","State","LGA","VR","RC","A","B","C","D1","D2","D3","D4","E1","E2","E3","E4","E5","F","G","H","J","K","M","N","P","Q","R","S","T","U","V","W","X","Y","Z","AA","Comment"]
        writer.writerow(header)

        vrcs = VRChecklist.objects.filter(submitted=True,observer__role='LGA')
        for vrc in vrcs:
            pscid = vrc.observer.observer_id
            try:
                zone = vrc.location.parent.parent.parent.parent.name
                state = vrc.location.parent.parent.parent.name
                lga = vrc.location.parent.name
                rc = vrc.location.code
            except AttributeError:
                try:
                    zone = vrc.observer.location.parent.parent.parent.name
                    state = vrc.observer.location.parent.parent.name
                    lga = vrc.observer.location.name
                    rc = "999"
                except AttributeError:
                    pass
            vr = vrc.date.day
            A = vrc.A if vrc.A else ""
            B = vrc.B
            C = vrc.C if vrc.C != None else ""
            D1 = "" if vrc.D1 == None else 1 if vrc.D1 == True else 2
            D2 = "" if vrc.D2 == None else 1 if vrc.D2 == True else 2
            D3 = "" if vrc.D3 == None else 1 if vrc.D3 == True else 2
            D4 = "" if vrc.D4 == None else 1 if vrc.D4 == True else 2
            E1 = "" if vrc.E1 == None else 1 if vrc.E1 == True else 2
            E2 = "" if vrc.E2 == None else 1 if vrc.E2 == True else 2
            E3 = "" if vrc.E3 == None else 1 if vrc.E3 == True else 2
            E4 = "" if vrc.E4 == None else 1 if vrc.E4 == True else 2
            E5 = "" if vrc.E5 == None else 1 if vrc.E5 == True else 2
            F = vrc.F if vrc.F != None else ""
            G = vrc.G
            H = vrc.H if vrc.H else ""
            J = vrc.J if vrc.J else ""
            K = vrc.K if vrc.K else ""
            M = vrc.M if vrc.M else ""
            N = vrc.N if vrc.N else ""
            P = vrc.P if vrc.P else ""
            Q = vrc.Q if vrc.Q else ""
            R = vrc.R if vrc.R else ""
            S = vrc.S if vrc.S else ""
            T = vrc.T
            U = vrc.U
            V = vrc.V
            W = vrc.W
            X = vrc.X
            Y = vrc.Y if vrc.Y != None else ""
            Z = vrc.Z if vrc.Z != None else ""
            AA = vrc.AA if vrc.AA != None else ""
            comment = vrc.comment
            writer.writerow([pscid, zone, state, lga, vr, rc, A, B, C, D1, D2, D3, D4, E1, E2, E3, E4, E5, F, G, H, J, K, M, N, P, Q, R, S, T, U, V, W, X, Y, Z, AA, comment.replace('"', "'")])

    # export here
    # TODO: refactor
    export_method = eval("export_%s" % model)
    if hasattr(export_method, '__call__'):
        export_method(writer)
        return response
@permission_required('psc.can_analyse', login_url='/')
@login_required()
def zone_summary(request):
    zone_list = Zone.objects.all()
    return render_to_response('psc/zone_summary.html', {'page_title': 'Zone Summary', 'zone_list': zone_list},  context_instance=RequestContext(request))

@permission_required('psc.can_analyse', login_url='/')
@login_required()
def state_summary(request):
    state_list = State.objects.all()
    return render_to_response('psc/state_summary.html', {'page_title': 'State Summary', 'state_list': state_list},  context_instance=RequestContext(request))

def get_rcs_by_lga(request, lga_id=0):
    #response = HttpResponse(mimetype='application/json')
    #get the serilizer
    from django.core import serializers
    if lga_id:
       rcs = serializers.serialize('json', RegistrationCenter.objects.filter(parent=lga_id))
       return HttpResponse(mimetype='application/json', content=rcs)

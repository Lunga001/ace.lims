# -*- coding: utf-8 -*-
#
# This file is part of Bika LIMS
#
# Copyright 2011-2017 by it's authors.
# Some rights reserved. See LICENSE.txt, AUTHORS.txt.

from bika.lims import api
from bika.lims import bikaMessageFactory as _
from bika.lims.browser.analysisrequest.analysisrequests \
        import AnalysisRequestsView
from bika.lims.utils import t
from Products.Archetypes import PloneMessageFactory as PMF


def __init__(self, context, request):
    super(AnalysisRequestsView, self).__init__(context, request)

    request.set('disable_plone.rightcolumn', 1)
    self.pagesize = 500

    self.catalog = "bika_catalog"
    self.contentFilter = {'portal_type': 'AnalysisRequest',
                          'sort_on': 'created',
                          'sort_order': 'reverse',
                          'path': {"query": "/", "level": 0},
                          'cancellation_state': 'active',
                          }

    self.context_actions = {}

    if self.context.portal_type == "AnalysisRequestsFolder":
        self.request.set('disable_border', 1)

    if self.view_url.find("analysisrequests") == -1:
        self.view_url = self.view_url + "/analysisrequests"

    self.allow_edit = True

    self.show_sort_column = False
    self.show_select_row = False
    self.show_select_column = True
    self.form_id = "analysisrequests"

    self.icon = self.portal_url + "/++resource++bika.lims.images/analysisrequest_big.png"
    self.title = self.context.translate(_("Analysis Requests"))
    self.description = ""

    SamplingWorkflowEnabled = \
            self.context.bika_setup.getSamplingWorkflowEnabled()

    mtool = api.get_tool('portal_membership')
    member = mtool.getAuthenticatedMember()
    user_is_preserver = 'Preserver' in member.getRoles()

    self.columns = {
        'getRequestID': {'title': _('Request ID'),
                         'index': 'getRequestID'},
        'getClientOrderNumber': {'title': _('Client Order'),
                                 'index': 'getClientOrderNumber',
                                 'toggle': True},
        'Creator': {'title': PMF('Creator'),
                                 'index': 'Creator',
                                 'toggle': True},
        'Created': {'title': PMF('Date Created'),
                    'index': 'created',
                    'toggle': False},
        'getSample': {'title': _("Sample"),
                      'toggle': True, },
        'BatchID': {'title': _("Batch ID"), 'toggle': True},
        'SubGroup': {'title': _('Sub-group')},
        'Client': {'title': _('Client'),
                   'toggle': True},
        'getClientReference': {'title': _('Client Ref'),
                               'index': 'getClientReference',
                               'toggle': True},
        'getClientSampleID': {'title': _('Client SID'),
                              'index': 'getClientSampleID',
                              'toggle': True},
        'ClientContact': {'title': _('Contact'),
                             'toggle': False},
        'getSampleTypeTitle': {'title': _('Sample Type'),
                               'index': 'getSampleTypeTitle',
                               'toggle': True},
        'getSamplePointTitle': {'title': _('Sample Point'),
                                'index': 'getSamplePointTitle',
                                'toggle': False},
        'getStorageLocation': {'title': _('Storage Location'),
                                'toggle': False},
        'SamplingDeviation': {'title': _('Sampling Deviation'),
                              'toggle': False},
        'Priority': {'title': _('Priority'),
                        'toggle': True,
                        'index': 'Priority',
                        'sortable': True},
        'AdHoc': {'title': _('Ad-Hoc'),
                  'toggle': False},
        'SamplingDate': {'title': _('Sampling Date'),
                         'index': 'getSamplingDate',
                         'toggle': True},
        'getDateSampled': {'title': _('Date Sampled'),
                           'index': 'getDateSampled',
                           'toggle': SamplingWorkflowEnabled,
                           'input_class': 'datetimepicker_nofuture',
                           'input_width': '10'},
        'getDateVerified': {'title': _('Date Verified'),
                            'input_width': '10'},
        'getSampler': {'title': _('Sampler'),
                       'toggle': SamplingWorkflowEnabled},
        'getDatePreserved': {'title': _('Date Preserved'),
                             'toggle': user_is_preserver,
                             'input_class': 'datetimepicker_nofuture',
                             'input_width': '10',
                             'sortable': False},  # no datesort without index
        'getPreserver': {'title': _('Preserver'),
                         'toggle': user_is_preserver},
        'getDateReceived': {'title': _('Date Received'),
                            'index': 'getDateReceived',
                            'toggle': False},
        'getDatePublished': {'title': _('Date Published'),
                             'index': 'getDatePublished',
                             'toggle': False},
        'state_title': {'title': _('State'),
                        'index': 'review_state'},
        'getProfilesTitle': {'title': _('Profile'),
                            'index': 'getProfilesTitle',
                            'toggle': False},
        'getAnalysesNum': {'title': _('Number of Analyses'),
                           'index': 'getAnalysesNum',
                           'sortable': True,
                           'toggle': False},
        'getTemplateTitle': {'title': _('Template'),
                             'index': 'getTemplateTitle',
                             'toggle': False},
    }
    self.review_states = [
        {'id': 'default',
         'title': _('None'),
         'contentFilter': {'review_state': 'impossible'},
         'custom_actions': [],
         'columns': ['getRequestID',
                    'getSample',
                    'BatchID',
                    'SubGroup',
                    'Client',
                    'Creator',
                    'Created',
                    'getClientOrderNumber',
                    'getClientReference',
                    'ClientContact',
                    'getClientSampleID',
                    'getProfilesTitle',
                    'getTemplateTitle',
                    'getSampleTypeTitle',
                    'getSamplePointTitle',
                    'getStorageLocation',
                    'SamplingDeviation',
                    'Priority',
                    'AdHoc',
                    'SamplingDate',
                    'getDateSampled',
                    'getSampler',
                    'getDatePreserved',
                    'getPreserver',
                    'getDateReceived',
                    'getAnalysesNum',
                    'getDateVerified',
                    'state_title']},
        {'id': 'active',
         'title': _('Active'),
         'contentFilter': {'sort_on': 'created',
                           'sort_order': 'reverse'},
         'transitions': [{'id': 'sample'},
                         {'id': 'preserve'},
                         {'id': 'receive'},
                         {'id': 'retract'},
                         {'id': 'verify'},
                         {'id': 'prepublish'},
                         {'id': 'publish'},
                         {'id': 'republish'},
                         {'id': 'cancel'},
                         {'id': 'reinstate'}],
         'custom_actions': [],
         'columns': ['getRequestID',
                    'getSample',
                    'BatchID',
                    'SubGroup',
                    'Client',
                    'Creator',
                    'Created',
                    'getClientOrderNumber',
                    'getClientReference',
                    'ClientContact',
                    'getClientSampleID',
                    'getProfilesTitle',
                    'getTemplateTitle',
                    'getSampleTypeTitle',
                    'getSamplePointTitle',
                    'getStorageLocation',
                    'SamplingDeviation',
                    'Priority',
                    'AdHoc',
                    'SamplingDate',
                    'getDateSampled',
                    'getSampler',
                    'getDatePreserved',
                    'getPreserver',
                    'getDateReceived',
                    'getAnalysesNum',
                    'getDateVerified',
                    'state_title']},
        {'id': 'to_be_sampled',
         'title': _('To Be Sampled'),
         'contentFilter': {'review_state': ('to_be_sampled',),
                           'sort_on': 'created',
                           'sort_order': 'reverse'},
         'transitions': [{'id': 'sample'},
                         {'id': 'submit'},
                         {'id': 'cancel'},
                        ],
         'custom_actions': [],
         'columns': ['getRequestID',
                    'getSample',
                    'BatchID',
                    'SubGroup',
                    'Client',
                    'getProfilesTitle',
                    'getTemplateTitle',
                    'Creator',
                    'Created',
                    'getClientOrderNumber',
                    'getClientReference',
                    'getClientSampleID',
                    'ClientContact',
                    'getDateSampled',
                    'getSampler',
                    'getDatePreserved',
                    'getPreserver',
                    'getSampleTypeTitle',
                    'getSamplePointTitle',
                    'getStorageLocation',
                    'SamplingDeviation',
                    'Priority',
                    'AdHoc',
                    'getAnalysesNum',
                    'getDateVerified',
                    'state_title']},
        {'id': 'to_be_preserved',
         'title': _('To Be Preserved'),
         'contentFilter': {'review_state': ('to_be_preserved',),
                           'sort_on': 'created',
                           'sort_order': 'reverse'},
         'transitions': [{'id': 'preserve'},
                         {'id': 'cancel'},
                         ],
         'custom_actions': [],
         'columns': ['getRequestID',
                    'getSample',
                    'BatchID',
                    'SubGroup',
                    'Client',
                    'getProfilesTitle',
                    'getTemplateTitle',
                    'Creator',
                    'Created',
                    'getClientOrderNumber',
                    'getClientReference',
                    'getClientSampleID',
                    'ClientContact',
                    'getDateSampled',
                    'getSampler',
                    'getDatePreserved',
                    'getPreserver',
                    'getSampleTypeTitle',
                    'getSamplePointTitle',
                    'getStorageLocation',
                    'SamplingDeviation',
                    'Priority',
                    'AdHoc',
                    'getAnalysesNum',
                    'getDateVerified',
                    'state_title']},
        {'id': 'scheduled_sampling',
         'title': _('Scheduled sampling'),
         'contentFilter': {'review_state': ('scheduled_sampling',),
                           'sort_on': 'created',
                           'sort_order': 'reverse'},
         'transitions': [{'id': 'sample'},
                         {'id': 'cancel'},
                         ],
         'custom_actions': [],
         'columns': ['getRequestID',
                    'getSample',
                    'BatchID',
                    'SubGroup',
                    'Client',
                    'getProfilesTitle',
                    'getTemplateTitle',
                    'Creator',
                    'Created',
                    'getClientOrderNumber',
                    'getClientReference',
                    'getClientSampleID',
                    'ClientContact',
                    'getDateSampled',
                    'getSampler',
                    'getDatePreserved',
                    'getPreserver',
                    'getSampleTypeTitle',
                    'getSamplePointTitle',
                    'getStorageLocation',
                    'SamplingDeviation',
                    'Priority',
                    'AdHoc',
                    'getAnalysesNum',
                    'getDateVerified',
                    'state_title']},
        {'id': 'sample_due',
         'title': _('Due'),
         'contentFilter': {'review_state': ('to_be_sampled',
                                            'to_be_preserved',
                                            'sample_due'),
                           'sort_on': 'created',
                           'sort_order': 'reverse'},
         'transitions': [{'id': 'sample'},
                         {'id': 'preserve'},
                         {'id': 'receive'},
                         {'id': 'cancel'},
                         {'id': 'reinstate'}],
         'custom_actions': [],
         'columns': ['getRequestID',
                    'getSample',
                    'BatchID',
                    'SubGroup',
                    'Client',
                    'getProfilesTitle',
                    'getTemplateTitle',
                    'Creator',
                    'Created',
                    'getClientOrderNumber',
                    'getClientReference',
                    'getClientSampleID',
                    'ClientContact',
                    'getDateSampled',
                    'getSampler',
                    'getDatePreserved',
                    'getPreserver',
                    'getSampleTypeTitle',
                    'getSamplePointTitle',
                    'getStorageLocation',
                    'SamplingDeviation',
                    'Priority',
                    'AdHoc',
                    'getAnalysesNum',
                    'getDateVerified',
                    'state_title']},
       {'id': 'sample_received',
         'title': _('Received'),
         'contentFilter': {'review_state': 'sample_received',
                           'sort_on': 'created',
                           'sort_order': 'reverse'},
         'transitions': [{'id': 'prepublish'},
                         {'id': 'cancel'},
                         {'id': 'reinstate'}],
         'custom_actions': [],
         'columns': ['getRequestID',
                    'getSample',
                    'BatchID',
                    'SubGroup',
                    'Client',
                    'getProfilesTitle',
                    'getTemplateTitle',
                    'Creator',
                    'Created',
                    'getClientOrderNumber',
                    'getClientReference',
                    'getClientSampleID',
                    'ClientContact',
                    'getSampleTypeTitle',
                    'getSamplePointTitle',
                    'getStorageLocation',
                    'SamplingDeviation',
                    'Priority',
                    'AdHoc',
                    'getDateSampled',
                    'getSampler',
                    'getDatePreserved',
                    'getPreserver',
                    'getAnalysesNum',
                    'getDateVerified',
                    'getDateReceived']},
        {'id': 'to_be_verified',
         'title': _('To be verified'),
         'contentFilter': {'review_state': 'to_be_verified',
                           'sort_on': 'created',
                           'sort_order': 'reverse'},
         'transitions': [{'id': 'retract'},
                         {'id': 'verify'},
                         {'id': 'prepublish'},
                         {'id': 'cancel'},
                         {'id': 'reinstate'}],
         'custom_actions': [],
         'columns': ['getRequestID',
                    'getSample',
                    'BatchID',
                    'SubGroup',
                    'Client',
                    'getProfilesTitle',
                    'getTemplateTitle',
                    'Creator',
                    'Created',
                    'getClientOrderNumber',
                    'getClientReference',
                    'getClientSampleID',
                    'ClientContact',
                    'getSampleTypeTitle',
                    'getSamplePointTitle',
                    'getStorageLocation',
                    'SamplingDeviation',
                    'Priority',
                    'AdHoc',
                    'getDateSampled',
                    'getSampler',
                    'getDatePreserved',
                    'getPreserver',
                    'getAnalysesNum',
                    'getDateVerified',
                    'getDateReceived']},
        {'id': 'verified',
         'title': _('Verified'),
         'contentFilter': {'review_state': 'verified',
                           'sort_on': 'created',
                           'sort_order': 'reverse'},
         'transitions': [{'id': 'publish'},
                         {'id': 'cancel'},
                         ],
         'custom_actions': [],
         'columns': ['getRequestID',
                    'getSample',
                    'BatchID',
                    'SubGroup',
                    'Client',
                    'getProfilesTitle',
                    'getTemplateTitle',
                    'Creator',
                    'Created',
                    'getClientOrderNumber',
                    'getClientReference',
                    'getClientSampleID',
                    'ClientContact',
                    'getSampleTypeTitle',
                    'getSamplePointTitle',
                    'getStorageLocation',
                    'SamplingDeviation',
                    'Priority',
                    'AdHoc',
                    'getDateSampled',
                    'getSampler',
                    'getDatePreserved',
                    'getPreserver',
                    'getAnalysesNum',
                    'getDateVerified',
                    'getDateReceived']},
        {'id': 'published',
         'title': _('Published'),
         'contentFilter': {'review_state': ('published', 'invalid'),
                           'sort_on': 'created',
                           'sort_order': 'reverse'},
         'transitions': [{'id': 'republish'}],
         'custom_actions': [],
         'columns': ['getRequestID',
                    'getSample',
                    'BatchID',
                    'SubGroup',
                    'Client',
                    'getProfilesTitle',
                    'getTemplateTitle',
                    'Creator',
                    'Created',
                    'getClientOrderNumber',
                    'getClientReference',
                    'getClientSampleID',
                    'ClientContact',
                    'getSampleTypeTitle',
                    'getSamplePointTitle',
                    'getStorageLocation',
                    'SamplingDeviation',
                    'Priority',
                    'AdHoc',
                    'getDateSampled',
                    'getSampler',
                    'getDatePreserved',
                    'getPreserver',
                    'getDateReceived',
                    'getAnalysesNum',
                    'getDateVerified',
                    'getDatePublished']},
        {'id': 'cancelled',
         'title': _('Cancelled'),
         'contentFilter': {'cancellation_state': 'cancelled',
                           'review_state': (
                               'sample_registered',
                               'to_be_sampled',
                               'to_be_preserved',
                               'sample_due',
                               'sample_received',
                               'to_be_verified',
                               'attachment_due',
                               'verified',
                               'published'),
                           'sort_on': 'created',
                           'sort_order': 'reverse'},
         'transitions': [{'id': 'reinstate'}],
         'custom_actions': [],
         'columns': ['getRequestID',
                    'getSample',
                    'BatchID',
                    'SubGroup',
                    'Client',
                    'getProfilesTitle',
                    'getTemplateTitle',
                    'Creator',
                    'Created',
                    'getClientOrderNumber',
                    'getClientReference',
                    'getClientSampleID',
                    'ClientContact',
                    'getSampleTypeTitle',
                    'getSamplePointTitle',
                    'getStorageLocation',
                    'SamplingDeviation',
                    'Priority',
                    'AdHoc',
                    'getDateSampled',
                    'getSampler',
                    'getDatePreserved',
                    'getPreserver',
                    'getDateReceived',
                    'getDatePublished',
                    'getAnalysesNum',
                    'getDateVerified',
                    'state_title']},
        {'id': 'invalid',
         'title': _('Invalid'),
         'contentFilter': {'review_state': 'invalid',
                           'sort_on': 'created',
                           'sort_order': 'reverse'},
         'transitions': [],
         'custom_actions': [],
         'columns':['getRequestID',
                    'getSample',
                    'BatchID',
                    'SubGroup',
                    'Client',
                    'getProfilesTitle',
                    'getTemplateTitle',
                    'Creator',
                    'Created',
                    'getClientOrderNumber',
                    'getClientReference',
                    'getClientSampleID',
                    'ClientContact',
                    'getSampleTypeTitle',
                    'getSamplePointTitle',
                    'getStorageLocation',
                    'SamplingDeviation',
                    'Priority',
                    'AdHoc',
                    'getDateSampled',
                    'getSampler',
                    'getDatePreserved',
                    'getPreserver',
                    'getDateReceived',
                    'getAnalysesNum',
                    'getDateVerified',
                    'getDatePublished']},
        {'id': 'assigned',
         'title': "<img title='%s'\
                   src='%s/++resource++bika.lims.images/assigned.png'/>" % (
                   t(_("Assigned")), self.portal_url),
         'contentFilter': {'worksheetanalysis_review_state': 'assigned',
                           'review_state': ('sample_received', 'to_be_verified',
                                            'attachment_due', 'verified',
                                            'published'),
                           'sort_on': 'created',
                           'sort_order': 'reverse'},
         'transitions': [{'id': 'retract'},
                         {'id': 'verify'},
                         {'id': 'prepublish'},
                         {'id': 'publish'},
                         {'id': 'republish'},
                         {'id': 'cancel'},
                         {'id': 'reinstate'}],
         'custom_actions': [],
         'columns': ['getRequestID',
                    'getSample',
                    'BatchID',
                    'SubGroup',
                    'Client',
                    'getProfilesTitle',
                    'getTemplateTitle',
                    'Creator',
                    'Created',
                    'getClientOrderNumber',
                    'getClientReference',
                    'getClientSampleID',
                    'ClientContact',
                    'getSampleTypeTitle',
                    'getSamplePointTitle',
                    'getStorageLocation',
                    'SamplingDeviation',
                    'Priority',
                    'AdHoc',
                    'getDateSampled',
                    'getSampler',
                    'getDatePreserved',
                    'getPreserver',
                    'getDateReceived',
                    'getAnalysesNum',
                    'getDateVerified',
                    'state_title']},
        {'id': 'unassigned',
         'title': "<img title='%s'\
                   src='%s/++resource++bika.lims.images/unassigned.png'/>" % (
                   t(_("Unassigned")), self.portal_url),
         'contentFilter': {'worksheetanalysis_review_state': 'unassigned',
                           'review_state': ('sample_received', 'to_be_verified',
                                            'attachment_due', 'verified',
                                            'published'),
                           'sort_on': 'created',
                           'sort_order': 'reverse'},
         'transitions': [{'id': 'receive'},
                         {'id': 'retract'},
                         {'id': 'verify'},
                         {'id': 'prepublish'},
                         {'id': 'publish'},
                         {'id': 'republish'},
                         {'id': 'cancel'},
                         {'id': 'reinstate'}],
         'custom_actions': [],
         'columns': ['getRequestID',
                    'getSample',
                    'BatchID',
                    'SubGroup',
                    'Client',
                    'getProfilesTitle',
                    'getTemplateTitle',
                    'Creator',
                    'Created',
                    'getClientOrderNumber',
                    'getClientReference',
                    'getClientSampleID',
                    'ClientContact',
                    'getSampleTypeTitle',
                    'getSamplePointTitle',
                    'getStorageLocation',
                    'SamplingDeviation',
                    'Priority',
                    'AdHoc',
                    'SamplingDate',
                    'getDateSampled',
                    'getSampler',
                    'getDatePreserved',
                    'getPreserver',
                    'getDateReceived',
                    'getAnalysesNum',
                    'getDateVerified',
                    'state_title']},
        {'id': 'rejected',
         'title': _('Rejected'),
         'contentFilter': {'review_state': 'rejected',
                           'sort_on': 'created',
                           'sort_order': 'reverse'},
         'transitions': [],
         'custom_actions': [],
         'columns': ['getRequestID',
                    'getSample',
                    'BatchID',
                    'SubGroup',
                    'Client',
                    'getProfilesTitle',
                    'getTemplateTitle',
                    'Creator',
                    'Created',
                    'getClientOrderNumber',
                    'getClientReference',
                    'getClientSampleID',
                    'ClientContact',
                    'getSampleTypeTitle',
                    'getSamplePointTitle',
                    'getStorageLocation',
                    'SamplingDeviation',
                    'Priority',
                    'AdHoc',
                    'getDateSampled',
                    'getSampler',
                    'getDatePreserved',
                    'getPreserver',
                    'getDateReceived',
                    'getDatePublished',
                    'getAnalysesNum',
                    'state_title']},
        ]

def folderitems(self, full_objects=False):
    items = super(AnalysisRequestsView, self).folderitems()
    if not self.request.get('analysisrequests_sort_on') or \
       self.request.analysisrequests_sort_on in (
                'created', 'getRequestID', 'getSample'):
        #Sort on AR ID sequence number
        reverse = False
        if self.request.get('analysisrequests_sort_on') and \
           self.request.analysisrequests_sort_on != 'created' and \
           self.request.analysisrequests_sort_order == 'descending':
            reverse = True
        items = sorted(
                items, 
                lambda x, y: cmp( x['id'].split('-')[3], y['id'].split('-')[3]),
                reverse=reverse)
    return items



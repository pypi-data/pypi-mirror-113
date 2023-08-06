from Products.Five import BrowserView
from itertools import chain
from plone.app.workflow.browser.sharing import merge_search_results
# from plone.restapi.interfaces import ISerializeToJsonSummary
# from plone.restapi.services import Service
from Products.CMFCore.utils import getToolByName
from zExceptions import BadRequest
from zope.component import getMultiAdapter
import json


class SearchForPrincipals(BrowserView):
    """
    Task of this view is to search and return
    list of users to the js plugin used for
    mentioning operation in text area
    """

    def __call__(self):
        """
        this is taken directly from plone.restapi 2.0.0
        I don't need stuff about authentication so i transform
        this service in a view protecting it with a permission
        for authenticated
        """
        if self.request.form.get('search', False):
            self.search_term = self.request.form['search']
        else:
            return json.dumps([])

        principals = self.serialize_principals(self.user_search_results())
        return json.dumps(principals)

    def serialize_principals(self, principals):
        result = []
        portal_membership = self.context.portal_membership
        for principal in principals:
            result.append(
                {
                    'value': principal.getId(),
                    'key': principal.getProperty('fullname'),
                    'image': portal_membership.getPersonalPortrait(
                        principal.getId()).absolute_url()
                }
            )
        return result

    def user_search_results(self):
        def search_for_principal(hunter, search_term):
            return merge_search_results(
                chain(*[hunter.searchUsers(**{field: search_term})
                      for field in ['name', 'fullname', 'email']]), 'userid')

        def get_principal_by_id(user_id):
            mtool = getToolByName(self.context, 'portal_membership')
            return mtool.getMemberById(user_id)

        return self._principal_search_results(
            search_for_principal, get_principal_by_id, 'user', 'userid')


    def _principal_search_results(
            self, search_for_principal,
            get_principal_by_id,
            principal_type,
            id_key):

        hunter = getMultiAdapter(
            (self.context, self.request), name='pas_search')

        principals = []
        for principal_info in search_for_principal(hunter, self.search_term):
            principal_id = principal_info[id_key]
            principals.append(get_principal_by_id(principal_id))

        return principals

from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView, DeleteView,
                                  TemplateView)

from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from portfolio.forms import AccountForm
from portfolio.models import Account
from .serializers import AccountSerializer


class AccountListView(TemplateView):
    # model = Account
    template_name = 'portfolio/account_list.html'

    def dispatch(self, request, *args, **kwargs):
        return super(AccountListView, self).dispatch(request, *args, **kwargs)
    
class AccountEditView(UpdateView):
    model = Account
    form_class = AccountForm
    success_url = "/portfolio"

class AccountCreateView(CreateView):
    model = Account
    form_class = AccountForm
    success_url = "/portfolio"

class AccountDeleteView(DeleteView):
    model = Account
    success_url = "/portfolio"

class AccountViewSet(viewsets.ModelViewSet):
    '''View to manage accounts'''

    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def create(self, request):
        try:
            return super(SettingsViewSet, self).create(request)
        except ValidationError as e:
            return Response({'error': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

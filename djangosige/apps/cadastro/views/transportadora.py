# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse_lazy

from djangosige.apps.cadastro.forms import TransportadoraForm, VeiculoFormSet
from djangosige.apps.cadastro.models import Transportadora, Veiculo

from .base import AdicionarPessoaView, PessoasListView, EditarPessoaView


class AdicionarTransportadoraView(AdicionarPessoaView):
    template_name = "cadastro/pessoa_add.html"
    success_url = reverse_lazy('cadastro:listatransportadorasview')
    success_message = "Transportadora <b>%(nome_razao_social)s </b>adicionada com sucesso."

    def get_context_data(self, **kwargs):
        context = super(AdicionarTransportadoraView, self).get_context_data(**kwargs)
        context['title_complete'] = 'CADASTRAR TRANSPORTADORA'
        context['return_url'] = reverse_lazy('cadastro:listatransportadorasview')
        context['tipo_pessoa'] = 'transportadora'
        return context

    def get(self, request, *args, **kwargs):
        form = TransportadoraForm(prefix='transportadora_form')
        veiculo_form = VeiculoFormSet(prefix='veiculo_form')
        veiculo_form.can_delete = False
        return super(AdicionarTransportadoraView, self).get(request, form, *args, **kwargs, veiculo_form=veiculo_form)

    def post(self, request, *args, **kwargs):
        form = TransportadoraForm(request.POST, request.FILES, prefix='transportadora_form', request=request)
        veiculo_form = VeiculoFormSet(request.POST, prefix='veiculo_form')
        return super(AdicionarTransportadoraView, self).post(request, form, *args, **kwargs, veiculo_form=veiculo_form)


class TransportadorasListView(PessoasListView):
    template_name = 'cadastro/pessoa_list.html'
    model = Transportadora
    context_object_name = 'all_transportadoras'
    success_url = reverse_lazy('cadastro:listatransportadorasview')

    def get_context_data(self, **kwargs):
        context = super(TransportadorasListView, self).get_context_data(**kwargs)
        context['title_complete'] = 'TRANSPORTADORAS CADASTRADAS'
        context['add_url'] = reverse_lazy('cadastro:addtransportadoraview')
        context['tipo_pessoa'] = 'transportadora'
        return context

    def get_queryset(self):
        return super(TransportadorasListView, self).get_queryset(object=Transportadora)

    def post(self, request, *args, **kwargs):
        return super(TransportadorasListView, self).post(request, Transportadora)


class EditarTransportadoraView(EditarPessoaView):
    form_class = TransportadoraForm
    model = Transportadora
    template_name = "cadastro/pessoa_edit.html"
    success_url = reverse_lazy('cadastro:listatransportadorasview')
    success_message = "Transportadora <b>%(nome_razao_social)s </b>editada com sucesso."

    def get_context_data(self, **kwargs):
        context = super(EditarTransportadoraView, self).get_context_data(**kwargs)
        context['return_url'] = reverse_lazy('cadastro:listatransportadorasview')
        context['tipo_pessoa'] = 'transportadora'
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form_class.prefix = "transportadora_form"
        form = self.get_form(form_class)

        veiculo_form = VeiculoFormSet(instance=self.object, prefix='veiculo_form')
        if Veiculo.objects.filter(transportadora_veiculo=self.object.pk).count():
            veiculo_form.extra = 0

        return super(EditarTransportadoraView, self).get(request, form, *args, **kwargs, veiculo_form=veiculo_form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = form_class(request.POST, request.FILES, prefix='transportadora_form', instance=self.object, request=request)

        veiculo_form = VeiculoFormSet(request.POST, prefix='veiculo_form', instance=self.object)

        return super(EditarTransportadoraView, self).post(request, form, *args, **kwargs, veiculo_form=veiculo_form)

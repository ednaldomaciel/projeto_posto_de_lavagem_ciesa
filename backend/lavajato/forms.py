from django import forms
from .models import EmpresaFaturada, OrdemServico, Veiculo, Cliente, Servico, Lavador, Pagamento


class ClienteCadastroForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'tipo', 'empresa_faturada', 'telefone', 'documento', 'observacoes']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'w-full bg-slate-50 border border-slate-300 rounded-lg p-2.5 text-sm'}),
            'tipo': forms.Select(attrs={'class': 'w-full bg-slate-50 border border-slate-300 rounded-lg p-2.5 text-sm'}),
            'empresa_faturada': forms.Select(attrs={'class': 'w-full bg-slate-50 border border-slate-300 rounded-lg p-2.5 text-sm'}),
            'telefone': forms.TextInput(attrs={'class': 'w-full bg-slate-50 border border-slate-300 rounded-lg p-2.5 text-sm'}),
            'documento': forms.TextInput(attrs={'class': 'w-full bg-slate-50 border border-slate-300 rounded-lg p-2.5 text-sm'}),
            'observacoes': forms.Textarea(attrs={'rows': 2, 'class': 'w-full bg-slate-50 border border-slate-300 rounded-lg p-2.5 text-sm'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['empresa_faturada'].queryset = EmpresaFaturada.objects.filter(ativo=True)


class VeiculoCadastroForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['placa', 'modelo', 'cor', 'tipo_veiculo']
        widgets = {
            'placa': forms.TextInput(attrs={'class': 'w-full bg-slate-50 border border-slate-300 rounded-lg p-2.5 text-sm font-mono uppercase', 'placeholder': 'Ex: ABC1D23'}),
            'modelo': forms.TextInput(attrs={'class': 'w-full bg-slate-50 border border-slate-300 rounded-lg p-2.5 text-sm'}),
            'cor': forms.TextInput(attrs={'class': 'w-full bg-slate-50 border border-slate-300 rounded-lg p-2.5 text-sm'}),
            'tipo_veiculo': forms.Select(attrs={'class': 'w-full bg-slate-50 border border-slate-300 rounded-lg p-2.5 text-sm'}),
        }


class OrdemServicoForm(forms.ModelForm):
    class Meta:
        model = OrdemServico
        fields = ['veiculo', 'servico', 'lavador', 'observacoes_veiculo']
        widgets = {
            'veiculo': forms.Select(attrs={'class': 'w-full bg-slate-50 border border-slate-300 rounded-lg p-2.5 text-sm focus:ring-2 focus:ring-blue-500 outline-none'}),
            'servico': forms.Select(attrs={'class': 'w-full bg-slate-50 border border-slate-300 rounded-lg p-2.5 text-sm focus:ring-2 focus:ring-blue-500 outline-none'}),
            'lavador': forms.Select(attrs={'class': 'w-full bg-slate-50 border border-slate-300 rounded-lg p-2.5 text-sm focus:ring-2 focus:ring-blue-500 outline-none'}),
            'observacoes_veiculo': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Vistoria: riscos, avarias ou pertences no veículo', 'class': 'w-full bg-slate-50 border border-slate-300 rounded-lg p-2.5 text-sm focus:ring-2 focus:ring-blue-500 outline-none'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['servico'].queryset = Servico.objects.filter(ativo=True)
        self.fields['lavador'].queryset = Lavador.objects.filter(ativo=True)


class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ['forma_pagamento', 'momento_pagamento', 'valor_pago']
        widgets = {
            'forma_pagamento': forms.Select(attrs={'class': 'w-full bg-slate-50 border border-slate-300 rounded-lg p-2 text-sm'}),
            'momento_pagamento': forms.Select(attrs={'class': 'w-full bg-slate-50 border border-slate-300 rounded-lg p-2 text-sm'}),
            'valor_pago': forms.NumberInput(attrs={'step': '0.01', 'class': 'w-full bg-slate-50 border border-slate-300 rounded-lg p-2 text-sm font-bold'}),
        }


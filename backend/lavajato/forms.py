from django import forms
from .models import OrdemServico, Veiculo, Cliente, Servico, Lavador, Pagamento


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


from django.contrib import admin
from django.utils.html import format_html
from .models import Cliente, Veiculo, Lavador, Servico, OrdemServico, Pagamento


class VeiculoInline(admin.TabularInline):
    model = Veiculo
    extra = 1


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo_badge', 'telefone', 'documento', 'total_veiculos', 'ativo', 'data_cadastro')
    list_filter = ('tipo', 'ativo')
    search_fields = ('nome', 'documento', 'telefone')
    inlines = [VeiculoInline]

    @admin.display(description='Tipo')
    def tipo_badge(self, obj):
        if obj.tipo == 'FATURADO':
            return format_html('<span style="background-color: #dbeafe; color: #1e40af; padding: 3px 8px; border-radius: 6px; font-weight: bold;">🏢 Faturado</span>')
        return format_html('<span style="background-color: #f3f4f6; color: #374151; padding: 3px 8px; border-radius: 6px;">👤 Avulso</span>')

    @admin.display(description='Veículos')
    def total_veiculos(self, obj):
        return obj.veiculos.count()


@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'marca', 'modelo', 'cor', 'tipo_veiculo', 'cliente', 'status_semanal')
    list_filter = ('tipo_veiculo', 'cliente__tipo')
    search_fields = ('placa', 'modelo', 'marca', 'cliente__nome', 'cliente__documento')

    @admin.display(description='Limite Semanal (RN01)')
    def status_semanal(self, obj):
        permitido, motivo = obj.pode_lavar_esta_semana()
        if permitido:
            return format_html('<span style="color: #16a34a; font-weight: 500;">✓ Apto</span>')
        return format_html('<span style="color: #dc2626; font-weight: bold;" title="{}">⚠️ Limite Atingido</span>', motivo)


@admin.register(Lavador)
class LavadorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'percentual_comissao', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('nome', 'cpf', 'telefone')


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor_formatado', 'tempo_estimado_minutos', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('descricao',)

    @admin.display(description='Valor')
    def valor_formatado(self, obj):
        return f"R$ {obj.valor:.2f}"


class PagamentoInline(admin.StackedInline):
    model = Pagamento
    extra = 0
    can_delete = False


@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    list_display = ('id_formatado', 'veiculo', 'servico', 'lavador', 'status_badge', 'valor_total_formatado', 'comissao_calculada', 'data_hora')
    list_filter = ('status', 'servico', 'lavador', 'data_hora')
    search_fields = ('id', 'veiculo__placa', 'veiculo__cliente__nome')
    readonly_fields = ('data_hora', 'comissao_calculada')
    inlines = [PagamentoInline]

    @admin.display(description='OS #')
    def id_formatado(self, obj):
        return f"#{obj.id:04d}"

    @admin.display(description='Status')
    def status_badge(self, obj):
        colors = {
            'FILA': ('#fef3c7', '#92400e'),
            'LAVAGEM': ('#dbeafe', '#1e40af'),
            'SECAGEM': ('#e0e7ff', '#3730a3'),
            'CONCLUIDO': ('#dcfce7', '#166534'),
            'ENTREGUE': ('#f3f4f6', '#374151'),
        }
        bg, fg = colors.get(obj.status, ('#f3f4f6', '#111827'))
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 4px 8px; border-radius: 6px; font-weight: bold; font-size: 11px;">{}</span>',
            bg, fg, obj.get_status_display()
        )

    @admin.display(description='Total')
    def valor_total_formatado(self, obj):
        return f"R$ {obj.valor_total:.2f}" if obj.valor_total else "-"

    @admin.display(description='Comissão Lavador (RF03)')
    def comissao_calculada(self, obj):
        return f"R$ {obj.valor_comissao:.2f}"


@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ('ordem_servico', 'forma_pagamento', 'momento_pagamento', 'status', 'valor_pago_formatado', 'data_pagamento')
    list_filter = ('forma_pagamento', 'momento_pagamento', 'status')
    search_fields = ('ordem_servico__id', 'ordem_servico__veiculo__placa')

    @admin.display(description='Valor Pago')
    def valor_pago_formatado(self, obj):
        return f"R$ {obj.valor_pago:.2f}"


# Personalização do Cabeçalho do Django Admin
admin.site.site_header = "Lava Jato do Valmir - Painel de Controle"
admin.site.site_title = "Lava Jato do Valmir"
admin.site.index_title = "Administração do Posto de Lavagem (CIESA)"

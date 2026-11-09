from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.db.models import Sum, Count, Q
from .models import OrdemServico, Veiculo, Lavador, Servico, Pagamento, Cliente
from .forms import OrdemServicoForm, PagamentoForm


def login_view(request):
    """Tela de login customizada com suporte a acesso rápido de teste (RF01, RNF01)."""
    if request.user.is_authenticated:
        return redirect(request.GET.get('next', 'recepcao'))

    if request.method == 'POST':
        # Suporte a botão de login rápido para testes
        quick_user = request.POST.get('quick_user')
        if quick_user in ['admin', 'juliana']:
            user = User.objects.filter(username=quick_user).first()
            if user:
                auth_login(request, user)
                messages.success(request, f"Conectado com sucesso como {user.get_full_name() or user.username}!")
                return redirect(request.POST.get('next') or request.GET.get('next') or 'recepcao')

        usuario = request.POST.get('username')
        senha = request.POST.get('password')
        user = authenticate(request, username=usuario, password=senha)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Bem-vindo(a), {user.get_full_name() or user.username}!")
            return redirect(request.POST.get('next') or request.GET.get('next') or 'recepcao')
        else:
            messages.error(request, "Usuário ou senha inválidos. Tente novamente.")

    return render(request, 'lavajato/login.html', {'next': request.GET.get('next', '')})


def logout_view(request):
    """Encerra a sessão do usuário."""
    auth_logout(request)
    messages.info(request, "Você encerrou a sessão.")
    return redirect('login')


def is_admin(user):
    """RN03: Verifica se o usuário possui perfil de Administrador."""
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name='Administrador').exists())


@login_required
def recepcao_view(request):
    """
    Painel de Recepção e Atendimento (RF01, RF02, RF05, RN01, RN02).
    Permite busca rápida por placa, valida limite de clientes faturados e emite OS.
    """
    termo_placa = request.GET.get('placa', '').strip().upper().replace('-', '')
    veiculo_selecionado = None
    alerta_rn01 = None

    if termo_placa:
        veiculo_selecionado = Veiculo.objects.filter(placa=termo_placa).select_related('cliente').first()
        if veiculo_selecionado:
            permitido, motivo = veiculo_selecionado.pode_lavar_esta_semana()
            if not permitido:
                alerta_rn01 = {
                    'tipo': 'danger',
                    'titulo': 'Bloqueio de Regra RN01 (Limite Semanal Excedido):',
                    'mensagem': motivo
                }
            elif veiculo_selecionado.cliente.tipo == 'FATURADO':
                alerta_rn01 = {
                    'tipo': 'info',
                    'titulo': 'Cliente Conveniado / Faturado:',
                    'mensagem': 'Veículo apto. Nenhuma lavagem registrada para esta frota na semana corrente.'
                }
        else:
            messages.warning(request, f"Placa '{termo_placa}' não cadastrada. Cadastre o veículo no Admin ou selecione abaixo.")

    if request.method == 'POST':
        form = OrdemServicoForm(request.POST)
        if form.is_valid():
            try:
                os = form.save(commit=False)
                os.usuario = request.user
                os.full_clean()
                os.save()

                # Registro de pagamento na entrada (se selecionado forma de pagamento no modal/form)
                forma_pgto = request.POST.get('forma_pagamento')
                momento_pgto = request.POST.get('momento_pagamento', 'ENTRADA')
                if forma_pgto:
                    Pagamento.objects.create(
                        ordem_servico=os,
                        forma_pagamento=forma_pgto,
                        momento_pagamento=momento_pgto,
                        status='CONCLUIDO' if momento_pgto == 'ENTRADA' else 'PENDENTE',
                        valor_pago=os.valor_total
                    )

                messages.success(request, f"Ordem de Serviço #{os.id:04d} para o veículo {os.veiculo.placa} aberta com sucesso!")
                return redirect('recepcao')
            except Exception as e:
                messages.error(request, f"Erro ao registrar OS: {e}")
    else:
        initial_data = {}
        if veiculo_selecionado:
            initial_data['veiculo'] = veiculo_selecionado
        form = OrdemServicoForm(initial=initial_data)

    # Ordens ativas no pátio (em tempo real)
    ordens_ativas = OrdemServico.objects.exclude(status='ENTREGUE').select_related(
        'veiculo', 'servico', 'lavador', 'pagamento'
    ).order_by('-data_hora')

    servicos_disponiveis = Servico.objects.filter(ativo=True)
    lavadores_disponiveis = Lavador.objects.filter(ativo=True)

    context = {
        'form': form,
        'termo_placa': termo_placa,
        'veiculo_selecionado': veiculo_selecionado,
        'alerta_rn01': alerta_rn01,
        'ordens_ativas': ordens_ativas,
        'servicos_disponiveis': servicos_disponiveis,
        'lavadores_disponiveis': lavadores_disponiveis,
        'hoje': timezone.localtime(timezone.now()),
    }
    return render(request, 'lavajato/recepcao.html', context)


@login_required
def patio_view(request):
    """
    Painel do Pátio e Lavadores (RF03, RF05, RNF02).
    Interface mobile/tablet para acompanhamento e alteração de status em tempo real.
    """
    if request.method == 'POST':
        os_id = request.POST.get('os_id')
        novo_status = request.POST.get('novo_status')
        os = get_object_or_404(OrdemServico, id=os_id)

        status_validos = dict(OrdemServico.STATUS_CHOICES)
        if novo_status in status_validos:
            os.status = novo_status
            if novo_status in ['CONCLUIDO', 'ENTREGUE'] and not os.data_hora_saida:
                os.data_hora_saida = timezone.now()
            os.save(update_fields=['status', 'data_hora_saida'])
            messages.success(request, f"OS #{os.id:04d} ({os.veiculo.placa}) alterada para: {status_validos[novo_status]}")
        return redirect('patio')

    # Fila de lavagem ativa no pátio
    ordens_patio = OrdemServico.objects.filter(
        status__in=['FILA', 'LAVAGEM', 'SECAGEM', 'CONCLUIDO']
    ).select_related('veiculo', 'servico', 'lavador').order_by('data_hora')

    context = {
        'ordens_patio': ordens_patio,
        'total_fila': ordens_patio.filter(status='FILA').count(),
        'total_lavagem': ordens_patio.filter(status='LAVAGEM').count(),
        'total_secagem': ordens_patio.filter(status='SECAGEM').count(),
        'total_concluido': ordens_patio.filter(status='CONCLUIDO').count(),
    }
    return render(request, 'lavajato/patio.html', context)


@login_required
@user_passes_test(is_admin, login_url='/recepcao/')
def gerenciamento_view(request):
    """
    Painel Administrativo e Fechamento de Caixa Diário (RF08, RN03).
    Acesso restrito ao perfil Administrador (Seu Valmir).
    """
    hoje = timezone.localtime(timezone.now()).date()

    # Ordens do dia
    ordens_hoje = OrdemServico.objects.filter(data_hora__date=hoje).select_related('servico', 'lavador')
    pagamentos_hoje = Pagamento.objects.filter(data_pagamento__date=hoje, status='CONCLUIDO')

    # Métricas Financeiras
    faturamento_diario = pagamentos_hoje.aggregate(total=Sum('valor_pago'))['total'] or Decimal('0.00')
    total_lavagens_concluidas = ordens_hoje.filter(status__in=['CONCLUIDO', 'ENTREGUE']).count()

    # Cálculo do total de comissões acumuladas hoje
    total_comissoes = sum(os.valor_comissao for os in ordens_hoje.filter(status__in=['CONCLUIDO', 'ENTREGUE']))
    lucro_liquido = faturamento_diario - Decimal(str(total_comissoes))

    # Desempenho por Lavador
    desempenho_lavadores = []
    for lavador in Lavador.objects.filter(ativo=True):
        os_lavador = ordens_hoje.filter(lavador=lavador, status__in=['CONCLUIDO', 'ENTREGUE'])
        qtd = os_lavador.count()
        comissao = sum(os.valor_comissao for os in os_lavador)
        desempenho_lavadores.append({
            'lavador': lavador,
            'quantidade': qtd,
            'comissao': comissao
        })

    # Resumo por Forma de Pagamento
    formas_pgto = pagamentos_hoje.values('forma_pagamento').annotate(
        total=Sum('valor_pago'),
        qtd=Count('id')
    ).order_by('-total')

    context = {
        'data_atual': hoje,
        'faturamento_diario': faturamento_diario,
        'total_lavagens_concluidas': total_lavagens_concluidas,
        'total_comissoes': total_comissoes,
        'lucro_liquido': lucro_liquido,
        'desempenho_lavadores': desempenho_lavadores,
        'formas_pgto': formas_pgto,
        'ultimas_ordens': ordens_hoje.order_by('-data_hora')[:10],
    }
    return render(request, 'lavajato/gerenciamento.html', context)


@login_required
def registrar_pagamento_os(request, os_id):
    """
    Registra ou liquida pagamento de uma OS na retirada/saída (RF06, RN02).
    """
    os = get_object_or_404(OrdemServico, id=os_id)

    if request.method == 'POST':
        forma = request.POST.get('forma_pagamento', 'PIX')
        valor = os.valor_total or os.servico.valor

        pagamento, _ = Pagamento.objects.get_or_create(
            ordem_servico=os,
            defaults={
                'forma_pagamento': forma,
                'momento_pagamento': 'RETIRADA',
                'status': 'CONCLUIDO',
                'valor_pago': valor
            }
        )
        pagamento.forma_pagamento = forma
        pagamento.status = 'CONCLUIDO'
        pagamento.valor_pago = valor
        pagamento.save()

        os.status = 'ENTREGUE'
        if not os.data_hora_saida:
            os.data_hora_saida = timezone.now()
        os.save(update_fields=['status', 'data_hora_saida'])

        messages.success(request, f"Pagamento da OS #{os.id:04d} confirmado com sucesso!")

    return redirect('recepcao')

import calendar
from datetime import datetime, date, timedelta
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
    Painel Administrativo, Caixa e Central de Relatórios (RF08, RN03).
    Acesso restrito ao Administrador (Seu Valmir).
    Suporta relatórios por categorias:
      - 'diario': Fechamento de caixa diário por data selecionada.
      - 'mensal': Consolidado mensal por mês e ano.
      - 'comissoes': Extrato de comissões por lavador no período.
      - 'faturado': Relatório de faturamento e cobrança de empresas conveniadas por período.
    """
    hoje = timezone.localtime(timezone.now()).date()
    tipo_relatorio = request.GET.get('tipo', 'diario')

    # Dados base para seletores
    empresas_faturadas = Cliente.objects.filter(tipo='FATURADO', ativo=True).order_by('nome')
    lavadores_todos = Lavador.objects.filter(ativo=True).order_by('nome')

    context = {
        'hoje': hoje,
        'tipo_relatorio': tipo_relatorio,
        'empresas_faturadas': empresas_faturadas,
        'lavadores_todos': lavadores_todos,
    }

    # =========================================================================
    # CATEGORIA 1: RELATÓRIO DIÁRIO (Fechamento de Caixa Diário)
    # =========================================================================
    if tipo_relatorio == 'diario':
        data_param = request.GET.get('data')
        try:
            data_selecionada = datetime.strptime(data_param, '%Y-%m-%d').date() if data_param else hoje
        except (ValueError, TypeError):
            data_selecionada = hoje

        ordens_dia = OrdemServico.objects.filter(data_hora__date=data_selecionada).select_related(
            'veiculo', 'veiculo__cliente', 'servico', 'lavador', 'pagamento'
        ).order_by('-data_hora')

        pagamentos_dia = Pagamento.objects.filter(data_pagamento__date=data_selecionada, status='CONCLUIDO')

        faturamento_diario = pagamentos_dia.aggregate(total=Sum('valor_pago'))['total'] or Decimal('0.00')
        ordens_finalizadas = ordens_dia.filter(status__in=['CONCLUIDO', 'ENTREGUE'])
        total_lavagens = ordens_finalizadas.count()
        total_comissoes = sum(os.valor_comissao for os in ordens_finalizadas)
        lucro_liquido = faturamento_diario - Decimal(str(total_comissoes))

        # Desempenho por lavador no dia
        desempenho_lavadores = []
        for lavador in lavadores_todos:
            os_lavador = ordens_finalizadas.filter(lavador=lavador)
            qtd = os_lavador.count()
            comissao = sum(os.valor_comissao for os in os_lavador)
            desempenho_lavadores.append({
                'lavador': lavador,
                'quantidade': qtd,
                'comissao': comissao
            })

        # Formas de pagamento realizadas no dia
        formas_pgto = pagamentos_dia.values('forma_pagamento').annotate(
            total=Sum('valor_pago'),
            qtd=Count('id')
        ).order_by('-total')

        context.update({
            'data_selecionada': data_selecionada,
            'faturamento_diario': faturamento_diario,
            'total_lavagens': total_lavagens,
            'total_comissoes': total_comissoes,
            'lucro_liquido': lucro_liquido,
            'desempenho_lavadores': desempenho_lavadores,
            'formas_pgto': formas_pgto,
            'ordens_dia': ordens_dia,
        })

    # =========================================================================
    # CATEGORIA 2: RELATÓRIO MENSAL (Consolidado do Mês)
    # =========================================================================
    elif tipo_relatorio == 'mensal':
        ano_atual = hoje.year
        mes_atual = hoje.month

        try:
            mes_sel = int(request.GET.get('mes', mes_atual))
            ano_sel = int(request.GET.get('ano', ano_atual))
        except (ValueError, TypeError):
            mes_sel = mes_atual
            ano_sel = ano_atual

        ultimo_dia = calendar.monthrange(ano_sel, mes_sel)[1]
        inicio_mes = date(ano_sel, mes_sel, 1)
        fim_mes = date(ano_sel, mes_sel, ultimo_dia)

        ordens_mes = OrdemServico.objects.filter(
            data_hora__date__gte=inicio_mes, data_hora__date__lte=fim_mes
        ).select_related('veiculo', 'veiculo__cliente', 'servico', 'lavador', 'pagamento')

        pagamentos_mes = Pagamento.objects.filter(
            data_pagamento__date__gte=inicio_mes, data_pagamento__date__lte=fim_mes, status='CONCLUIDO'
        )

        faturamento_mensal = pagamentos_mes.aggregate(total=Sum('valor_pago'))['total'] or Decimal('0.00')
        ordens_finalizadas = ordens_mes.filter(status__in=['CONCLUIDO', 'ENTREGUE'])
        total_lavagens = ordens_finalizadas.count()
        total_comissoes = sum(os.valor_comissao for os in ordens_finalizadas)
        lucro_liquido = faturamento_mensal - Decimal(str(total_comissoes))
        ticket_medio = (faturamento_mensal / total_lavagens) if total_lavagens > 0 else Decimal('0.00')

        # Formas de pagamento no mês
        formas_pgto = pagamentos_mes.values('forma_pagamento').annotate(
            total=Sum('valor_pago'),
            qtd=Count('id')
        ).order_by('-total')

        # Desempenho acumulado dos lavadores no mês
        desempenho_lavadores = []
        for lavador in lavadores_todos:
            os_lav = ordens_finalizadas.filter(lavador=lavador)
            qtd = os_lav.count()
            comissao = sum(os.valor_comissao for os in os_lav)
            total_servicos = sum(os.valor_total or os.servico.valor for os in os_lav)
            desempenho_lavadores.append({
                'lavador': lavador,
                'quantidade': qtd,
                'total_servicos': total_servicos,
                'comissao': comissao
            })

        meses_nomes = [
            (1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'), (4, 'Abril'),
            (5, 'Maio'), (6, 'Junho'), (7, 'Julho'), (8, 'Agosto'),
            (9, 'Setembro'), (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro')
        ]
        anos_disponiveis = [ano_atual - 1, ano_atual, ano_atual + 1]

        context.update({
            'mes_sel': mes_sel,
            'ano_sel': ano_sel,
            'inicio_mes': inicio_mes,
            'fim_mes': fim_mes,
            'faturamento_mensal': faturamento_mensal,
            'total_lavagens': total_lavagens,
            'total_comissoes': total_comissoes,
            'lucro_liquido': lucro_liquido,
            'ticket_medio': ticket_medio,
            'formas_pgto': formas_pgto,
            'desempenho_lavadores': desempenho_lavadores,
            'ordens_mes': ordens_mes.order_by('-data_hora')[:30],
            'meses_nomes': meses_nomes,
            'anos_disponiveis': anos_disponiveis,
        })

    # =========================================================================
    # CATEGORIA 3: RELATÓRIO DE COMISSÕES POR LAVADOR
    # =========================================================================
    elif tipo_relatorio == 'comissoes':
        data_ini_param = request.GET.get('data_inicio')
        data_fim_param = request.GET.get('data_fim')
        lavador_id = request.GET.get('lavador_id')

        try:
            data_inicio = datetime.strptime(data_ini_param, '%Y-%m-%d').date() if data_ini_param else hoje.replace(day=1)
        except (ValueError, TypeError):
            data_inicio = hoje.replace(day=1)

        try:
            data_fim = datetime.strptime(data_fim_param, '%Y-%m-%d').date() if data_fim_param else hoje
        except (ValueError, TypeError):
            data_fim = hoje

        lavador_selecionado = None
        ordens_comissao = OrdemServico.objects.filter(
            data_hora__date__gte=data_inicio,
            data_hora__date__lte=data_fim,
            status__in=['CONCLUIDO', 'ENTREGUE']
        ).select_related('veiculo', 'servico', 'lavador').order_by('-data_hora')

        if lavador_id and lavador_id.isdigit():
            lavador_selecionado = Lavador.objects.filter(id=int(lavador_id)).first()
            if lavador_selecionado:
                ordens_comissao = ordens_comissao.filter(lavador=lavador_selecionado)

        total_comissoes_periodo = sum(os.valor_comissao for os in ordens_comissao)
        total_servicos_periodo = sum(os.valor_total or os.servico.valor for os in ordens_comissao)

        # Resumo por lavador
        resumo_lavadores = []
        lavadores_query = [lavador_selecionado] if lavador_selecionado else lavadores_todos
        for lavador in lavadores_query:
            os_lav = ordens_comissao.filter(lavador=lavador)
            qtd = os_lav.count()
            comissao = sum(os.valor_comissao for os in os_lav)
            faturamento_lavador = sum(os.valor_total or os.servico.valor for os in os_lav)
            resumo_lavadores.append({
                'lavador': lavador,
                'quantidade': qtd,
                'faturamento': faturamento_lavador,
                'comissao': comissao
            })

        context.update({
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'lavador_selecionado': lavador_selecionado,
            'lavador_id': lavador_id,
            'total_comissoes_periodo': total_comissoes_periodo,
            'total_servicos_periodo': total_servicos_periodo,
            'total_lavagens_periodo': ordens_comissao.count(),
            'resumo_lavadores': resumo_lavadores,
            'ordens_comissao': ordens_comissao,
        })

    # =========================================================================
    # CATEGORIA 4: RELATÓRIO DE FATURAMENTO / COBRANÇA DE EMPRESAS FATURADAS
    # =========================================================================
    elif tipo_relatorio == 'faturado':
        data_ini_param = request.GET.get('data_inicio')
        data_fim_param = request.GET.get('data_fim')
        cliente_id = request.GET.get('cliente_id')
        status_pgto = request.GET.get('status_pgto', 'TODOS')

        try:
            data_inicio = datetime.strptime(data_ini_param, '%Y-%m-%d').date() if data_ini_param else hoje.replace(day=1)
        except (ValueError, TypeError):
            data_inicio = hoje.replace(day=1)

        try:
            data_fim = datetime.strptime(data_fim_param, '%Y-%m-%d').date() if data_fim_param else hoje
        except (ValueError, TypeError):
            data_fim = hoje

        cliente_selecionado = None
        ordens_faturadas = OrdemServico.objects.filter(
            veiculo__cliente__tipo='FATURADO',
            data_hora__date__gte=data_inicio,
            data_hora__date__lte=data_fim
        ).select_related('veiculo', 'veiculo__cliente', 'servico', 'lavador', 'pagamento').order_by('data_hora')

        if cliente_id and cliente_id.isdigit():
            cliente_selecionado = Cliente.objects.filter(id=int(cliente_id), tipo='FATURADO').first()
            if cliente_selecionado:
                ordens_faturadas = ordens_faturadas.filter(veiculo__cliente=cliente_selecionado)

        if status_pgto == 'PENDENTE':
            ordens_faturadas = ordens_faturadas.filter(Q(pagamento__isnull=True) | Q(pagamento__status='PENDENTE'))
        elif status_pgto == 'CONCLUIDO':
            ordens_faturadas = ordens_faturadas.filter(pagamento__status='CONCLUIDO')

        total_faturamento = sum(os.valor_total or os.servico.valor for os in ordens_faturadas)
        total_pendente = sum(
            os.valor_total or os.servico.valor for os in ordens_faturadas
            if not hasattr(os, 'pagamento') or os.pagamento.status == 'PENDENTE'
        )
        total_pago = total_faturamento - total_pendente
        veiculos_unicos = ordens_faturadas.values('veiculo__placa').distinct().count()

        context.update({
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'cliente_selecionado': cliente_selecionado,
            'cliente_id': cliente_id,
            'status_pgto': status_pgto,
            'ordens_faturadas': ordens_faturadas,
            'total_faturamento': total_faturamento,
            'total_pendente': total_pendente,
            'total_pago': total_pago,
            'total_atendimentos': ordens_faturadas.count(),
            'veiculos_unicos': veiculos_unicos,
        })

    return render(request, 'lavajato/gerenciamento.html', context)


@login_required
@user_passes_test(is_admin, login_url='/recepcao/')
def imprimir_relatorio_view(request):
    """
    Renderiza layout formal pronto para impressão / exportação PDF (RF08, RN03).
    Destaque especial para o Demonstrativo de Cobrança / Fatura da Empresa Faturada.
    """
    hoje = timezone.localtime(timezone.now()).date()
    tipo = request.GET.get('tipo', 'faturado')

    # Dados padrão do estabelecimento para cabeçalho do documento de cobrança
    posto_dados = {
        'nome': 'Lava Jato do Valmir',
        'razao_social': 'Valmir Lava Jato & Serviços Automotivos EIRELI',
        'cnpj': '14.582.391/0001-44',
        'endereco': 'Av. Djalma Batista, 1020 - Chapada, Manaus - AM, 69050-010',
        'telefone': '(92) 99123-4567 / (92) 3644-8899',
        'chave_pix': 'financeiro@lavajatodovalmir.com.br',
        'banco': 'Banco Cora SCD / Agência: 0001 / Conta: 1827364-5',
    }

    context = {
        'hoje': hoje,
        'tipo': tipo,
        'posto_dados': posto_dados,
        'emissao_timestamp': timezone.localtime(timezone.now()),
    }

    # =========================================================================
    # IMPRESSÃO DE FATURA / COBRANÇA DA EMPRESA FATURADA
    # =========================================================================
    if tipo == 'faturado':
        data_ini_param = request.GET.get('data_inicio')
        data_fim_param = request.GET.get('data_fim')
        cliente_id = request.GET.get('cliente_id')
        status_pgto = request.GET.get('status_pgto', 'TODOS')

        try:
            data_inicio = datetime.strptime(data_ini_param, '%Y-%m-%d').date() if data_ini_param else hoje.replace(day=1)
        except (ValueError, TypeError):
            data_inicio = hoje.replace(day=1)

        try:
            data_fim = datetime.strptime(data_fim_param, '%Y-%m-%d').date() if data_fim_param else hoje
        except (ValueError, TypeError):
            data_fim = hoje

        cliente_selecionado = None
        ordens = OrdemServico.objects.filter(
            veiculo__cliente__tipo='FATURADO',
            data_hora__date__gte=data_inicio,
            data_hora__date__lte=data_fim
        ).select_related('veiculo', 'veiculo__cliente', 'servico', 'lavador', 'pagamento').order_by('data_hora')

        if cliente_id and cliente_id.isdigit():
            cliente_selecionado = Cliente.objects.filter(id=int(cliente_id), tipo='FATURADO').first()
            if cliente_selecionado:
                ordens = ordens.filter(veiculo__cliente=cliente_selecionado)

        if status_pgto == 'PENDENTE':
            ordens = ordens.filter(Q(pagamento__isnull=True) | Q(pagamento__status='PENDENTE'))
        elif status_pgto == 'CONCLUIDO':
            ordens = ordens.filter(pagamento__status='CONCLUIDO')

        total_faturar = sum(os.valor_total or os.servico.valor for os in ordens)
        total_pendente = sum(
            os.valor_total or os.servico.valor for os in ordens
            if not hasattr(os, 'pagamento') or os.pagamento.status == 'PENDENTE'
        )

        context.update({
            'titulo_documento': 'DEMONSTRATIVO DE SERVIÇOS PARA FATURAMENTO CORPORATIVO',
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'cliente': cliente_selecionado,
            'ordens': ordens,
            'total_faturar': total_faturar,
            'total_pendente': total_pendente,
            'total_atendimentos': ordens.count(),
            'veiculos_unicos': ordens.values('veiculo__placa').distinct().count(),
        })

    # =========================================================================
    # IMPRESSÃO DE FECHAMENTO DIÁRIO
    # =========================================================================
    elif tipo == 'diario':
        data_param = request.GET.get('data')
        try:
            data_sel = datetime.strptime(data_param, '%Y-%m-%d').date() if data_param else hoje
        except (ValueError, TypeError):
            data_sel = hoje

        ordens_dia = OrdemServico.objects.filter(data_hora__date=data_sel).select_related(
            'veiculo', 'veiculo__cliente', 'servico', 'lavador', 'pagamento'
        ).order_by('data_hora')

        pagamentos_dia = Pagamento.objects.filter(data_pagamento__date=data_sel, status='CONCLUIDO')
        faturamento_diario = pagamentos_dia.aggregate(total=Sum('valor_pago'))['total'] or Decimal('0.00')
        ordens_finalizadas = ordens_dia.filter(status__in=['CONCLUIDO', 'ENTREGUE'])
        total_comissoes = sum(os.valor_comissao for os in ordens_finalizadas)
        lucro_liquido = faturamento_diario - Decimal(str(total_comissoes))

        context.update({
            'titulo_documento': f'RELATÓRIO DE FECHAMENTO DE CAIXA DIÁRIO - {data_sel.strftime("%d/%m/%Y")}',
            'data_sel': data_sel,
            'ordens': ordens_dia,
            'faturamento': faturamento_diario,
            'total_comissoes': total_comissoes,
            'lucro_liquido': lucro_liquido,
            'total_atendimentos': ordens_dia.count(),
        })

    # =========================================================================
    # IMPRESSÃO DE EXTRATO DE COMISSÕES
    # =========================================================================
    elif tipo == 'comissoes':
        data_ini_param = request.GET.get('data_inicio')
        data_fim_param = request.GET.get('data_fim')
        lavador_id = request.GET.get('lavador_id')

        try:
            data_inicio = datetime.strptime(data_ini_param, '%Y-%m-%d').date() if data_ini_param else hoje.replace(day=1)
        except (ValueError, TypeError):
            data_inicio = hoje.replace(day=1)

        try:
            data_fim = datetime.strptime(data_fim_param, '%Y-%m-%d').date() if data_fim_param else hoje
        except (ValueError, TypeError):
            data_fim = hoje

        lavador = None
        ordens = OrdemServico.objects.filter(
            data_hora__date__gte=data_inicio,
            data_hora__date__lte=data_fim,
            status__in=['CONCLUIDO', 'ENTREGUE']
        ).select_related('veiculo', 'servico', 'lavador').order_by('lavador__nome', 'data_hora')

        if lavador_id and lavador_id.isdigit():
            lavador = Lavador.objects.filter(id=int(lavador_id)).first()
            if lavador:
                ordens = ordens.filter(lavador=lavador)

        total_comissoes = sum(os.valor_comissao for os in ordens)
        total_servicos = sum(os.valor_total or os.servico.valor for os in ordens)

        context.update({
            'titulo_documento': 'EXTRATO DE REPASSE DE COMISSÕES DE LAVADORES',
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'lavador': lavador,
            'ordens': ordens,
            'total_comissoes': total_comissoes,
            'total_servicos': total_servicos,
            'total_atendimentos': ordens.count(),
        })

    return render(request, 'lavajato/relatorio_impressao.html', context)


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

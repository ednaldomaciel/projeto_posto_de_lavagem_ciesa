from decimal import Decimal
from datetime import timedelta
from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.urls import reverse
from lavajato.models import EmpresaFaturada, Cliente, Veiculo, Lavador, Servico, OrdemServico, Pagamento
from lavajato.forms import ClienteCadastroForm


class RegrasDeNegocioTestCase(TestCase):
    def setUp(self):
        # Usuário Operador
        self.user = User.objects.create_user(username='operador', password='password123')

        # Clientes: 1 Avulso e 1 Faturado
        self.cliente_avulso = Cliente.objects.create(
            nome='Carlos Avulso',
            tipo='AVULSO',
            telefone='92999990001'
        )
        self.cliente_faturado = Cliente.objects.create(
            nome='Empresa ABC Frotas',
            tipo='FATURADO',
            empresa_faturada=EmpresaFaturada.objects.create(nome='Empresa ABC Frotas'),
            telefone='9233334444'
        )

        # Veículos
        self.veiculo_avulso = Veiculo.objects.create(
            cliente=self.cliente_avulso,
            placa='AVU1234',
            modelo='Gol',
            marca='VW'
        )
        self.veiculo_faturado = Veiculo.objects.create(
            cliente=self.cliente_faturado,
            placa='FAT5678',
            modelo='Strada',
            marca='Fiat'
        )

        # Lavador com 10% de comissão (RF03)
        self.lavador = Lavador.objects.create(
            nome='Sebastião da Silva',
            percentual_comissao=Decimal('10.00'),
            ativo=True
        )

        # Serviços (RF04)
        self.servico_simples = Servico.objects.create(
            descricao='Lavagem Simples',
            valor=Decimal('50.00'),
            tempo_estimado_minutos=30
        )
        self.servico_completo = Servico.objects.create(
            descricao='Lavagem Completa',
            valor=Decimal('100.00'),
            tempo_estimado_minutos=60
        )

    def test_recepcao_cadastra_cliente_faturado_e_veiculo(self):
        empresa = EmpresaFaturada.objects.create(
            nome='Transportadora Teste',
            documento='11.222.333/0001-44',
        )
        client = Client()
        client.force_login(self.user)

        resposta_cliente = client.post(reverse('recepcao'), {
            'acao': 'cadastrar_cliente',
            'nome': 'Motorista Joao',
            'tipo': 'FATURADO',
            'empresa_faturada': empresa.id,
            'telefone': '(92) 99999-0000',
            'documento': '123.456.789-00',
            'observacoes': 'Cadastro pela recepção',
        })
        self.assertEqual(resposta_cliente.status_code, 302)

        cliente = Cliente.objects.get(nome='Motorista Joao')
        self.assertEqual(cliente.empresa_faturada, empresa)

        resposta_veiculo = client.post(reverse('recepcao'), {
            'acao': 'cadastrar_veiculo',
            'cliente': cliente.id,
            'placa': 'rece101',
            'modelo': 'Corolla',
            'cor': 'Prata',
            'tipo_veiculo': 'Médio',
        })
        self.assertEqual(resposta_veiculo.status_code, 302)

        veiculo = Veiculo.objects.get(placa='RECE101')
        self.assertEqual(veiculo.cliente, cliente)
        self.assertEqual(veiculo.marca, '')

    def test_busca_por_placa_exige_confirmacao_antes_da_os(self):
        client = Client()
        client.force_login(self.user)

        resposta = client.get(reverse('recepcao'), {'placa': 'avu1234'})

        self.assertContains(resposta, 'Selecionar veículo e continuar')
        self.assertNotContains(resposta, 'Emitir Ordem de Serviço')

        resposta_selecao = client.get(
            reverse('recepcao'),
            {'placa': 'AVU1234', 'selecionar': '1'},
        )
        self.assertContains(resposta_selecao, 'Emitir Ordem de Serviço')
        self.assertContains(resposta_selecao, 'Marcar como pago agora')

    def test_cliente_faturado_nao_paga_na_lavagem_mesmo_com_post_manipulado(self):
        client = Client()
        client.force_login(self.user)
        url = f"{reverse('recepcao')}?placa={self.veiculo_faturado.placa}&selecionar=1"

        resposta = client.get(url)
        self.assertContains(resposta, self.cliente_faturado.empresa_faturada.nome)
        self.assertNotContains(resposta, 'Marcar como pago agora')

        resposta = client.post(url, {
            'veiculo': self.veiculo_faturado.id,
            'servico': self.servico_simples.id,
            'lavador': self.lavador.id,
            'observacoes_veiculo': '',
            'pagamento_agora': 'on',
            'forma_pagamento': 'PIX',
        })

        self.assertEqual(resposta.status_code, 302)
        pagamento = OrdemServico.objects.latest('id').pagamento
        self.assertEqual(pagamento.forma_pagamento, 'FATURADO')
        self.assertEqual(pagamento.status, 'PENDENTE')

    def test_os_pode_ser_registrada_com_pagamento_pendente_ou_pago(self):
        client = Client()
        client.force_login(self.user)
        url = f"{reverse('recepcao')}?placa={self.veiculo_avulso.placa}&selecionar=1"
        dados_os = {
            'veiculo': self.veiculo_avulso.id,
            'servico': self.servico_simples.id,
            'lavador': self.lavador.id,
            'observacoes_veiculo': '',
        }

        resposta_pendente = client.post(url, dados_os)
        self.assertEqual(resposta_pendente.status_code, 302)
        os_pendente = OrdemServico.objects.latest('id')
        self.assertEqual(os_pendente.pagamento.status, 'PENDENTE')
        self.assertEqual(os_pendente.pagamento.forma_pagamento, 'PENDENTE')

        dados_pago = {
            **dados_os,
            'pagamento_agora': 'on',
            'forma_pagamento': 'PIX',
        }
        resposta_pago = client.post(url, dados_pago)
        self.assertEqual(resposta_pago.status_code, 302)
        os_pago = OrdemServico.objects.latest('id')
        self.assertEqual(os_pago.pagamento.status, 'CONCLUIDO')
        self.assertEqual(os_pago.pagamento.forma_pagamento, 'PIX')

    def test_cliente_faturado_exige_empresa_faturada(self):
        form = ClienteCadastroForm(data={
            'nome': 'Cliente conveniado',
            'tipo': 'FATURADO',
            'empresa_faturada': '',
            'telefone': '',
            'documento': '',
            'observacoes': '',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('empresa_faturada', form.errors)

    def test_busca_sem_placa_cadastrada_lista_apenas_empresas_ativas(self):
        empresa_ativa = EmpresaFaturada.objects.create(nome='Frota Ativa')
        EmpresaFaturada.objects.create(nome='Frota Inativa', ativo=False)
        client = Client()
        client.force_login(self.user)

        resposta = client.get(reverse('recepcao'), {'placa': 'NOV1234'})

        self.assertContains(resposta, '1. Tipo de cliente')
        self.assertContains(resposta, empresa_ativa.nome)
        self.assertNotContains(resposta, 'Frota Inativa')

    def test_rn01_bloqueio_segunda_lavagem_veiculo_faturado_na_mesma_semana(self):
        """
        RN01: Veículos de clientes faturados possuem limite estrito de
        no máximo 1 lavagem por semana, com bloqueio automático no sistema.
        """
        # Primeira lavagem na semana: deve ser permitida
        os1 = OrdemServico.objects.create(
            veiculo=self.veiculo_faturado,
            servico=self.servico_simples,
            lavador=self.lavador,
            usuario=self.user,
            status='FILA'
        )
        self.assertIsNotNone(os1.id)

        # Tentativa de segunda lavagem na mesma semana: deve levantar ValidationError
        os_duplicada = OrdemServico(
            veiculo=self.veiculo_faturado,
            servico=self.servico_completo,
            lavador=self.lavador,
            usuario=self.user,
            status='FILA'
        )
        with self.assertRaises(ValidationError) as context:
            os_duplicada.save()

        self.assertIn('RN01', str(context.exception))

    def test_cliente_avulso_pode_lavar_multiplas_vezes_na_semana(self):
        """Clientes avulsos não possuem trava de limite semanal."""
        os1 = OrdemServico.objects.create(
            veiculo=self.veiculo_avulso,
            servico=self.servico_simples,
            lavador=self.lavador,
            usuario=self.user,
            status='FILA'
        )
        os2 = OrdemServico.objects.create(
            veiculo=self.veiculo_avulso,
            servico=self.servico_completo,
            lavador=self.lavador,
            usuario=self.user,
            status='FILA'
        )
        self.assertIsNotNone(os1.id)
        self.assertIsNotNone(os2.id)

    def test_patio_registra_entrega_ao_cliente_em_coluna_separada(self):
        os = OrdemServico.objects.create(
            veiculo=self.veiculo_avulso,
            servico=self.servico_simples,
            lavador=self.lavador,
            usuario=self.user,
            status='CONCLUIDO',
        )
        client = Client()
        client.force_login(self.user)

        resposta = client.get(reverse('patio'))
        self.assertContains(resposta, 'Entregues ao cliente')
        self.assertContains(resposta, 'Registrar entrega ao cliente')

        resposta = client.post(reverse('patio'), {
            'os_id': os.id,
            'novo_status': 'ENTREGUE',
        })

        self.assertEqual(resposta.status_code, 302)
        os.refresh_from_db()
        self.assertEqual(os.status, 'ENTREGUE')
        self.assertIsNotNone(os.data_hora_saida)

        resposta = client.get(reverse('patio'))
        self.assertContains(resposta, self.veiculo_avulso.placa)
        self.assertContains(resposta, 'Entregue ao cliente')

    def test_rf03_calculo_comissao_lavador(self):
        """RF03: A comissão do lavador deve ser calculada baseada na taxa configurada."""
        os = OrdemServico.objects.create(
            veiculo=self.veiculo_avulso,
            servico=self.servico_completo,
            lavador=self.lavador,
            usuario=self.user,
            status='CONCLUIDO'
        )
        self.assertEqual(os.valor_comissao, Decimal('10.00'))

    def test_rn02_flexibilidade_pagamento_entrada_e_retirada(self):
        """RN02: Pagamento pode ser efetuado na entrada ou na retirada do veículo."""
        os = OrdemServico.objects.create(
            veiculo=self.veiculo_avulso,
            servico=self.servico_simples,
            lavador=self.lavador,
            usuario=self.user
        )

        pagamento = Pagamento.objects.create(
            ordem_servico=os,
            forma_pagamento='PIX',
            momento_pagamento='ENTRADA',
            status='CONCLUIDO',
            valor_pago=os.valor_total
        )
        self.assertEqual(pagamento.momento_pagamento, 'ENTRADA')
        self.assertEqual(pagamento.valor_pago, Decimal('50.00'))


class RelatoriosGestaoTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Grupos e Usuários
        grp_admin, _ = Group.objects.get_or_create(name='Administrador')
        grp_recepcao, _ = Group.objects.get_or_create(name='Recepcionista')

        self.admin_user = User.objects.create_superuser(username='admin_test', password='adm_password', email='adm@test.com')
        self.admin_user.groups.add(grp_admin)

        self.recepcao_user = User.objects.create_user(username='recep_test', password='rec_password')
        self.recepcao_user.groups.add(grp_recepcao)

        # Clientes
        self.empresa_faturada = EmpresaFaturada.objects.create(nome='Empresa Parceira de Frotas LTDA')
        self.cliente_corp = Cliente.objects.create(
            nome='Empresa Parceira de Frotas LTDA',
            tipo='FATURADO',
            empresa_faturada=self.empresa_faturada,
            documento='11.222.333/0001-44',
            telefone='(92) 3300-1122'
        )
        self.cliente_avulso = Cliente.objects.create(
            nome='João da Silva',
            tipo='AVULSO',
            telefone='(92) 99100-2233'
        )

        # Veículos
        self.veiculo_corp1 = Veiculo.objects.create(cliente=self.cliente_corp, placa='CORP001', modelo='Hilux', marca='Toyota')
        self.veiculo_corp2 = Veiculo.objects.create(cliente=self.cliente_corp, placa='CORP002', modelo='Strada', marca='Fiat')
        self.veiculo_avulso = Veiculo.objects.create(cliente=self.cliente_avulso, placa='AVU9999', modelo='Civic', marca='Honda')

        # Lavador
        self.lavador = Lavador.objects.create(nome='Marcos Lavador', percentual_comissao=Decimal('10.00'), ativo=True)

        # Serviços
        self.servico_geral = Servico.objects.create(descricao='Lavagem Geral', valor=Decimal('80.00'), tempo_estimado_minutos=45)
        self.servico_cera = Servico.objects.create(descricao='Geral com Cera', valor=Decimal('120.00'), tempo_estimado_minutos=60)

        # Data base: hoje
        self.hoje = timezone.localtime(timezone.now()).date()

        # Cria OS corporativa faturada 1 (Pendente de pagamento)
        self.os_faturada1 = OrdemServico.objects.create(
            veiculo=self.veiculo_corp1,
            servico=self.servico_geral,
            lavador=self.lavador,
            usuario=self.admin_user,
            status='ENTREGUE',
            valor_total=Decimal('80.00'),
            data_hora=timezone.localtime(timezone.now()) - timedelta(days=2)
        )
        Pagamento.objects.create(
            ordem_servico=self.os_faturada1,
            forma_pagamento='FATURADO',
            momento_pagamento='RETIRADA',
            status='PENDENTE',
            valor_pago=Decimal('80.00')
        )

        cliente_frota_adicional = Cliente.objects.create(
            nome='Motorista da frota',
            tipo='FATURADO',
            empresa_faturada=self.empresa_faturada,
        )
        veiculo_frota_adicional = Veiculo.objects.create(
            cliente=cliente_frota_adicional,
            placa='CORP003',
            modelo='Onix',
        )
        self.os_faturada_adicional = OrdemServico.objects.create(
            veiculo=veiculo_frota_adicional,
            servico=self.servico_geral,
            lavador=self.lavador,
            usuario=self.admin_user,
            status='ENTREGUE',
            valor_total=Decimal('50.00'),
            data_hora=timezone.localtime(timezone.now()) - timedelta(days=1)
        )

        # Cria OS corporativa faturada 2 (Pendente)
        self.os_faturada2 = OrdemServico.objects.create(
            veiculo=self.veiculo_corp2,
            servico=self.servico_cera,
            lavador=self.lavador,
            usuario=self.admin_user,
            status='ENTREGUE',
            valor_total=Decimal('120.00'),
            data_hora=timezone.localtime(timezone.now()) - timedelta(days=1)
        )

    def test_relatorio_faturado_por_empresa_e_periodo(self):
        """RF08 / RN01: O relatório faturado deve totalizar corretamente os atendimentos da empresa no período."""
        self.client.force_login(self.admin_user)

        data_ini = (self.hoje - timedelta(days=7)).strftime('%Y-%m-%d')
        data_fim = self.hoje.strftime('%Y-%m-%d')

        url = f"{reverse('gerenciamento')}?tipo=faturado&empresa_id={self.empresa_faturada.id}&data_inicio={data_ini}&data_fim={data_fim}"
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context['tipo_relatorio'], 'faturado')
        self.assertEqual(res.context['empresa_selecionada'], self.empresa_faturada)
        self.assertEqual(res.context['total_atendimentos'], 3)
        self.assertEqual(res.context['total_faturamento'], Decimal('250.00'))
        self.assertEqual(res.context['total_pendente'], Decimal('250.00'))

    def test_impressao_fatura_empresa_faturada(self):
        """RF08: A tela de impressão pronta para cobrança deve renderizar dados do conveniado e valor a pagar."""
        self.client.force_login(self.admin_user)

        data_ini = (self.hoje - timedelta(days=7)).strftime('%Y-%m-%d')
        data_fim = self.hoje.strftime('%Y-%m-%d')

        url = f"{reverse('imprimir_relatorio')}?tipo=faturado&empresa_id={self.empresa_faturada.id}&data_inicio={data_ini}&data_fim={data_fim}"
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'DEMONSTRATIVO DE SERVIÇOS PARA FATURAMENTO CORPORATIVO')
        self.assertContains(res, self.empresa_faturada.nome)
        self.assertContains(res, 'CORP001')
        self.assertContains(res, 'CORP002')
        self.assertContains(res, 'CORP003')
        self.assertContains(res, '250,00')

    def test_relatorio_fechamento_diario(self):
        """RF08 / RN03: Relatório diário deve retornar status 200 e contexto do dia."""
        self.client.force_login(self.admin_user)
        url = f"{reverse('gerenciamento')}?tipo=diario&data={self.hoje.strftime('%Y-%m-%d')}"
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertIn('faturamento_diario', res.context)

    def test_relatorio_consolidado_mensal(self):
        """RF08 / RN03: Relatório mensal deve retornar status 200 com métricas agregadas."""
        self.client.force_login(self.admin_user)
        url = f"{reverse('gerenciamento')}?tipo=mensal&mes={self.hoje.month}&ano={self.hoje.year}"
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertIn('faturamento_mensal', res.context)
        self.assertIn('ticket_medio', res.context)

    def test_relatorio_comissoes_lavador(self):
        """RF03 / RF08: Relatório de comissões deve listar valores devidos por lavador."""
        self.client.force_login(self.admin_user)
        url = f"{reverse('gerenciamento')}?tipo=comissoes&lavador_id={self.lavador.id}"
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertIn('total_comissoes_periodo', res.context)

    def test_rn03_bloqueio_usuario_nao_administrador_em_gerenciamento_e_impressao(self):
        """RN03: Operador de recepção não possui acesso a telas financeiras e é redirecionado."""
        self.client.force_login(self.recepcao_user)

        res_gerencia = self.client.get(reverse('gerenciamento'))
        self.assertEqual(res_gerencia.status_code, 302)
        self.assertIn('/recepcao/', res_gerencia.url)

        res_imprime = self.client.get(reverse('imprimir_relatorio'))
        self.assertEqual(res_imprime.status_code, 302)
        self.assertIn('/recepcao/', res_imprime.url)

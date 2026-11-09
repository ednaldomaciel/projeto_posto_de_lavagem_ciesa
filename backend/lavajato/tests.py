from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from lavajato.models import Cliente, Veiculo, Lavador, Servico, OrdemServico, Pagamento


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

    def test_rf03_calculo_comissao_lavador(self):
        """RF03: A comissão do lavador deve ser calculada baseada na taxa configurada."""
        # Serviço de R$ 100 com lavador a 10% comissão = R$ 10.00
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

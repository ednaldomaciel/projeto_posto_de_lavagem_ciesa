import calendar
from decimal import Decimal
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.utils import timezone
from lavajato.models import EmpresaFaturada, Cliente, Veiculo, Lavador, Servico, OrdemServico, Pagamento


class Command(BaseCommand):
    help = 'Popula o banco de dados com dados iniciais completos de demonstração (Lava Jato do Valmir)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Iniciando carga de dados no banco...'))

        # 1. Perfis e Usuários (RF01, RNF05)
        grp_admin, _ = Group.objects.get_or_create(name='Administrador')
        grp_recepcao, _ = Group.objects.get_or_create(name='Recepcionista')

        # Superusuário / Admin
        admin_user, created_admin = User.objects.get_or_create(
            username='admin',
            defaults={
                'first_name': 'Seu',
                'last_name': 'Valmir (Admin)',
                'email': 'admin@postolavagem.com',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created_admin:
            admin_user.set_password('admin123')
            admin_user.save()
            admin_user.groups.add(grp_admin)
            self.stdout.write(self.style.SUCCESS('Admin criado: usuario="admin" / senha="admin123"'))

        # Operador de Recepção
        recep_user, created_rec = User.objects.get_or_create(
            username='juliana',
            defaults={
                'first_name': 'Juliana',
                'last_name': 'Recepção',
                'email': 'juliana@postolavagem.com',
                'is_staff': True,
                'is_superuser': False,
            }
        )
        if created_rec:
            recep_user.set_password('recepcao123')
            recep_user.save()
            recep_user.groups.add(grp_recepcao)
            self.stdout.write(self.style.SUCCESS('Recepcionista criada: usuario="juliana" / senha="recepcao123"'))

        # 2. Clientes (RF02)
        empresa_frota_segura, _ = EmpresaFaturada.objects.get_or_create(
            nome='Empresa Frota Segura LTDA',
            defaults={
                'documento': '12.345.678/0001-99',
                'telefone': '(92) 3622-4455',
                'observacoes': 'Convênio corporativo semanal / Faturamento quinzenal',
            },
        )
        empresa_transportes, _ = EmpresaFaturada.objects.get_or_create(
            nome='Transportes & Logística AM',
            defaults={
                'documento': '98.765.432/0001-11',
                'telefone': '(92) 3234-8899',
                'observacoes': 'Frota corporativa faturada mensalmente',
            },
        )

        c1, _ = Cliente.objects.get_or_create(
            nome='Marcos Antônio Oliveira',
            defaults={'tipo': 'AVULSO', 'telefone': '(92) 99111-2233', 'documento': '123.456.789-00', 'observacoes': 'Cliente preferencial matutino'}
        )
        c2, _ = Cliente.objects.get_or_create(
            nome='Empresa Frota Segura LTDA',
            defaults={'tipo': 'FATURADO', 'empresa_faturada': empresa_frota_segura, 'telefone': '(92) 3622-4455', 'documento': '12.345.678/0001-99', 'observacoes': 'Convênio corporativo semanal / Faturamento quinzenal'}
        )
        c3, _ = Cliente.objects.get_or_create(
            nome='Ana Beatriz Souza',
            defaults={'tipo': 'AVULSO', 'telefone': '(92) 98444-5566', 'documento': '987.654.321-11'}
        )
        c4, _ = Cliente.objects.get_or_create(
            nome='Transportes & Logística AM',
            defaults={'tipo': 'FATURADO', 'empresa_faturada': empresa_transportes, 'telefone': '(92) 3234-8899', 'documento': '98.765.432/0001-11', 'observacoes': 'Frota corporativa faturada mensalmente'}
        )

        # 3. Veículos (RF02)
        v1, _ = Veiculo.objects.get_or_create(placa='ABC1D23', defaults={'cliente': c1, 'modelo': 'Corolla', 'marca': 'Toyota', 'cor': 'Prata', 'tipo_veiculo': 'Médio'})
        v2, _ = Veiculo.objects.get_or_create(placa='XYZ9876', defaults={'cliente': c2, 'modelo': 'Hilux', 'marca': 'Toyota', 'cor': 'Branca', 'tipo_veiculo': 'Caminhonete'})
        v3, _ = Veiculo.objects.get_or_create(placa='KGB4421', defaults={'cliente': c2, 'modelo': 'Compass', 'marca': 'Jeep', 'cor': 'Preto', 'tipo_veiculo': 'SUV'})
        v4, _ = Veiculo.objects.get_or_create(placa='MNO5566', defaults={'cliente': c3, 'modelo': 'Onix', 'marca': 'Chevrolet', 'cor': 'Vermelho', 'tipo_veiculo': 'Pequeno'})
        v5, _ = Veiculo.objects.get_or_create(placa='JKL3322', defaults={'cliente': c4, 'modelo': 'Civic', 'marca': 'Honda', 'cor': 'Cinza', 'tipo_veiculo': 'Médio'})

        # 4. Lavadores (RF03)
        l1, _ = Lavador.objects.get_or_create(nome='Carlos Silva', defaults={'telefone': '(92) 98100-1122', 'percentual_comissao': Decimal('10.00'), 'ativo': True})
        l2, _ = Lavador.objects.get_or_create(nome='João Pedro Santos', defaults={'telefone': '(92) 98200-2233', 'percentual_comissao': Decimal('10.00'), 'ativo': True})
        l3, _ = Lavador.objects.get_or_create(nome='Marcos de Souza', defaults={'telefone': '(92) 98300-3344', 'percentual_comissao': Decimal('12.00'), 'ativo': True})

        # 5. Serviços (RF04)
        s1, _ = Servico.objects.get_or_create(descricao='Ducha Externa', defaults={'valor': Decimal('30.00'), 'tempo_estimado_minutos': 20, 'ativo': True})
        s2, _ = Servico.objects.get_or_create(descricao='Lavagem Simples', defaults={'valor': Decimal('45.00'), 'tempo_estimado_minutos': 35, 'ativo': True})
        s3, _ = Servico.objects.get_or_create(descricao='Lavagem Completa', defaults={'valor': Decimal('70.00'), 'tempo_estimado_minutos': 50, 'ativo': True})
        s4, _ = Servico.objects.get_or_create(descricao='Aplicação de Cera', defaults={'valor': Decimal('30.00'), 'tempo_estimado_minutos': 20, 'ativo': True})
        s5, _ = Servico.objects.get_or_create(descricao='Higienização Interna', defaults={'valor': Decimal('150.00'), 'tempo_estimado_minutos': 120, 'ativo': True})

        # 6. Ordens de Serviço e Histórico para Demonstração de Relatórios
        # Limpa ordens existentes para re-popular dados consistentes se necessário
        if OrdemServico.objects.count() < 5:
            OrdemServico.objects.all().delete()
            agora = timezone.localtime(timezone.now())

            # --- Ordens de hoje ---
            # OS 1: Em Fila (Avulso)
            os1 = OrdemServico.objects.create(
                veiculo=v4,
                servico=s2,
                lavador=l3,
                usuario=recep_user,
                status='FILA',
                valor_total=s2.valor,
                observacoes_veiculo='Sem avarias observadas',
                data_hora=agora - timedelta(minutes=45)
            )

            # OS 2: Em Lavagem (Faturado - Frota Segura)
            os2 = OrdemServico.objects.create(
                veiculo=v3,
                servico=s3,
                lavador=l2,
                usuario=recep_user,
                status='LAVAGEM',
                valor_total=s3.valor,
                observacoes_veiculo='Veículo com lama na caixa de roda',
                data_hora=agora - timedelta(minutes=30)
            )
            Pagamento.objects.create(
                ordem_servico=os2,
                forma_pagamento='FATURADO',
                momento_pagamento='RETIRADA',
                status='PENDENTE',
                valor_pago=s3.valor,
                data_pagamento=agora - timedelta(minutes=30)
            )

            # OS 3: Concluída e Paga hoje (Avulso - PIX)
            os3 = OrdemServico.objects.create(
                veiculo=v1,
                servico=s3,
                lavador=l1,
                usuario=recep_user,
                status='CONCLUIDO',
                valor_total=s3.valor,
                observacoes_veiculo='Pequeno risco no para-lama dianteiro esquerdo',
                data_hora=agora - timedelta(hours=2),
                data_hora_saida=agora - timedelta(hours=1)
            )
            Pagamento.objects.create(
                ordem_servico=os3,
                forma_pagamento='PIX',
                momento_pagamento='ENTRADA',
                status='CONCLUIDO',
                valor_pago=s3.valor,
                data_pagamento=agora - timedelta(hours=2)
            )

            # --- Histórico dos dias anteriores para relatórios mensais e de faturamento corporativo ---
            # OS 4: Frota Segura semana passada (Concluída - Faturado Pendente)
            data_os4 = agora - timedelta(days=8)
            os4 = OrdemServico.objects.create(
                veiculo=v2,
                servico=s3,
                lavador=l2,
                usuario=recep_user,
                status='ENTREGUE',
                valor_total=s3.valor,
                observacoes_veiculo='Higienização de caçamba solicitada',
                data_hora=data_os4,
                data_hora_saida=data_os4 + timedelta(minutes=55)
            )
            Pagamento.objects.create(
                ordem_servico=os4,
                forma_pagamento='FATURADO',
                momento_pagamento='RETIRADA',
                status='PENDENTE',
                valor_pago=s3.valor,
                data_pagamento=data_os4
            )

            # OS 5: Frota Segura há 15 dias (Concluída - Faturado)
            data_os5 = agora - timedelta(days=15)
            os5 = OrdemServico.objects.create(
                veiculo=v3,
                servico=s2,
                lavador=l1,
                usuario=recep_user,
                status='ENTREGUE',
                valor_total=s2.valor,
                observacoes_veiculo='Lavagem de rotina de frota',
                data_hora=data_os5,
                data_hora_saida=data_os5 + timedelta(minutes=40)
            )
            Pagamento.objects.create(
                ordem_servico=os5,
                forma_pagamento='FATURADO',
                momento_pagamento='RETIRADA',
                status='PENDENTE',
                valor_pago=s2.valor,
                data_pagamento=data_os5
            )

            # OS 6: Transportes & Logística AM há 4 dias (Concluída - Faturado)
            data_os6 = agora - timedelta(days=4)
            os6 = OrdemServico.objects.create(
                veiculo=v5,
                servico=s5,
                lavador=l3,
                usuario=recep_user,
                status='ENTREGUE',
                valor_total=s5.valor,
                observacoes_veiculo='Higienização interna completa de frota',
                data_hora=data_os6,
                data_hora_saida=data_os6 + timedelta(hours=2)
            )
            Pagamento.objects.create(
                ordem_servico=os6,
                forma_pagamento='FATURADO',
                momento_pagamento='RETIRADA',
                status='PENDENTE',
                valor_pago=s5.valor,
                data_pagamento=data_os6
            )

            # OS 7: Avulso pago em Dinheiro há 3 dias
            data_os7 = agora - timedelta(days=3)
            os7 = OrdemServico.objects.create(
                veiculo=v4,
                servico=s2,
                lavador=l2,
                usuario=recep_user,
                status='ENTREGUE',
                valor_total=s2.valor,
                observacoes_veiculo='Lavagem rápida',
                data_hora=data_os7,
                data_hora_saida=data_os7 + timedelta(minutes=35)
            )
            Pagamento.objects.create(
                ordem_servico=os7,
                forma_pagamento='DINHEIRO',
                momento_pagamento='ENTRADA',
                status='CONCLUIDO',
                valor_pago=s2.valor,
                data_pagamento=data_os7
            )

            # OS 8: Avulso pago em Cartão há 5 dias
            data_os8 = agora - timedelta(days=5)
            os8 = OrdemServico.objects.create(
                veiculo=v1,
                servico=s3,
                lavador=l1,
                usuario=recep_user,
                status='ENTREGUE',
                valor_total=s3.valor,
                data_hora=data_os8,
                data_hora_saida=data_os8 + timedelta(minutes=50)
            )
            Pagamento.objects.create(
                ordem_servico=os8,
                forma_pagamento='CARTAO',
                momento_pagamento='RETIRADA',
                status='CONCLUIDO',
                valor_pago=s3.valor,
                data_pagamento=data_os8
            )

        self.stdout.write(self.style.SUCCESS('Banco de dados populado com sucesso com histórico completo!'))

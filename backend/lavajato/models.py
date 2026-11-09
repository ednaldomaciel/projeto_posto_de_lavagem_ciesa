from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta


# 1. Tabela: Clientes (Avulso vs Faturado / Conveniado - RF02)
class Cliente(models.Model):
    TIPO_CHOICES = [
        ('AVULSO', 'Avulso (Pessoa Física)'),
        ('FATURADO', 'Faturado / Convênio Corporativo'),
    ]

    nome = models.CharField('Nome do Cliente / Razão Social', max_length=120)
    tipo = models.CharField('Tipo de Cliente', max_length=20, choices=TIPO_CHOICES, default='AVULSO')
    telefone = models.CharField('Telefone / WhatsApp', max_length=20, blank=True, null=True)
    documento = models.CharField('CPF / CNPJ', max_length=25, blank=True, null=True)
    observacoes = models.TextField('Observações', blank=True, null=True)
    ativo = models.BooleanField('Ativo', default=True)
    data_cadastro = models.DateTimeField('Data de Cadastro', auto_now_add=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"


# 2. Tabela: Veículos (RF02)
class Veiculo(models.Model):
    TIPO_VEICULO_CHOICES = [
        ('Pequeno', 'Pequeno / Hatch'),
        ('Médio', 'Médio / Sedan'),
        ('SUV', 'SUV'),
        ('Caminhonete', 'Caminhonete / Picape'),
        ('Van', 'Van / Utilitário'),
        ('Outro', 'Outro'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='veiculos', verbose_name='Cliente Proprietário')
    placa = models.CharField('Placa', max_length=10, unique=True)
    modelo = models.CharField('Modelo', max_length=50)
    marca = models.CharField('Marca / Fabricante', max_length=50)
    cor = models.CharField('Cor', max_length=30, blank=True, null=True)
    tipo_veiculo = models.CharField('Porte do Veículo', max_length=30, choices=TIPO_VEICULO_CHOICES, default='Médio')

    class Meta:
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'
        ordering = ['placa']

    def save(self, *args, **kwargs):
        # Normaliza a placa sempre em caixa alta e sem espaços
        if self.placa:
            self.placa = self.placa.strip().upper().replace('-', '')
        super().save(*args, **kwargs)

    def pode_lavar_esta_semana(self):
        """
        RN01: Veículos de clientes faturados possuem limite estrito de
        no máximo 1 lavagem por semana corrente.
        Retorna (bool_permitido, mensagem).
        """
        if self.cliente.tipo != 'FATURADO':
            return True, ""

        hoje = timezone.localtime(timezone.now())
        # Início da semana corrente (Segunda-feira às 00:00:00)
        inicio_semana = (hoje - timedelta(days=hoje.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)

        ja_lavou = self.ordens_servico.filter(data_hora__gte=inicio_semana).exists()
        if ja_lavou:
            return False, "Limite semanal de lavagens atingido para este veículo faturado (Regra RN01)."

        return True, ""

    def __str__(self):
        return f"{self.placa} - {self.marca} {self.modelo} ({self.cliente.nome})"


# 3. Tabela: Lavadores (RF03)
class Lavador(models.Model):
    nome = models.CharField('Nome do Lavador', max_length=100)
    cpf = models.CharField('CPF', max_length=20, blank=True, null=True)
    telefone = models.CharField('Telefone / WhatsApp', max_length=20, blank=True, null=True)
    percentual_comissao = models.DecimalField(
        'Comissão Padrão (%)',
        max_digits=5,
        decimal_places=2,
        default=Decimal('10.00'),
        help_text='Percentual repassado por lavagem realizada (ex: 10.00 para 10%)'
    )
    ativo = models.BooleanField('Ativo na Operação', default=True)

    class Meta:
        verbose_name = 'Lavador'
        verbose_name_plural = 'Lavadores'
        ordering = ['nome']

    def __str__(self):
        return self.nome


# 4. Tabela: Catálogo de Serviços (RF04 / RN03 - Restrito ao ADM)
class Servico(models.Model):
    descricao = models.CharField('Descrição do Serviço', max_length=100)
    valor = models.DecimalField('Valor Padrão (R$)', max_digits=10, decimal_places=2)
    tempo_estimado_minutos = models.PositiveIntegerField('Tempo Estimado (minutos)', default=30)
    ativo = models.BooleanField('Disponível', default=True)

    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'
        ordering = ['valor']

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor:.2f}"


# 5. Tabela: Ordens de Serviço - OS (RF05, RN01, RN02)
class OrdemServico(models.Model):
    STATUS_CHOICES = [
        ('FILA', 'Em Fila'),
        ('LAVAGEM', 'Em Lavagem'),
        ('SECAGEM', 'Aguardando Secagem'),
        ('CONCLUIDO', 'Concluído'),
        ('ENTREGUE', 'Entregue'),
    ]

    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT, related_name='ordens_servico', verbose_name='Veículo')
    servico = models.ForeignKey(Servico, on_delete=models.PROTECT, related_name='ordens_servico', verbose_name='Serviço Solicitado')
    lavador = models.ForeignKey(Lavador, on_delete=models.PROTECT, related_name='ordens_servico', verbose_name='Lavador Designado')
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='ordens_criadas', verbose_name='Operador Responsável')
    status = models.CharField('Status da OS', max_length=30, choices=STATUS_CHOICES, default='FILA')
    observacoes_veiculo = models.TextField('Observações / Vistoria de Entrada', blank=True, null=True, help_text='Riscos, avarias prévias ou itens deixados no veículo')
    valor_total = models.DecimalField('Valor Total (R$)', max_digits=10, decimal_places=2, blank=True, null=True)
    data_hora = models.DateTimeField('Data e Hora de Entrada', auto_now_add=True)
    data_hora_saida = models.DateTimeField('Data e Hora de Saída', blank=True, null=True)

    class Meta:
        verbose_name = 'Ordem de Serviço'
        verbose_name_plural = 'Ordens de Serviço'
        ordering = ['-data_hora']

    def clean(self):
        super().clean()
        # RN01: Validação do limite semanal para clientes faturados
        if self.pk is None and hasattr(self, 'veiculo') and self.veiculo:
            permitido, motivo = self.veiculo.pode_lavar_esta_semana()
            if not permitido:
                raise ValidationError({'veiculo': motivo})

    def save(self, *args, **kwargs):
        # Preenche o valor total com o valor de tabela do serviço caso não definido
        if self.valor_total is None and self.servico_id:
            self.valor_total = self.servico.valor

        # Executa validação das regras de negócio
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def valor_comissao(self):
        """Calcula o valor monetário da comissão do lavador para esta OS (RF03)."""
        base = self.valor_total or (self.servico.valor if self.servico else Decimal('0.00'))
        if self.lavador and self.lavador.percentual_comissao:
            return round(base * (self.lavador.percentual_comissao / Decimal('100.00')), 2)
        return Decimal('0.00')

    def __str__(self):
        return f"OS #{self.id:04d} - {self.veiculo.placa} ({self.get_status_display()})"


# 6. Tabela: Pagamentos e Caixa (RF06, RN02)
class Pagamento(models.Model):
    FORMA_PAGAMENTO_CHOICES = [
        ('PIX', 'PIX'),
        ('DINHEIRO', 'Dinheiro em Espécie'),
        ('CARTAO', 'Cartão de Débito/Crédito'),
        ('FATURADO', 'Faturado / Convênio Corporativo'),
    ]

    MOMENTO_CHOICES = [
        ('ENTRADA', 'No Momento da Entrada'),
        ('RETIRADA', 'No Momento da Retirada / Saída'),
    ]

    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('CONCLUIDO', 'Concluído'),
    ]

    ordem_servico = models.OneToOneField(OrdemServico, on_delete=models.CASCADE, related_name='pagamento', verbose_name='Ordem de Serviço')
    forma_pagamento = models.CharField('Forma de Pagamento', max_length=30, choices=FORMA_PAGAMENTO_CHOICES)
    momento_pagamento = models.CharField('Momento do Pagamento (RN02)', max_length=20, choices=MOMENTO_CHOICES, default='ENTRADA')
    status = models.CharField('Status do Pagamento', max_length=20, choices=STATUS_CHOICES, default='CONCLUIDO')
    valor_pago = models.DecimalField('Valor Pago (R$)', max_digits=10, decimal_places=2)
    data_pagamento = models.DateTimeField('Data e Hora do Pagamento', auto_now_add=True)

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
        ordering = ['-data_pagamento']

    def __str__(self):
        return f"Pagamento OS #{self.ordem_servico.id:04d} - {self.get_forma_pagamento_display()} (R$ {self.valor_pago:.2f})"

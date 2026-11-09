# Elicitação de Requisitos - Sistema de Gerenciamento de Posto de Lavagem

Este documento registra as atividades de elicitação de requisitos realizadas para o **Lava Jato do Valmir**, mapeando as necessidades dos stakeholders, observações de campo e análise documental.

---

## 1. Entrevistas Semiestruturadas

### Entrevista 01: Propriedade e Administração
- **Data:** 14/07/2026
- **Entrevistado:** Seu Valmir (Dono e Administrador)
- **Entrevistador:** Analista de Requisitos / Ednaldo
- **Objetivo:** Compreender o modelo de negócio, dores operacionais, visão financeira e regras de restrição do lava jato.

#### Perguntas e Respostas:
1. **Pergunta:** Seu Valmir, qual é hoje o maior gargalo na gestão do lava jato?
   - *Resposta:* "É o controle do dinheiro e das fichas no papel. No fim do dia, perco muito tempo somando comandas rasuradas. Às vezes o cliente paga no PIX ou dinheiro e a recepcionista não anota direito quem lavou, aí dá confusão na hora de pagar a comissão dos lavadores."
2. **Pergunta:** Como funcionam os clientes faturados (empresas parceiras)?
   - *Resposta:* "Temos convênio com frotas locais. O combinado é que cada veículo faturado só pode lavar **no máximo 1 vez por semana**. Hoje controlamos isso na planilha impressa, mas às vezes passa lavagem duplicada sem a gente perceber."
3. **Pergunta:** Quem pode alterar valores de serviços e fechar o caixa no fim do expediente?
   - *Resposta:* "Apenas eu. A recepcionista pode lançar e receber, mas mudar preço de tabela ou fechar o resumo do dia tem que ser com senha de administrador."

#### Requisitos Derivados:
- **RF01:** Gerenciar usuários com perfis diferenciados.
- **RF03:** Gerenciar lavadores e cálculo de comissões.
- **RF04:** Gerenciar tabela de tipos de serviços e valores (restrito ao ADM).
- **RF08:** Gerar relatórios operacionais e financeiros de fechamento.
- **RN01:** Clientes faturados têm limite estrito de no máximo 1 lavagem por semana.
- **RN03:** Encerramento do caixa diário e alteração de valores restritos ao Administrador.
- **RNF05:** Restrição de funcionalidades por nível de perfil (Administrador x Recepcionista).

---

### Entrevista 02: Equipe Operacional (Lavadores)
- **Data:** 15/07/2026
- **Entrevistados:** Equipe de Pátio / Lavadores
- **Entrevistador:** Analista de Requisitos
- **Objetivo:** Entender a dinâmica de acompanhamento dos veículos no pátio e controle de comissão por lavagem.

#### Perguntas e Respostas:
1. **Pergunta:** Como vocês sabem qual veículo deve ser lavado primeiro e qual o tipo de lavagem solicitada?
   - *Resposta:* "A recepcionista grita. O problema é que pode haver confusão no tipo de serviço a ser feito ou o lavador correto definido por ordem de chegada no posto equivalente ao dia."
2. **Pergunta:** Como vocês conferem se a comissão do dia está correta?
   - *Resposta:* "A gente verifica no que foi anotado na planilha do controle de lavagem do dia, e vai anotando no proprio celular. No caso de divergência com o relatório do caixa, porque faltou lançar o nome de quem lavou o veiculo."

#### Requisitos Derivados:
- **RF03:** Vínculo direto e obrigatório do lavador responsável na Ordem de Serviço.
- **RF05:** Registrar e atualizar o status da lavagem em tempo real (ex: *Em Fila*, *Em Lavagem*, *Aguardando Secagem*, *Concluído*).
- **RNF02:** Interface responsiva/amigável para consulta rápida em tablets ou smartphones no pátio.

---

### Entrevista 03: Cliente Faturado (Frota / Empresa Parceira)
- **Data:** 15/07/2026
- **Entrevistado:** Gestor de Frota de Empresa Conveniada
- **Entrevistador:** Analista de Requisitos
- **Objetivo:** Entender a experiência de atendimento corporativo e necessidades de validação.

#### Perguntas e Respostas:
1. **Pergunta:** Como é a rotina quando o motorista da sua empresa leva o carro ao lava jato?
   - *Resposta:* "O motorista apresenta o veículo com a placa cadastrada. O problema é que precisamos de um comprovante claro e relatórios mensais para bater com a nossa fatura. Se um motorista levar o carro duas vezes na mesma semana, o sistema de vocês deveria bloquear na hora."

#### Requisitos Derivados:
- **RF02:** Cadastrar e vincular veículos a clientes faturados/conveniados.
- **RF06:** Emitir comprovante de entrada/atendimento.
- **RF07:** Consultar histórico de lavagens por placa/veículo.
- **RN01:** Regra de bloqueio automático para lavagem excedente de veículo faturado na mesma semana.

---

### Entrevista 04: Cliente Avulso (Pessoa Física)
- **Data:** 16/07/2026
- **Entrevistado:** Cliente Frequente do Lava Jato
- **Entrevistador:** Analista de Requisitos
- **Objetivo:** Identificar expectativas quanto à agilidade, pagamento e acompanhamento do serviço.

#### Perguntas e Respostas Simuladas:
1. **Pergunta:** Qual a sua maior insatisfação ao deixar o carro no lava jato?
   - *Resposta:* "Demorar para ser atendido na recepção enquanto procuram meu cadastro e não saber exatamente a que horas o carro vai ficar pronto. Gostaria de pagar logo na entrada ou na saída via PIX/Cartão sem ter que esperar procurar comanda de papel."

#### Requisitos Derivados:
- **RF02:** Localização e cadastro ágil de cliente e veículo pela placa.
- **RF06:** Registrar pagamento flexível e emitir comprovante.
- **RN02:** O pagamento do serviço pode ser efetuado no momento da entrada ou na retirada do veículo.
- **RNF03:** Tempo de resposta da consulta no sistema inferior a 2 segundos.

---

## 2. Observação (Observação Direta de Campo)

- **Data de Realização:** 16/07/2026 - 20/07/2026 (Período da manhã - 08:30 às 11:30)
- **Local:** Recepção e Pátio do Lava Jato do Valmir
- **Constatações:**
  1. A recepcionista gasta em média 3 a 5 minutos por cliente procurando fichas físicas em pastas suspensas.
  2. Foram observados 2 veículos aguardando no pátio sem que os lavadores soubessem se a lavagem era simples ou completa.
  3. Troco e notas de papel ficam misturados em uma gaveta sem registro imediato no sistema financeiro.

---

## 3. Análise de Documentos

- **Insumos Analisados:**
  - Planilha impressa de controle manual de caixa diário.
  - Talões de recibo em papel autocopiativo.
  - Planilha impressa de cadastro de clientes faturados.
  
- **Conclusões:**
  - Alta incidência de rasuras e letras ilegíveis no registro de placas e valores.
  - Ausência de padronização nas nomenclaturas dos serviços (ex: "Lavagem Geral", "Geral + Cera", "L. Completa").
  - Ausência de histórico consolidado por veículo, inviabilizando métricas de fidelidade ou relatórios precisos.
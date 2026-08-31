# Roadmap de Produto (Product Roadmap)
## Sistema de Gerenciamento de Posto de Lavagem

Este documento apresenta o planejamento estratégico de evolução do sistema, dividido em fases de maturidade e marcos de entrega.

---

## 🗺️ Visão Geral das Fases

---

## 🚀 Fase 1: MVP (Produto Mínimo Viável)
> **Objetivo:** Eliminar a operação manual em papel e permitir a abertura e acompanhamento digital das Ordens de Serviço (O.S.).

* **Escopo Funcional:**
  * **RF01:** Autenticação e cadastro básico de Usuários (Administrador e Recepcionista).
  * **RF02:** Cadastro e consulta rápida de Clientes e Veículos.
  * **RF04:** Cadastro simples de Tipos de Serviços e Tabela de Preços.
  * **RF05:** Registro de Ordem de Serviço (Abertura, atribuição de lavador e mudança de status em tempo real).
  * **RN02:** Seleção do momento do pagamento (Entrada ou Retirada).
* **Interface:** Telas responsivas essenciais para desktop e celular (**RNF02**).
* **Entrega de Valor:** Fim do risco de perda de papeis no pátio e visualização rápida dos veículos que estão sendo lavados.

---

## ⭐️ Fase 2: Versão 1.0 (Lançamento Oficial Operacional)
> **Objetivo:** Consolidar a gestão financeira, controle de comissões e aplicação estrita das regras de negócio.

* **Escopo Funcional:**
  * **RF03 & Comissões:** Cálculo automático da comissão por lavador e relatório de acerto financeiro.
  * **RF06:** Registro de Pagamentos (Dinheiro, PIX, Cartão) e emissão de comprovante/recibo simples.
  * **RF07:** Histórico completo de lavagens por placa/veículo.
  * **RF08:** Relatórios Operacionais e Financeiros consolidados (fechamento de caixa diário).
  * **RN01:** Regra de bloqueio de mais de 1 lavagem/semana para clientes Faturados (**FE01**).
  * **RN03:** Restrição de alteração de preços e fechamento de caixa apenas para perfil Administrador.
* **Infraestrutura:** Rotina automatizada de Backup diário (**RNF04**).
* **Entrega de Valor:** Controle financeiro total da operação, transparência no pagamento de funcionários e segurança dos dados.

---

## 🔮 Fase 3: Versão 2.0 (Automação e Escalabilidade)
> **Objetivo:** Expandir a experiência do cliente final, integração de pagamentos e automações de comunicação.

* **Escopo Funcional / Melhorias:**
  * **Notificação Automática:** Envio de mensagem automática via WhatsApp/SMS quando o veículo mudar para o status `Pronta para Retirada`.
  * **Integrador de Pagamentos:** Integração via API com maquininhas de cartão/PIX para baixa automática de pagamento.
  * **Emissão Fiscal:** Integração para emissão opcional de Nota Fiscal (NFC-e).
  * **Suporte Multi-filial:** Preparação da arquitetura para gerenciar mais de uma unidade/posto na mesma conta.
  * **Painel de Pátio (TV/Monitor):** Dashboard visual para ser fixado na parede da oficina/recepção mostrando a fila de carros.

---

## 📌 Resumo da Matriz de Escopo por Fase

| Módulo / Funcionalidade | MVP (Fase 1) | V1.0 (Fase 2) | V2.0 (Fase 3) |
|---|:---:|:---:|:---:|
| Gestão de Veículos e Clientes | **Sim** | **Sim** | **Sim** |
| Fila de O.S. no Pátio | **Sim** | **Sim** | **Sim** |
| Registro de Pagamento | Parcial | **Sim** | **Sim** |
| Controle de Comissões | ❌ | **Sim** | **Sim** |
| Relatórios Financeiros | ❌ | **Sim** | **Sim** |
| Bloqueio de Cliente Faturado | ❌ | **Sim** | **Sim** |
| Notificação via WhatsApp | ❌ | ❌ | **Sim** |
| API de Pagamento / NFC-e | ❌ | ❌ | **Sim** |
# BR [Versão em Português](README.pt-BR.md)
# Event Horizon

Event Horizon é uma ferramenta modular de linha de comando designada para operações de rede controladas, enumeração, e teste de conectividade

A ferramenta prioriza precisão, controle, e baixo impacto operacional em relação à velocidade bruta ou à execução em alto volume.

---

## Filosofia

Event Horizon foi construído em torno de um princípio simples.

> **Controle sobre a velocidade**

Em vez de realizar operações agressivas e ruidosas, a ferramenta se concentra em:

* Execução Controlada
* Comportamento previsivel
* Baixo footprint operacional
* Design Modular
* Workflows de CLI confiáveis

Ele foi projetado para funcionar como um "canivete suíço" confiável para tarefas relacionadas à rede.

---

## Objetivos do Projeto

* Arquitetura Modular (`modulo -> ação`)
* Estrutura de comando clara e explicita
* Controle preciso da execução (tempos limite, novas tentativas, taxa)
* Saída consistente e previsível
* Extensibilidade para protocolos e recursos futuros

---

## Recursos Planejados

### Subdomain

* Descoberta de subdominio por bruteforce
* Resolução de DNS

### SMB

* Gerenciamento controlado de conexões
* Tentativas de autenticação (usuário/senha)
* Ataques de força bruta contra senhas (com taxa controlada)

### Core

* Normalização de destino (domínio, IP, entrada de arquivo)
* Parâmetros de execução configuráveis
* Controle de registro e verbosidade

---

## CLI Design

A ferramenta segue uma estrutura simples:

```
eventhorizon <module> <action> [options]
```

Exemplo:

```
eventhorizon smb connect -t <target> --anonymous
eventhorizon smb spray -t <target> -U users.txt -P passwords.txt
eventhorizon subdomain bruteforce -t example.com -w subdomains.txt
eventhorizon subdomain resolve -t example.com
```

---

## Filosofia de Execução

O Event Horizon não foi projetado para maximizar throughput.

Em vez disso, ele se concentra em:

* Controle do ritmo de requisições
* Mínimo de ruído desnecessário
* Comportamento definido pelo operador
* Configurações padrão seguras com ajustes opcionais

---

## Status

Este projeto encontra-se atualmente em fase inicial de desenvolvimento.

A arquitetura principal e a estrutura da interface de linha de comando (CLI) estão sendo definidas antes da implementação completa.

---

## Licença

MIT License

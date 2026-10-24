# 🇺🇸 [English version](README.md)
# Event Horizon

Event Horizon é uma ferramenta modular de linha de comando voltada para operações de rede controladas, enumeração e testes de conectividade.

A ferramenta prioriza precisão, controle, e baixo impacto operacional em relação à velocidade bruta ou à execução em alto volume.

---

## Filosofia

Event Horizon foi construído em torno de um princípio simples.

> **Controle sobre a velocidade**

Em vez de realizar operações agressivas e ruidosas, a ferramenta se concentra em:

* Execução Controlada
* Comportamento previsível
* Baixo footprint operacional
* Design Modular
* Workflows de CLI confiáveis

Ele foi projetado para funcionar como um "canivete suíço" confiável para tarefas relacionadas à rede.

---

## Objetivos do Projeto

* Arquitetura Modular (`módulo -> ação`)
* Estrutura de comando clara e explicita
* Controle preciso da execução (timeouts, modo de envio, taxa)
* Saída consistente e previsível
* Extensibilidade para protocolos e recursos futuros

---

## Módulos e Ações

### tcp

* `synscan` — SYN scan controlado (via Scapy), com TTL e source port customizáveis. Exige modo de envio explícito (`sequential` ou `batch`).
* `connectscan` — scan TCP connect controlado (three-way handshake completo), com timeout customizável. Exige modo de envio explícito (`sequential` ou `batch`).
* `portpeek` — checagem avulsa de uma única porta.

### subdomain

* `bruteforce` — descoberta de subdomínio via wordlist, com resolução de DNS opcional e lookups multithreaded.
* `takeover` — detecção de subdomain takeover (resolução de CNAME + base de fingerprints de serviços).

### smtp

* `vrfycrack` — enumeração de usuários SMTP via comando `VRFY`, com banner grabbing opcional.

---

## CLI Design

A ferramenta segue uma estrutura simples:

```
eventhorizon <module> <action> [options]
```

Exemplos:

```
eventhorizon tcp synscan -t example.com -m sequential
eventhorizon tcp synscan -t example.com -p 22,80,443 -m batch -v
eventhorizon tcp connectscan -t 192.168.1.1 -m batch --timeout 1.5
eventhorizon tcp portpeek -t example.com -p 443

eventhorizon subdomain bruteforce -t example.com -w subdomains.txt
eventhorizon subdomain bruteforce -t example.com -w subdomains.txt -r --threads 20
eventhorizon subdomain takeover -t example.com -w subdomains.txt -v

eventhorizon smtp vrfycrack -t mail.example.com -w users.txt -b -v
```

---

## Filosofia de Execução

O Event Horizon não foi projetado para maximizar throughput.

Em vez disso, ele se concentra em:

* Controle do ritmo de requisições
* Mínimo de ruído desnecessário
* Comportamento definido pelo operador
* Configurações padrão seguras com ajustes opcionais — todo scan de porta exige `--mode` (`sequential` ou `batch`) explícito, em vez de escolher um silenciosamente

---

## Status

🚧 Este projeto encontra-se atualmente em desenvolvimento ativo, em fase inicial.

Já implementado: scan de portas TCP (via SYN e via connect, modos sequencial e batch), bruteforce e detecção de takeover de subdomínio, enumeração de usuários SMTP via VRFY.

---

## Licença

MIT License
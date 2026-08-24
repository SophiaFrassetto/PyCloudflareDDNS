# PyCloudflareDDNS

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Cloudflare](https://img.shields.io/badge/Cloudflare-DNS%20API-F38020?logo=cloudflare&logoColor=white)](https://api.cloudflare.com/)
[![IPv4%20%2B%20IPv6](https://img.shields.io/badge/IPv4%20%2B%20IPv6-supported-2E8B57)](https://github.com/)
[![License](https://img.shields.io/badge/license-MIT-1f6feb)](LICENSE)

[English version](README_EN.md)

## Sobre o projeto

Atualiza automaticamente registros DNS `A` (IPv4) e `AAAA` (IPv6) na
Cloudflare com os endereços IP públicos atuais da máquina. O programa consulta
um ou mais provedores de IP e só altera o registro quando o endereço mudou.

## Requisitos

- Python 3.10 ou superior
- Uma zona/domínio gerenciado pela Cloudflare
- Um token da API da Cloudflare com as permissões `Zone - Read` e
  `DNS - Edit` para a zona desejada

## Configuração

1. Crie e ative um ambiente virtual:

   ```bash
   python -m venv .venv
   ```

   ```bash
   # Windows PowerShell
   .venv\Scripts\Activate.ps1

   # Linux/macOS
   source .venv/bin/activate
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Crie um arquivo `.env` na raiz do projeto:

   ```dotenv
   CF_API_TOKEN=seu_token_da_cloudflare
   ZONE_NAME=exemplo.com
   IPV4_RECORDS=home.exemplo.com
   IPV6_RECORDS=
   IPV4_PROVIDERS=https://api.ipify.org,https://ifconfig.me/ip
   IPV6_PROVIDERS=https://api6.ipify.org
   ```

| Variável | Descrição |
| --- | --- |
| `CF_API_TOKEN` | Token da API com acesso de leitura à zona e edição de DNS. |
| `ZONE_NAME` | Domínio da zona na Cloudflare. |
| `IPV4_RECORDS` | Nomes dos registros `A`, separados por vírgula. |
| `IPV6_RECORDS` | Nomes dos registros `AAAA`, separados por vírgula. |
| `IPV4_PROVIDERS` | URLs que retornam o IPv4 público, separadas por vírgula. |
| `IPV6_PROVIDERS` | URLs que retornam o IPv6 público, separadas por vírgula. |

Deixe uma lista de registros ou provedores vazia para desativar esse tipo de
IP. Os provedores são tentados na ordem informada. Não compartilhe o arquivo
`.env` nem o token da API.

## Atenção: CGNAT no IPv4

O **CGNAT** (Carrier-Grade NAT) coloca vários clientes atrás do mesmo IPv4
público. Nesse cenário, o endereço retornado pelos provedores de IP pode ser
compartilhado e não permite conexões externas diretamente até a sua rede,
mesmo que o registro DNS esteja atualizado corretamente.

O PyCloudflareDDNS atualiza o DNS, mas não consegue desabilitar o CGNAT nem
criar um IPv4 público. Para receber conexões externas por IPv4, solicite à sua
operadora a desativação do CGNAT ou a contratação de um IPv4 público. Caso a
operadora não ofereça essa opção, será necessário trocar de provedor. O IPv6
pode continuar funcionando normalmente, desde que esteja disponível e
configurado na rede.

## Execução

Com o ambiente virtual ativado, execute:

```bash
python main.py
```

As mensagens no terminal mostram a validação das credenciais, o IP encontrado
e os registros atualizados. Para execução automática, agende esse comando no
Agendador de Tarefas do Windows ou no `cron`.

### Agendamento no Windows

1. Abra o **Agendador de Tarefas** (`taskschd.msc`) e selecione **Criar Tarefa**.
2. Na aba **Geral**, informe um nome, como `PyCloudflareDDNS`.
3. Na aba **Disparadores**, clique em **Novo** e escolha **Ao fazer logon** ou
   **Ao iniciar o computador**.
4. Na aba **Ações**, clique em **Nova** e preencha:

   - **Programa/script:**
     `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`
   - **Adicionar argumentos:**
     `-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\caminho\para\PyCloudflareDDNS\run.ps1"`
   - **Iniciar em:** `C:\caminho\para\PyCloudflareDDNS`

5. Na aba **Condições**, desmarque **Iniciar a tarefa somente se o computador
   estiver ligado à energia da rede elétrica**, caso ela esteja selecionada.
6. Confirme em **OK**. Use **Executar** no menu de contexto da tarefa para
   testar imediatamente.

Substitua `C:\caminho\para\PyCloudflareDDNS` pelo caminho real do projeto, caso ele
esteja em outra pasta. O arquivo `run.ps1` usa o ambiente virtual `.venv` quando
ele existe e, caso contrário, utiliza o Python disponível no sistema.

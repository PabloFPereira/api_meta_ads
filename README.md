# Extração de Dados do Meta Ads com Python

## Introdução

Este guia fornece instruções passo a passo para configurar e executar a API da Meta que coleta insights de anúncios.

## Pré-requisitos

- **Conta de desenvolvedor na Meta (Facebook)**.
- **Python 3** instalado.
- **Conhecimentos básicos em Python e no uso de terminal/linha de comando**.

## Passo a Passo

### 1. Criar uma pasta e navegar até ela

Abra o terminal (ou prompt de comando) e execute os seguintes comandos:

```bash
# Crie uma nova pasta para o projeto
mkdir minha_api_meta

# Navegue até a pasta criada
cd minha_api_meta
```

### 2. Clonar o projeto do GitHub

```bash
# Clone o repositório do GitHub
git clone https://github.com/PabloFPereira/api_meta_ads.git

# Navegue até a pasta do projeto
cd api_meta_ads
```

### 3. Instalar as bibliotecas necessárias

Certifique-se de que você tem o `pip` instalado. Em seguida, instale a biblioteca `requests`:

```bash
pip install requests
```

### 4. Obter o Token de Desenvolvedor

1. Acesse o [Meta for Developers](https://developers.facebook.com/).
2. Faça login com sua conta do Facebook.
3. Crie um novo aplicativo:
   - Clique em **Meus Apps** > **Criar App**.
   - Selecione o tipo de aplicativo que melhor se adapta às suas necessidades e siga as instruções.
4. Obtenha o token de acesso:
   - No painel do aplicativo, vá para **Ferramentas** > **Graph API Explorer**.
   - Selecione seu aplicativo no menu suspenso.
   - Gere um token de acesso de **usuário** ou **sistema** com as permissões necessárias.
   - Copie o token gerado.

### 5. Configurar o Código

1. No diretório do projeto, localize a pasta `Token`. Ela já existe, portanto, não é necessário criá-la.

2. Dentro da pasta `Token`, abra o arquivo `fb_token.py` e cole seu token de acesso:

   ```python
   "seu_token_de_acesso_aqui"
   ```

3. No arquivo principal do código `api_meta.py`, verifique se o caminho para o token está correto:

   ```python
   fb_api = open("Token/fb_token.py").read().strip()
   ```

4. Substitua `"xxxxxxxxxxx"` pelo **ID da sua conta de anúncios**:

   ```python
   ad_acc = "seu_id_de_conta_de_anuncios"
   ```

5. Opcional: Ajuste a data específica para os insights, se necessário:

   ```python
   specific_date = "YYYY-MM-DD"  # Exemplo: "2024-10-08"
   ```

### 6. Executar o Script

No terminal, execute o script Python:

```bash
python api_meta.py
```

### 7. Verificar a Saída

Os dados dos insights serão salvos no arquivo especificado no código, por exemplo:

```bash
saida_api.txt
```


Nota: Este guia foi elaborado para facilitar a configuração e execução do projeto. Se você encontrar algum problema ou tiver dúvidas, sinta-se à vontade para abrir uma issue no repositório.

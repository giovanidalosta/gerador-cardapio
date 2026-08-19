# Gerador de Cardápio

Este projeto é uma aplicação web que permite gerar cardápios a partir de arquivos Excel. A aplicação utiliza o Flask como framework web e a biblioteca Pillow para manipulação de imagens.

## Estrutura do Projeto

```
gerador-cardapio
├── app.py                # Arquivo principal da aplicação
├── requirements.txt      # Dependências do projeto
├── render.yaml           # Configurações para implantação no Render
├── README.md             # Documentação do projeto
├── templates             # Diretório para templates HTML
│   └── index.html       # Template da interface do usuário
├── static                # Diretório para arquivos estáticos
│   ├── css              # Diretório para arquivos CSS
│   │   └── style.css    # Estilos da aplicação
│   └── js               # Diretório para arquivos JavaScript
│       └── app.js       # Funcionalidade do lado do cliente
├── fontes                # Diretório para arquivos de fonte
│   ├── Exo-Bold.ttf     # Fonte utilizada na aplicação
│   └── calibri.ttf      # Outra fonte utilizada na aplicação
└── CardapiosGerados     # Diretório para armazenar cardápios gerados
    └── .gitkeep         # Arquivo placeholder para controle de versão
```

## Instalação

1. Clone o repositório:
   ```
   git clone <URL_DO_REPOSITORIO>
   cd gerador-cardapio
   ```

2. Crie um ambiente virtual e ative-o:
   ```
   python -m venv venv
   source venv/bin/activate  # Para Linux/Mac
   venv\Scripts\activate     # Para Windows
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

## Execução

Para executar a aplicação, utilize o seguinte comando:

```
python app.py
```

A aplicação estará disponível em `http://127.0.0.1:5000`.

## Implantação no Render

1. Envie este projeto para um repositório no GitHub ou GitLab.
2. No Render, acesse **New + > Blueprint** e conecte o repositório.
3. Selecione o arquivo `render.yaml` e confirme a implantação.

O Blueprint instala as dependências com `pip install -r requirements.txt` e inicia a aplicação com Gunicorn. O Render define automaticamente a variável `PORT` usada pelo serviço.

## Funcionalidade

A aplicação permite que os usuários façam upload de um arquivo Excel contendo os dados do cardápio. Após o upload, o cardápio é gerado e salvo como uma imagem, que pode ser baixada pelo usuário.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.
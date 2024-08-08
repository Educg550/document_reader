# document_reader
Projeto simples para leitura e interpretação de texto de imagens e PDFs

# Como executar

Com a Docker Engine instalada e sendo executada na sua máquina, execute os seguintes comandos:

```bash
# Clonando o repositório
git clone https://github.com/Educg550/document_reader.git

# Criando a imagem Docker
make

# Executando o container
make run
```
Uma imagem `ocr-image-reader` será criada na sua máquina e um container de mesmo nome será executado.

# Como usar

Com o container em execução, acesse o endereço `http://localhost:8501` no seu navegador para acessar a interface gráfica feita com Streamlit. Você verá uma página com um campo para upload de arquivos. Os seguintes arquivos são compatíveis:

[X] Texto puro (txt)

A implementar:

[] PDF
[] Imagens (png, jpg, jpeg)

# Para desenvolvedores
Após feita uma modificação no código, você pode reconstruir a imagem Docker com o comando:

```bash
make rebuild
```

O comando acima irá reconstruir e executar a imagem `ocr-image-reader` em um novo container, com a última versão do código.

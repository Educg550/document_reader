# Document Reader 📷
Leitura e interpretação de texto de imagens, PDFs e texto puro

![preview mockup](https://github.com/user-attachments/assets/e1abed60-fe33-44fe-be8a-2528a8ad05d8)

# Tecnologias

- [Streamlit](https://streamlit.io/) 📊
- [EasyOCR](https://github.com/JaidedAI/EasyOCR) 👁️
- [pdf2image](https://github.com/Belval/pdf2image) 📄
- [Google Gemini LLM](https://cloud.google.com/gemini/docs) 🤖

# Como executar

Com a Docker Engine instalada e sendo executada na sua máquina, primeiro clone o repositório:

```bash
# Clonando o repositório
git clone https://github.com/Educg550/document_reader.git
```

Após, insira a sua chave da API do Gemini em um arquivo `.env` na raiz do projeto (caso deseje utilizar a LLM para detecção):

Exemplo de arquivo `.env`:

```bash
GOOGLE_API_KEY="SUA_CHAVE_AQUI"
```

Você pode manter o arquivo `.env` vazio caso não vá usar detecção com LLM. Em seguida, execute os comandos:

```bash
# Criando a imagem Docker
make

# Executando o container
make run
```


Uma imagem `ocr-image-reader` será criada na sua máquina e um container de mesmo nome será executado.

# Como usar

Com o container em execução, acesse o endereço `http://localhost:8501` no seu navegador para acessar a interface gráfica feita com Streamlit. Você verá uma página com um campo para upload de arquivos. Os seguintes arquivos são compatíveis:

- [x]  **Texto puro** (`.txt`)
- [x]  **PDF** (`.pdf`)
- [x]  **Imagens** (`.png`, `.jpg`, `.jpeg`)

# Para desenvolvedores
Após feita uma modificação no código, você pode reconstruir a imagem Docker com o comando:

```bash
make rebuild
```

O comando acima irá reconstruir e executar a imagem `ocr-image-reader` em um novo container, com a última versão do código.

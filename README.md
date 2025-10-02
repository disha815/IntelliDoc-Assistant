# 📋 IntelliDoc Assistant: NHPC Smart PDF Chatbot

A powerful Streamlit-based PDF document assistant that uses RAG (Retrieval-Augmented Generation) to help you interact with your PDF documents intelligently. Built specifically for NHPC (National Hydroelectric Power Corporation) document processing.

## 🚀 Features

- **PDF Text Extraction**: Advanced text extraction using Docling with OCR support
- **Smart Q&A**: Ask questions about your PDF content using natural language
- **Table Detection**: Automatically extracts and searches tables within documents
- **Chat History**: Maintains conversation history for better context
- **Vector Search**: Uses FAISS for efficient similarity search
- **Downloadable Conversations**: Export your chat history

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **NLP/ML**: LangChain, Sentence Transformers
- **Document Processing**: Docling, PaddleOCR
- **Vector Database**: FAISS
- **LLM Model**: Google Gemma-3-27b-it (via Hugging Face)
- **LLM Integration**: Ollama support
- **Data Processing**: Pandas, Scikit-learn

## �📦 Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/disha815/IntelliDoc-Assistant.git
   cd IntelliDoc-Assistant
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv rag-env
   ```

3. **Activate the virtual environment**:

   - On Windows:
     ```bash
     rag-env\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source rag-env/bin/activate
     ```

4. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Set up LLM Model**:
   - **Option 1 - Hugging Face (Recommended)**: The application uses Google Gemma-3-27b-it model from Hugging Face
     ```bash
     # The model will be automatically downloaded when first used
     # Ensure you have sufficient GPU memory or use CPU inference
     ```
   - **Option 2 - Ollama (Alternative)**:
     - Install Ollama from [ollama.ai](https://ollama.ai)
     - Pull a suitable model: `ollama pull llama2`

## 🚀 Usage

1. **Start the application**:

   ```bash
   streamlit run app.py
   ```

2. **Upload a PDF**: Use the file uploader to select your PDF document

3. **Ask Questions**: Type your questions in the text input field

4. **View Results**: Get AI-powered answers with source references

5. **Download Chat**: Export your conversation history

## 📁 Project Structure

```
IntelliDoc Assistant/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── components/                 # UI components
│   ├── __init__.py
│   ├── chat_history.py        # Chat history rendering
│   └── sidebar.py             # Sidebar information
├── utils/                     # Utility modules
│   ├── __init__.py
│   ├── docling_extractor.py   # PDF text extraction
│   ├── prompt.py              # LLM prompts
│   ├── rag_pipeline.py        # RAG implementation
│   ├── table_extractor.py     # Table processing
│   └── ui_helpers.py          # UI helper functions
├── static/                    # Static assets
│   └── nhpc_logo.png
└── logs/                      # Application logs
```

## 🔧 Configuration

The application can be configured through various parameters:

- **Chunk Size**: Modify text splitting parameters in `utils/rag_pipeline.py`
- **Vector Store**: Configure FAISS settings for your use case
- **LLM Model**: Currently configured to use Google Gemma-3-27b-it from Hugging Face
  - Model: `google/gemma-2-27b-it`
  - Source: Hugging Face Transformers
  - Supports both GPU and CPU inference
  - Change model in `utils/rag_pipeline.py` for different LLM options
- **OCR Settings**: Adjust PaddleOCR parameters in `utils/docling_extractor.py`

## 🧪 Key Components

### Document Processing

- **Docling**: Advanced PDF parsing with layout preservation
- **PaddleOCR**: OCR for image-based text extraction
- **Table Extraction**: Automated table detection and processing

### RAG Pipeline

- **Text Chunking**: Intelligent document segmentation
- **Vector Embedding**: Sentence transformer-based embeddings
- **Similarity Search**: FAISS-powered retrieval
- **Question Answering**: LangChain-based QA system

### LLM Integration

- **Primary Model**: Google Gemma-3-27b-it
  - **Size**: 27 billion parameters
  - **Performance**: High-quality responses with strong reasoning capabilities
  - **Context Length**: Supports long document contexts
  - **Inference**: Optimized for both GPU and CPU deployment
- **Alternative Models**: Easily configurable to use other Hugging Face models or Ollama

### User Interface

- **Streamlit**: Modern, responsive web interface
- **Real-time Processing**: Live document analysis
- **Interactive Chat**: Conversational document exploration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- NHPC for the use case and requirements
- Docling team for excellent PDF processing
- LangChain community for RAG framework
- Streamlit team for the amazing web framework

## 📞 Support

For questions and support, please open an issue in the GitHub repository.

---

Built with ❤️ for efficient document processing and intelligent information retrieval.

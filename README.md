# AgentSeleneium

## Overview

AgentSeleneium is an AI-powered web automation testing framework that leverages large language models (LLMs) to generate, execute, and debug Selenium and Playwright-based automation scripts. The project integrates LangChain for agent orchestration, Groq API for LLM interactions, and includes RAG (Retrieval-Augmented Generation) capabilities for enhanced test data processing. It supports OCR for image-based testing, encryption utilities for secure API key management, and comprehensive test case management via CSV files.

The framework automates the entire testing lifecycle: from natural language test case descriptions to executable code generation, execution, and intelligent debugging using AI.

## Features

- **AI-Powered Code Generation**: Uses Groq API and LangChain to generate Selenium/Playwright automation code from natural language test case descriptions.
- **Automated Execution**: Executes generated code and captures outputs/errors for verification.
- **Intelligent Debugging**: AI-driven error analysis and code correction for failed test executions.
- **RAG Integration**: Retrieval-Augmented Generation for processing test data from PDFs, DOCX, and TXT files.
- **Multi-Browser Testing**: Playwright configuration for testing across Chromium, Firefox, and WebKit.
- **OCR Support**: Image processing and text extraction using Tesseract and OpenCV.
- **Secure API Management**: Encryption utilities for storing and retrieving API keys securely.
- **Test Case Management**: CSV-based test case storage and runtime data handling.
- **Vector Database**: ChromaDB integration for efficient data retrieval and embeddings.
- **Extensible Agent Framework**: Built on LangChain with structured tools for modular functionality.

## Installation

### Prerequisites

- Python 3.11+
- Node.js 16+ (for Playwright)
- Git

### Setup Steps

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd AgentSeleneium
   ```

2. **Set Up Python Virtual Environment**
   ```bash
   python -m venv CustomVENV
   CustomVENV\Scripts\activate  # On Windows
   # source CustomVENV/bin/activate  # On macOS/Linux
   ```

3. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright Browsers**
   ```bash
   pip install playwright
   playwright install
   ```

5. **Install Node.js Dependencies** (for Playwright testing)
   ```bash
   npm install
   ```

6. **Configure API Keys**
   - Place your Groq API key in `Data/GroqAPI/GroqAPI_key.txt`
   - Use the encryption utilities in `Utils/` to secure your keys if needed
   - Run `python Utils/initialize_api_key.py` to set environment variables

## Usage

### Running the AI Agent

1. **Prepare Test Cases**
   - Add test cases to `TestData/TestCases.csv` in the format: `TestCaseName,Description`
   - Example:
     ```
     HomePageIcon,Verify the automationTesting web Logo is displayed in the automationTesting web Home Page https://testautomationpractice.blogspot.com/
     EnterName,Enter the name Alex in the name field
     ```

2. **Execute the Agent**
   ```bash
   python src/automatingwebPages.py
   ```

   The agent will:
   - Read test cases from CSV
   - Generate automation code using AI
   - Execute the code
   - Debug and fix any errors
   - Output results for each test case

### Running Playwright Tests

```bash
npx playwright test
```

### Using RAG Chatbot

The RAG functionality processes documents in the `Database/` folder (create this folder and add PDF/DOCX/TXT files).

### Generated Code

Generated automation scripts are saved in the `GeneratedCode/` folder with timestamps.

## Project Structure

```
AgentSeleneium/
├── src/
│   ├── automatingwebPages.py    # Main AI agent script
│   └── tools.py                 # Agent tools and utilities
├── Utils/
│   ├── __init__.py
│   ├── crawlURL.py             # URL crawling utilities
│   ├── ecryptSecret.py         # Encryption functions
│   ├── enCryptdeCrypt_apiKeys.py # API key encryption/decryption
│   ├── initialize_api_key.py   # API key initialization
│   ├── RAGChatbot.py           # RAG chatbot implementation
│   ├── readPdf.py              # PDF reading utilities
│   └── WebElementFinder.py     # Web element detection
├── tests/
│   └── example.spec.ts         # Playwright test example
├── TestData/
│   ├── RunTimeData.csv         # Runtime test data
│   └── TestCases.csv           # Test case definitions
├── GeneratedCode/              # AI-generated automation scripts
├── Data/
│   ├── GroqAPI/
│   │   └── GroqAPI_key.txt     # Groq API key storage
│   └── RAGChatBot_deepseek/
│       └── RAGChatBot_deepseek_key.txt
├── CustomVENV/                 # Python virtual environment
├── package.json                # Node.js dependencies
├── playwright.config.ts        # Playwright configuration
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Dependencies

### Python Dependencies

- **Core Framework**: langchain, langchain-core, langchain-community, langchain-groq
- **LLM Providers**: groq, openai, google-generativeai
- **Embeddings**: sentence-transformers, transformers, tokenizers
- **Data Processing**: pydantic, numpy, pandas, scikit-learn
- **Automation**: selenium, playwright
- **OCR**: pytesseract, Pillow, opencv-python
- **Networking**: requests, httpx, aiohttp, urllib3, tenacity
- **Vector DB**: faiss-cpu, chromadb

### Node.js Dependencies

- **Testing**: @playwright/test
- **Types**: @types/node

## Configuration

- **Playwright**: Configured in `playwright.config.ts` for multi-browser testing
- **API Keys**: Managed through environment variables and encrypted storage
- **Virtual Environment**: Custom Python venv in `CustomVENV/`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

ISC License

## Support

For issues and questions, please create an issue in the repository or contact the maintainers.

## Future Enhancements

- Integration with additional LLM providers
- Enhanced debugging capabilities
- GUI for test case management
- CI/CD pipeline integration
- Performance monitoring and reporting
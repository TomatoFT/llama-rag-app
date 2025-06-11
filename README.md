# LLaMA-RAG Demo

A Retrieval-Augmented Generation (RAG) system using LLaMA and FAISS, with a modern React frontend.

## Project Structure

- `src/`: Backend components
  - `retriever.py`: FAISS-based document retriever
  - `generator.py`: LLaMA-based text generator using llama-cpp-python
  - `rag_pipeline.py`: RAG pipeline implementation
  - `api.py`: FastAPI backend server
- `project/`: Frontend React application
  - `src/`: React components and logic
  - `public/`: Static assets
- `data/`: Document storage
- `models/`: Model storage
  - `llama-2-7b/`: LLaMA model files

## Setup

### Backend Setup

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Prepare the LLaMA model:
   - Convert your LLaMA model to GGML/GGUF format using [llama.cpp](https://github.com/ggerganov/llama.cpp)
   - Place the converted model file (e.g., `ggml-model.bin`) in `models/llama-2-7b/`

4. Run the setup script:
```bash
python setup.py
```

### Frontend Setup

1. Navigate to the project directory:
```bash
cd project
```

2. Install dependencies:
```bash
npm install
```

## Running the Application

### Backend

1. Start the FastAPI server:
```bash
python api_main.py
```
The API will be available at `http://localhost:8000`

### Frontend

1. In a new terminal, start the Vite development server:
```bash
cd project
npm run dev
```
The UI will be available at `http://localhost:5173`

## Usage

1. Open your browser and navigate to `http://localhost:5173`
2. Upload a PDF document using the file upload interface
3. Once the document is processed, you can start asking questions about its content
4. The AI will respond with answers based on the document's content

## API Endpoints

- `POST /upload`: Upload a PDF document for processing
- `POST /query`: Query the processed document
- `GET /health`: Check API health status

## Customization

### Backend
- Modify the retriever's model in `src/retriever.py`
- Adjust generation parameters in `src/generator.py`
- Customize the prompt template in `src/rag_pipeline.py`
- Use a different model by updating the `model_path` in `src/generator.py`

### Frontend
- Customize the UI components in `project/src/components/`
- Modify the API integration in `project/src/App.tsx`
- Update styles in `project/src/index.css`

## Model Conversion

To convert your LLaMA model to GGML/GGUF format:

1. Clone llama.cpp:
```bash
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
```

2. Convert your model:
```bash
python convert.py --outfile models/llama-2-7b/ggml-model.bin --outtype f16 /path/to/your/llama/model
```

For more details, refer to the [llama.cpp documentation](https://github.com/ggerganov/llama.cpp#usage). 
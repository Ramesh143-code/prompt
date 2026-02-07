# PromptGenius 🚀✨

> **Advanced NLP-Powered Prompt Optimization System**  
> A portfolio project showcasing expertise in Natural Language Processing and Prompt Engineering

![PromptGenius Banner](https://img.shields.io/badge/NLP-Project-00d4ff?style=for-the-badge) ![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python) ![React](https://img.shields.io/badge/React-18-61dafb?style=for-the-badge&logo=react) ![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?style=for-the-badge&logo=fastapi)

---

## 📖 Project Overview

**PromptGenius** is a production-grade web application that automatically analyzes and optimizes user prompts using state-of-the-art NLP techniques and prompt engineering best practices. It serves as a comprehensive portfolio project demonstrating advanced skills in both **Natural Language Processing** and **Prompt Engineering**.

### 🎯 Problem Statement

Most users struggle to craft effective prompts for Large Language Models (LLMs), resulting in suboptimal outputs. PromptGenius solves this by:
- Automatically detecting issues in prompts using NLP analysis
- Generating optimized variants using proven prompt engineering techniques
- Evaluating outputs to identify the best-performing prompts

### ✨ Key Features

- **🧠 Advanced NLP Analysis**
  - Intent classification using BERT zero-shot learning
  - Named Entity Recognition with spaCy
  - Domain detection and categorization
  - Quality scoring using linguistic features
  - Sentiment analysis
  - Complexity assessment

- **🎯 Intelligent Optimization**
  - Template-based prompt enhancement
  - Context injection and augmentation
  - Multiple optimization strategies (Few-shot, Chain-of-Thought, Role-based, etc.)
  - Domain-specific optimizations

- **⚖️ Output Evaluation**
  - Semantic similarity scoring
  - Coherence analysis
  - Completeness assessment
  - Automated ranking system

- **🎨 Beautiful User Interface**
  - Modern, responsive design
  - Real-time analysis feedback
  - Interactive result visualization
  - Elegant animations and transitions

---

## 🏗️ Architecture

### Technology Stack

**Backend:**
- **FastAPI** - High-performance Python web framework
- **Transformers (HuggingFace)** - BERT, RoBERTa for NLP tasks
- **spaCy** - Named Entity Recognition and linguistic analysis
- **Sentence-Transformers** - Semantic similarity computation
- **NLTK** - Text preprocessing and analysis
- **scikit-learn** - Machine learning utilities

**Frontend:**
- **React 18** - Modern UI framework
- **Vite** - Fast build tool
- **Custom CSS** - Beautiful, responsive design

**NLP Models:**
- `facebook/bart-large-mnli` - Zero-shot classification
- `distilbert-base-uncased-finetuned-sst-2-english` - Sentiment analysis
- `all-MiniLM-L6-v2` - Sentence embeddings
- `en_core_web_sm` - spaCy NER model

### System Architecture

```
┌─────────────────┐
│   React UI      │
│  (Frontend)     │
└────────┬────────┘
         │
         │ HTTP/JSON
         │
┌────────▼────────┐
│  FastAPI        │
│  (Backend)      │
└────────┬────────┘
         │
    ┌────┴────┬──────────┬──────────────┐
    │         │          │              │
┌───▼───┐ ┌──▼──┐  ┌────▼─────┐  ┌────▼──────┐
│ NLP   │ │Prompt│  │  Output  │  │   LLM     │
│Analyzer│ │Optim-│  │ Evaluator│  │  APIs     │
│       │ │izer  │  │          │  │(Optional) │
└───────┘ └──────┘  └──────────┘  └───────────┘
```

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.9 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. **Clone the repository**
```bash
cd promptgenius/backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download spaCy model**
```bash
python -m spacy download en_core_web_sm
```

5. **Download NLTK data**
```python
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger')"
```

6. **Configure environment variables (optional)**
```bash
cp .env.example .env
# Edit .env and add your API keys if you want LLM evaluation
```

7. **Run the backend server**
```bash
python main.py
# Or using uvicorn:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd promptgenius/frontend
```

2. **Install dependencies**
```bash
npm install
# Or with yarn:
yarn install
```

3. **Start development server**
```bash
npm run dev
# Or with yarn:
yarn dev
```

The application will be available at `http://localhost:3000`

---

## 📚 Usage Guide

### Basic Workflow

1. **Enter Your Prompt**
   - Type or paste any prompt in the text area
   - See real-time word and character count

2. **Choose Analysis Mode**
   - **Analyze Only**: Get NLP analysis without optimization
   - **Analyze & Optimize**: Full pipeline with optimized variants

3. **Review Analysis Results**
   - Quality score (0-100)
   - Intent classification with confidence
   - Extracted entities
   - Domain detection
   - Issues and suggestions

4. **Explore Optimized Variants**
   - Multiple optimized versions using different techniques
   - Improvement highlights
   - Evaluation scores (if enabled)
   - Best prompt recommendation

### Example Prompts

**Bad Prompt:**
```
write about AI
```

**PromptGenius Output:**
- **Quality Score**: 45/100
- **Issues**: Too vague, lacks context, no audience specified
- **Optimized Variant**: "Write a 500-word informative article about artificial intelligence for business professionals. Cover: current applications, benefits, challenges, and future trends. Tone: professional yet accessible. Include real-world examples."

---

## 🧪 NLP Techniques Explained

### 1. Intent Classification
**What it does:** Determines what the user is trying to accomplish  
**How:** Zero-shot classification using BERT (facebook/bart-large-mnli)  
**Categories:** Text generation, Q&A, summarization, code generation, etc.

### 2. Named Entity Recognition (NER)
**What it does:** Extracts key entities and topics from the prompt  
**How:** spaCy's statistical NER model  
**Entities:** People, organizations, locations, dates, etc.

### 3. Domain Detection
**What it does:** Identifies the subject area of the prompt  
**How:** Multi-label text classification  
**Domains:** Technical, business, creative, academic, etc.

### 4. Quality Assessment
**What it does:** Scores prompt effectiveness  
**How:** Linguistic feature analysis (length, specificity, clarity, complexity)  
**Output:** 0-100 score with specific issues and suggestions

### 5. Semantic Similarity
**What it does:** Measures how similar outputs are to expected results  
**How:** Sentence-BERT embeddings + cosine similarity  
**Use case:** Ranking optimized prompts by quality

### 6. Coherence Analysis
**What it does:** Evaluates logical flow and structure  
**How:** Consecutive sentence similarity scoring  
**Metric:** Coherence score (0-1)

---

## 🎓 Prompt Engineering Techniques Implemented

### 1. **Structured Prompting**
Adds clear structure with format, audience, length specifications

### 2. **Few-Shot Learning**
Includes examples to demonstrate desired output style

### 3. **Chain-of-Thought**
Breaks complex tasks into step-by-step reasoning

### 4. **Role-Based Prompting**
Assigns expert personas for domain-specific tasks

### 5. **Constraint-Based**
Adds explicit requirements and quality criteria

### 6. **Context Injection**
Enriches prompts with relevant background information

---

## 📊 API Documentation

### Endpoints

#### `POST /api/analyze`
Analyze a prompt using NLP techniques

**Request:**
```json
{
  "prompt": "write about dogs"
}
```

**Response:**
```json
{
  "intent": "text generation",
  "intent_confidence": 0.89,
  "entities": [...],
  "domain": "general knowledge",
  "quality_score": 45.0,
  "issues": ["Prompt is too short", "Contains vague terms"],
  "suggestions": ["Add more context and details"],
  "sentiment": "neutral",
  "complexity": "simple"
}
```

#### `POST /api/optimize`
Generate optimized prompt variants

#### `POST /api/optimize-and-evaluate`
Complete pipeline with LLM evaluation

#### `GET /api/stats`
Get system statistics

**Full API documentation available at:** `http://localhost:8000/docs`

---

## 🎨 UI/UX Highlights

- **Deep Ocean Theme**: Modern dark theme with gradient accents
- **Smooth Animations**: Fade-ins, hover effects, transitions
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Feedback**: Loading states, progress indicators
- **Interactive Cards**: Clickable, expandable result cards
- **Visual Metrics**: Progress bars, score circles, rankings

---

## 🔬 Technical Highlights for Portfolio

### NLP Expertise Demonstrated
✅ **Text Classification** - Zero-shot learning with BERT  
✅ **Named Entity Recognition** - spaCy statistical models  
✅ **Semantic Analysis** - Sentence embeddings and similarity  
✅ **Feature Engineering** - Linguistic feature extraction  
✅ **Model Integration** - Multiple transformer models  
✅ **Evaluation Metrics** - ROUGE, coherence, custom scoring

### Prompt Engineering Expertise
✅ **Template Design** - Intent-specific templates  
✅ **Few-Shot Prompting** - Example-based learning  
✅ **Chain-of-Thought** - Structured reasoning  
✅ **Role Assignment** - Expert persona injection  
✅ **Output Evaluation** - Quality assessment and ranking  
✅ **Best Practices** - Industry-standard techniques

### Software Engineering
✅ **RESTful API Design** - Clean, documented endpoints  
✅ **Async Programming** - FastAPI async/await  
✅ **Error Handling** - Comprehensive error management  
✅ **Code Organization** - Modular, maintainable structure  
✅ **Modern Frontend** - React with hooks  
✅ **Responsive Design** - Mobile-first approach

---

## 📈 Future Enhancements

- [ ] User authentication and prompt history
- [ ] Fine-tuned models for domain-specific optimization
- [ ] A/B testing framework for prompts
- [ ] Multi-language support
- [ ] Prompt template library
- [ ] Chrome extension for on-the-fly optimization
- [ ] Integration with popular AI platforms
- [ ] Advanced analytics dashboard

---

## 🤝 Contributing

This is a portfolio project, but feedback and suggestions are welcome! Feel free to:
- Report issues
- Suggest new features
- Propose improvements

---

## 📝 License

MIT License - Feel free to use this project as inspiration for your own work!

---

## 👨‍💻 Author

**Your Name**  
NLP Engineer | AI Enthusiast | Portfolio Project

**Skills Demonstrated:**
- Natural Language Processing
- Prompt Engineering
- Machine Learning
- Full-Stack Development
- Python & JavaScript
- API Development
- UI/UX Design

---

## 🙏 Acknowledgments

- **HuggingFace** - Transformers library and pre-trained models
- **spaCy** - Excellent NLP library
- **FastAPI** - Modern Python web framework
- **React** - UI framework
- **Anthropic** - Claude API (optional integration)
- **OpenAI** - GPT API (optional integration)

---

## 📞 Contact

For questions or collaboration opportunities:
- Email: your.email@example.com
- LinkedIn: [Your LinkedIn]
- GitHub: [Your GitHub]
- Portfolio: [Your Portfolio]

---

**Made with ❤️ and lots of ☕ | Showcasing NLP + Prompt Engineering**

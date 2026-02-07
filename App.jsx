import React, { useState } from 'react';
import './styles/App.css';
import PromptAnalyzer from './components/PromptAnalyzer';
import OptimizedResults from './components/OptimizedResults';
import Header from './components/Header';
import LoadingAnimation from './components/LoadingAnimation';
import { analyzePrompt, optimizeAndEvaluate } from './services/api';

function App() {
  const [prompt, setPrompt] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('analyze');

  const handleAnalyze = async () => {
    if (!prompt.trim()) {
      setError('Please enter a prompt');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const data = await analyzePrompt(prompt);
      setAnalysis(data);
      setActiveTab('results');
    } catch (err) {
      setError('Failed to analyze prompt: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleOptimize = async () => {
    if (!prompt.trim()) {
      setError('Please enter a prompt');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const data = await optimizeAndEvaluate(prompt, 3);
      setResults(data);
      setAnalysis(data.analysis);
      setActiveTab('results');
    } catch (err) {
      setError('Failed to optimize prompt: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="background-effects">
        <div className="gradient-orb orb-1"></div>
        <div className="gradient-orb orb-2"></div>
        <div className="gradient-orb orb-3"></div>
        <div className="grid-overlay"></div>
      </div>

      <Header />

      <main className="main-content">
        <div className="container">
          
          {/* Hero Section */}
          <div className="hero-section">
            <div className="hero-badge">
              <span className="badge-icon">⚡</span>
              <span>NLP-Powered Prompt Engineering</span>
            </div>
            <h1 className="hero-title">
              Transform Your Prompts with
              <span className="gradient-text"> AI Intelligence</span>
            </h1>
            <p className="hero-description">
              Advanced NLP analysis and optimization to craft perfect prompts every time.
              Leveraging state-of-the-art transformers, semantic analysis, and prompt engineering.
            </p>
          </div>

          {/* Main Input Area */}
          <div className="input-section">
            <div className="input-wrapper">
              <label htmlFor="prompt-input" className="input-label">
                Your Prompt
                <span className="label-hint">Enter any prompt to analyze and optimize</span>
              </label>
              <textarea
                id="prompt-input"
                className="prompt-textarea"
                placeholder="e.g., Write about artificial intelligence..."
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                rows={6}
              />
              <div className="input-stats">
                <span className="stat-item">
                  {prompt.split(/\s+/).filter(w => w).length} words
                </span>
                <span className="stat-item">
                  {prompt.length} characters
                </span>
              </div>
            </div>

            <div className="action-buttons">
              <button 
                className="btn btn-secondary"
                onClick={handleAnalyze}
                disabled={loading}
              >
                <span className="btn-icon">🔍</span>
                Analyze Only
              </button>
              <button 
                className="btn btn-primary"
                onClick={handleOptimize}
                disabled={loading}
              >
                <span className="btn-icon">✨</span>
                Analyze & Optimize
              </button>
            </div>

            {error && (
              <div className="error-message">
                <span className="error-icon">⚠️</span>
                {error}
              </div>
            )}
          </div>

          {/* Loading State */}
          {loading && <LoadingAnimation />}

          {/* Results Section */}
          {!loading && (analysis || results) && (
            <div className="results-section">
              <PromptAnalyzer analysis={analysis} />
              {results && (
                <OptimizedResults 
                  results={results}
                  originalPrompt={prompt}
                />
              )}
            </div>
          )}

          {/* Features Section */}
          {!analysis && !results && !loading && (
            <div className="features-grid">
              <div className="feature-card">
                <div className="feature-icon">🧠</div>
                <h3 className="feature-title">Intent Classification</h3>
                <p className="feature-description">
                  BERT-based zero-shot classification to understand what you're trying to achieve
                </p>
              </div>
              <div className="feature-card">
                <div className="feature-icon">🏷️</div>
                <h3 className="feature-title">Entity Recognition</h3>
                <p className="feature-description">
                  spaCy NER to extract key entities, topics, and contextual information
                </p>
              </div>
              <div className="feature-card">
                <div className="feature-icon">📊</div>
                <h3 className="feature-title">Quality Assessment</h3>
                <p className="feature-description">
                  Linguistic analysis to score prompt clarity, specificity, and effectiveness
                </p>
              </div>
              <div className="feature-card">
                <div className="feature-icon">🎯</div>
                <h3 className="feature-title">Smart Optimization</h3>
                <p className="feature-description">
                  Template-based enhancement with advanced prompt engineering techniques
                </p>
              </div>
              <div className="feature-card">
                <div className="feature-icon">⚖️</div>
                <h3 className="feature-title">Output Evaluation</h3>
                <p className="feature-description">
                  Semantic similarity and coherence scoring to rank optimized variants
                </p>
              </div>
              <div className="feature-card">
                <div className="feature-icon">💡</div>
                <h3 className="feature-title">Learning System</h3>
                <p className="feature-description">
                  Builds knowledge base of successful patterns and best practices
                </p>
              </div>
            </div>
          )}
        </div>
      </main>

      <footer className="footer">
        <div className="container">
          <div className="footer-content">
            <div className="footer-info">
              <span className="footer-brand">PromptGenius</span>
              <span className="footer-description">NLP & Prompt Engineering Portfolio Project</span>
            </div>
            <div className="footer-tech">
              <span className="tech-badge">React</span>
              <span className="tech-badge">FastAPI</span>
              <span className="tech-badge">Transformers</span>
              <span className="tech-badge">spaCy</span>
              <span className="tech-badge">BERT</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;

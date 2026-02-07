import React, { useState } from 'react';
import '../styles/OptimizedResults.css';

function OptimizedResults({ results, originalPrompt }) {
  const [selectedPrompt, setSelectedPrompt] = useState(null);
  const [compareMode, setCompareMode] = useState(false);

  if (!results || !results.optimized_prompts) return null;

  const handleSelectPrompt = (prompt) => {
    setSelectedPrompt(selectedPrompt === prompt ? null : prompt);
  };

  return (
    <div className="optimized-container">
      <div className="optimized-header">
        <h2 className="optimized-title">
          <span className="title-icon">✨</span>
          Optimized Prompts
        </h2>
        {results.best_prompt && (
          <div className="best-badge">
            <span className="badge-icon">👑</span>
            Best Prompt Identified
          </div>
        )}
      </div>

      <div className="prompts-grid">
        
        {/* Original Prompt */}
        <div className="prompt-card original-card">
          <div className="prompt-header">
            <h3 className="prompt-type">Original Prompt</h3>
            <span className="prompt-badge baseline">Baseline</span>
          </div>
          <div className="prompt-content">
            <p className="prompt-text">{originalPrompt}</p>
          </div>
        </div>

        {/* Optimized Prompts */}
        {results.optimized_prompts.map((opt, idx) => {
          const isBest = results.best_prompt === opt.optimized;
          const evaluation = results.evaluations?.find(e => e.prompt === opt.optimized);
          
          return (
            <div 
              key={idx} 
              className={`prompt-card ${isBest ? 'best-card' : ''} ${selectedPrompt === opt ? 'selected' : ''}`}
              onClick={() => handleSelectPrompt(opt)}
            >
              <div className="prompt-header">
                <h3 className="prompt-type">{opt.technique}</h3>
                <div className="prompt-badges">
                  {isBest && <span className="prompt-badge best">👑 Best</span>}
                  <span className="prompt-badge">
                    +{Math.round(opt.expected_improvement * 100)}%
                  </span>
                </div>
              </div>
              
              <div className="prompt-content">
                <p className="prompt-text">{opt.optimized}</p>
              </div>

              {/* Improvements List */}
              <div className="improvements-section">
                <h4 className="improvements-title">Improvements Applied:</h4>
                <div className="improvements-tags">
                  {opt.improvements.map((imp, i) => (
                    <span key={i} className="improvement-tag">
                      ✓ {imp}
                    </span>
                  ))}
                </div>
              </div>

              {/* Evaluation Scores */}
              {evaluation && (
                <div className="scores-section">
                  <h4 className="scores-title">Evaluation Scores:</h4>
                  <div className="scores-grid">
                    <div className="score-item">
                      <span className="score-label">Relevance</span>
                      <div className="score-bar-container">
                        <div 
                          className="score-bar"
                          style={{ width: `${evaluation.scores.relevance * 100}%` }}
                        />
                      </div>
                      <span className="score-value">
                        {(evaluation.scores.relevance * 100).toFixed(0)}%
                      </span>
                    </div>
                    <div className="score-item">
                      <span className="score-label">Completeness</span>
                      <div className="score-bar-container">
                        <div 
                          className="score-bar"
                          style={{ width: `${evaluation.scores.completeness * 100}%` }}
                        />
                      </div>
                      <span className="score-value">
                        {(evaluation.scores.completeness * 100).toFixed(0)}%
                      </span>
                    </div>
                    <div className="score-item">
                      <span className="score-label">Coherence</span>
                      <div className="score-bar-container">
                        <div 
                          className="score-bar"
                          style={{ width: `${evaluation.scores.coherence * 100}%` }}
                        />
                      </div>
                      <span className="score-value">
                        {(evaluation.scores.coherence * 100).toFixed(0)}%
                      </span>
                    </div>
                    <div className="score-item overall-score">
                      <span className="score-label">Overall</span>
                      <div className="score-bar-container">
                        <div 
                          className="score-bar overall-bar"
                          style={{ width: `${evaluation.scores.overall * 100}%` }}
                        />
                      </div>
                      <span className="score-value highlight">
                        {(evaluation.scores.overall * 100).toFixed(0)}%
                      </span>
                    </div>
                  </div>
                  
                  {/* Rank Badge */}
                  <div className="rank-badge">
                    Rank #{evaluation.rank}
                  </div>
                </div>
              )}

              {/* Expand indicator */}
              <div className="expand-indicator">
                Click to {selectedPrompt === opt ? 'collapse' : 'expand'}
              </div>
            </div>
          );
        })}
      </div>

      {/* Tips Section */}
      <div className="tips-section">
        <div className="tips-card">
          <h3 className="tips-title">
            <span className="tips-icon">💡</span>
            Prompt Engineering Tips
          </h3>
          <ul className="tips-list">
            <li>Be specific about your desired output format and length</li>
            <li>Include context about your audience and purpose</li>
            <li>Use examples to demonstrate the style you want</li>
            <li>Break complex tasks into step-by-step instructions</li>
            <li>Specify constraints and quality criteria upfront</li>
            <li>Assign expert roles for domain-specific tasks</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default OptimizedResults;

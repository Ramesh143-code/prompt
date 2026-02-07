import React from 'react';
import '../styles/PromptAnalyzer.css';

function PromptAnalyzer({ analysis }) {
  if (!analysis) return null;

  const getQualityColor = (score) => {
    if (score >= 80) return '#10b981';
    if (score >= 60) return '#f59e0b';
    return '#ef4444';
  };

  const getConfidenceBar = (confidence) => {
    return Math.round(confidence * 100);
  };

  return (
    <div className="analyzer-container">
      <div className="analyzer-header">
        <h2 className="analyzer-title">
          <span className="title-icon">🔍</span>
          NLP Analysis Results
        </h2>
      </div>

      <div className="analysis-grid">
        
        {/* Quality Score Card */}
        <div className="analysis-card quality-card">
          <div className="card-header">
            <h3 className="card-title">Quality Score</h3>
            <span className="card-icon">📊</span>
          </div>
          <div className="quality-score">
            <div 
              className="score-circle"
              style={{ '--score-color': getQualityColor(analysis.quality_score) }}
            >
              <svg width="120" height="120">
                <circle
                  cx="60"
                  cy="60"
                  r="50"
                  fill="none"
                  stroke="rgba(148, 163, 184, 0.2)"
                  strokeWidth="10"
                />
                <circle
                  cx="60"
                  cy="60"
                  r="50"
                  fill="none"
                  stroke={getQualityColor(analysis.quality_score)}
                  strokeWidth="10"
                  strokeDasharray={`${analysis.quality_score * 3.14} 314`}
                  strokeLinecap="round"
                  transform="rotate(-90 60 60)"
                  className="score-progress"
                />
              </svg>
              <div className="score-value">
                {analysis.quality_score}
                <span className="score-unit">/100</span>
              </div>
            </div>
          </div>
          {analysis.issues && analysis.issues.length > 0 && (
            <div className="issues-list">
              <h4 className="issues-title">Issues Found:</h4>
              {analysis.issues.map((issue, idx) => (
                <div key={idx} className="issue-item">
                  <span className="issue-icon">⚠️</span>
                  {issue}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Intent Classification Card */}
        <div className="analysis-card">
          <div className="card-header">
            <h3 className="card-title">Intent Classification</h3>
            <span className="card-icon">🧠</span>
          </div>
          <div className="intent-result">
            <div className="intent-label">{analysis.intent}</div>
            <div className="confidence-bar">
              <div 
                className="confidence-fill"
                style={{ width: `${getConfidenceBar(analysis.intent_confidence)}%` }}
              />
            </div>
            <div className="confidence-text">
              {getConfidenceBar(analysis.intent_confidence)}% confidence
            </div>
          </div>
          <div className="meta-info">
            <div className="meta-item">
              <span className="meta-label">Domain:</span>
              <span className="meta-value">{analysis.domain}</span>
            </div>
            <div className="meta-item">
              <span className="meta-label">Complexity:</span>
              <span className="meta-value">{analysis.complexity}</span>
            </div>
            <div className="meta-item">
              <span className="meta-label">Sentiment:</span>
              <span className="meta-value">{analysis.sentiment}</span>
            </div>
          </div>
        </div>

        {/* Entities Card */}
        {analysis.entities && analysis.entities.length > 0 && (
          <div className="analysis-card">
            <div className="card-header">
              <h3 className="card-title">Extracted Entities</h3>
              <span className="card-icon">🏷️</span>
            </div>
            <div className="entities-list">
              {analysis.entities.map((entity, idx) => (
                <div key={idx} className="entity-tag">
                  <span className="entity-text">{entity.text}</span>
                  <span className="entity-label">{entity.label}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Suggestions Card */}
        {analysis.suggestions && analysis.suggestions.length > 0 && (
          <div className="analysis-card suggestions-card">
            <div className="card-header">
              <h3 className="card-title">Improvement Suggestions</h3>
              <span className="card-icon">💡</span>
            </div>
            <div className="suggestions-list">
              {analysis.suggestions.map((suggestion, idx) => (
                <div key={idx} className="suggestion-item">
                  <span className="suggestion-bullet">→</span>
                  {suggestion}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default PromptAnalyzer;

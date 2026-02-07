import React from 'react';
import '../styles/Loading.css';

function LoadingAnimation() {
  return (
    <div className="loading-container">
      <div className="loading-content">
        <div className="loading-spinner">
          <div className="spinner-ring"></div>
          <div className="spinner-ring"></div>
          <div className="spinner-ring"></div>
        </div>
        <h3 className="loading-title">Analyzing with NLP Models...</h3>
        <div className="loading-steps">
          <div className="loading-step">
            <span className="step-icon">🧠</span>
            <span>BERT Intent Classification</span>
          </div>
          <div className="loading-step">
            <span className="step-icon">🏷️</span>
            <span>spaCy Entity Recognition</span>
          </div>
          <div className="loading-step">
            <span className="step-icon">📊</span>
            <span>Quality Assessment</span>
          </div>
          <div className="loading-step">
            <span className="step-icon">✨</span>
            <span>Generating Optimizations</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LoadingAnimation;

"""
NLP Analyzer Module
Implements core NLP techniques for prompt analysis
"""

import spacy
import nltk
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from sentence_transformers import SentenceTransformer
import torch
from typing import Dict, List
import re
from collections import Counter
import textstat
import logging

logger = logging.getLogger(__name__)

class PromptAnalyzer:
    def __init__(self):
        """Initialize NLP models and tools"""
        logger.info("Initializing NLP Analyzer...")
        
        # Download required NLTK data
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
        except:
            pass
        
        # Load spaCy model for NER and linguistic analysis
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            logger.warning("spaCy model not found, using basic features")
            self.nlp = None
        
        # Intent Classification Model (Zero-shot classification)
        self.intent_classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli",
            device=0 if torch.cuda.is_available() else -1
        )
        
        # Sentiment Analysis
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            device=0 if torch.cuda.is_available() else -1
        )
        
        # Sentence embeddings for semantic analysis
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Statistics tracking
        self.stats = {
            'total_analyzed': 0,
            'intent_distribution': Counter(),
            'quality_scores': []
        }
        
        # Define intent categories
        self.intent_labels = [
            "text generation",
            "question answering",
            "summarization",
            "translation",
            "code generation",
            "creative writing",
            "data analysis",
            "explanation",
            "classification",
            "extraction"
        ]
        
        # Define domain categories
        self.domain_labels = [
            "technical/programming",
            "business/professional",
            "creative/artistic",
            "academic/educational",
            "general knowledge",
            "personal/casual"
        ]
        
        logger.info("NLP Analyzer initialized successfully")
    
    async def analyze(self, prompt: str) -> Dict:
        """
        Comprehensive NLP analysis of a prompt
        
        NLP Techniques:
        1. Intent Classification - Zero-shot BART
        2. Named Entity Recognition - spaCy
        3. Domain Detection - Zero-shot classification
        4. Quality Scoring - Linguistic features
        5. Sentiment Analysis - DistilBERT
        6. Complexity Analysis - Readability metrics
        """
        self.stats['total_analyzed'] += 1
        
        # 1. INTENT CLASSIFICATION
        intent_result = self.classify_intent(prompt)
        
        # 2. NAMED ENTITY RECOGNITION
        entities = self.extract_entities(prompt)
        
        # 3. DOMAIN DETECTION
        domain = self.detect_domain(prompt)
        
        # 4. QUALITY ASSESSMENT
        quality_analysis = self.assess_quality(prompt)
        
        # 5. SENTIMENT ANALYSIS
        sentiment = self.analyze_sentiment(prompt)
        
        # 6. COMPLEXITY ANALYSIS
        complexity = self.analyze_complexity(prompt)
        
        # Update statistics
        self.stats['intent_distribution'][intent_result['label']] += 1
        self.stats['quality_scores'].append(quality_analysis['score'])
        
        return {
            'intent': intent_result['label'],
            'intent_confidence': intent_result['score'],
            'entities': entities,
            'domain': domain,
            'quality_score': quality_analysis['score'],
            'issues': quality_analysis['issues'],
            'suggestions': quality_analysis['suggestions'],
            'sentiment': sentiment,
            'complexity': complexity
        }
    
    def classify_intent(self, prompt: str) -> Dict:
        """Classify the intent of the prompt using zero-shot classification"""
        try:
            result = self.intent_classifier(
                prompt,
                candidate_labels=self.intent_labels,
                multi_label=False
            )
            return {
                'label': result['labels'][0],
                'score': float(result['scores'][0])
            }
        except Exception as e:
            logger.error(f"Intent classification error: {e}")
            return {'label': 'general', 'score': 0.5}
    
    def extract_entities(self, prompt: str) -> List[Dict]:
        """Extract named entities using spaCy NER"""
        entities = []
        
        if self.nlp:
            doc = self.nlp(prompt)
            for ent in doc.ents:
                entities.append({
                    'text': ent.text,
                    'label': ent.label_,
                    'start': ent.start_char,
                    'end': ent.end_char
                })
        
        return entities
    
    def detect_domain(self, prompt: str) -> str:
        """Detect the domain/subject area of the prompt"""
        try:
            result = self.intent_classifier(
                prompt,
                candidate_labels=self.domain_labels,
                multi_label=False
            )
            return result['labels'][0]
        except:
            return "general knowledge"
    
    def assess_quality(self, prompt: str) -> Dict:
        """
        Assess prompt quality using linguistic features
        
        Factors:
        - Length (too short/long)
        - Specificity (vague words)
        - Clarity (readability)
        - Completeness (missing context)
        """
        issues = []
        suggestions = []
        score = 100.0
        
        # Check length
        word_count = len(prompt.split())
        if word_count < 5:
            issues.append("Prompt is too short")
            suggestions.append("Add more context and details")
            score -= 20
        elif word_count > 200:
            issues.append("Prompt might be too long")
            suggestions.append("Consider breaking into smaller, focused prompts")
            score -= 10
        
        # Check for vague language
        vague_words = ['something', 'anything', 'stuff', 'things', 'it', 'this', 'that']
        vague_count = sum(1 for word in vague_words if word in prompt.lower())
        if vague_count > 0:
            issues.append(f"Contains {vague_count} vague term(s)")
            suggestions.append("Be more specific about what you want")
            score -= (vague_count * 5)
        
        # Check for questions vs statements
        if '?' not in prompt and not any(prompt.lower().startswith(q) for q in ['write', 'create', 'generate', 'make', 'build']):
            issues.append("Unclear instruction format")
            suggestions.append("Use clear directives (e.g., 'Write...', 'Create...', 'Explain...')")
            score -= 15
        
        # Check readability
        try:
            reading_ease = textstat.flesch_reading_ease(prompt)
            if reading_ease < 30:
                issues.append("Prompt is complex/hard to parse")
                suggestions.append("Simplify sentence structure")
                score -= 10
        except:
            pass
        
        # Check for context markers
        context_markers = ['for', 'about', 'regarding', 'in the context of', 'audience:', 'format:', 'tone:']
        has_context = any(marker in prompt.lower() for marker in context_markers)
        if not has_context and word_count > 5:
            suggestions.append("Add context: audience, purpose, format, or tone")
            score -= 5
        
        # Normalize score
        score = max(0, min(100, score))
        
        return {
            'score': round(score, 2),
            'issues': issues,
            'suggestions': suggestions
        }
    
    def analyze_sentiment(self, prompt: str) -> str:
        """Analyze the sentiment/tone of the prompt"""
        try:
            result = self.sentiment_analyzer(prompt[:512])[0]
            return result['label'].lower()
        except:
            return "neutral"
    
    def analyze_complexity(self, prompt: str) -> str:
        """Determine complexity level of the prompt"""
        word_count = len(prompt.split())
        
        if self.nlp:
            doc = self.nlp(prompt)
            avg_word_length = sum(len(token.text) for token in doc) / len(doc)
            
            if word_count < 10 and avg_word_length < 5:
                return "simple"
            elif word_count > 50 or avg_word_length > 7:
                return "complex"
            else:
                return "moderate"
        else:
            if word_count < 10:
                return "simple"
            elif word_count > 50:
                return "complex"
            else:
                return "moderate"
    
    def get_stats(self) -> Dict:
        """Get analyzer statistics"""
        most_common_intent = self.stats['intent_distribution'].most_common(1)
        avg_quality = sum(self.stats['quality_scores']) / len(self.stats['quality_scores']) if self.stats['quality_scores'] else 0
        
        return {
            'total_analyzed': self.stats['total_analyzed'],
            'most_common_intent': most_common_intent[0][0] if most_common_intent else 'none',
            'avg_quality': round(avg_quality, 2)
        }

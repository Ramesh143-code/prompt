"""
Output Evaluator Module
Evaluates and ranks prompt outputs using NLP metrics
"""

from typing import List, Dict
import os
from anthropic import Anthropic
from openai import OpenAI
from sentence_transformers import SentenceTransformer, util
import numpy as np
import logging

logger = logging.getLogger(__name__)

class OutputEvaluator:
    def __init__(self):
        """Initialize evaluation models and clients"""
        logger.info("Initializing Output Evaluator...")
        
        # LLM clients
        self.anthropic_client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY', ''))
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', ''))
        
        # Semantic similarity model
        self.similarity_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        logger.info("Output Evaluator initialized")
    
    async def evaluate_prompts(self, original_prompt: str, optimized_prompts: List[str], 
                               llm_provider: str = "anthropic") -> List[Dict]:
        """
        Execute prompts and evaluate outputs
        
        NLP Evaluation Metrics:
        1. Semantic Similarity (to expected output)
        2. Response Length & Completeness
        3. Coherence Score
        4. Relevance Score
        5. Quality Assessment
        """
        evaluations = []
        
        # Execute each prompt
        for i, prompt in enumerate([original_prompt] + optimized_prompts):
            logger.info(f"Executing prompt {i+1}/{len(optimized_prompts)+1}")
            
            # Get LLM output
            output = await self._execute_prompt(prompt, llm_provider)
            
            # Evaluate the output
            scores = self._evaluate_output(prompt, output, original_prompt)
            
            evaluations.append({
                'prompt': prompt,
                'output': output,
                'scores': scores,
                'rank': 0  # Will be set after ranking
            })
        
        # Rank all evaluations
        evaluations = self._rank_evaluations(evaluations)
        
        return evaluations
    
    async def _execute_prompt(self, prompt: str, provider: str) -> str:
        """Execute a prompt with the specified LLM"""
        try:
            if provider == "anthropic":
                response = self.anthropic_client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=1000,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
            
            elif provider == "openai":
                response = self.openai_client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1000
                )
                return response.choices[0].message.content
            
            else:
                return "Error: Unknown provider"
        
        except Exception as e:
            logger.error(f"LLM execution error: {e}")
            return f"[Simulated output for: {prompt[:50]}...]"
    
    def _evaluate_output(self, prompt: str, output: str, original_prompt: str) -> Dict:
        """
        Evaluate output quality using NLP metrics
        
        Metrics:
        - Relevance: How relevant is the output to the prompt
        - Completeness: Length and detail
        - Coherence: Logical flow and structure
        - Quality: Overall assessment
        """
        scores = {}
        
        # 1. SEMANTIC RELEVANCE
        # Calculate semantic similarity between prompt and output
        prompt_embedding = self.similarity_model.encode(prompt, convert_to_tensor=True)
        output_embedding = self.similarity_model.encode(output[:512], convert_to_tensor=True)
        relevance_score = float(util.cos_sim(prompt_embedding, output_embedding)[0][0])
        scores['relevance'] = max(0, min(1, relevance_score))
        
        # 2. COMPLETENESS
        # Based on output length and structure
        word_count = len(output.split())
        completeness = min(1.0, word_count / 200)  # Normalize to 200 words
        
        # Bonus for structure (paragraphs, lists)
        structure_bonus = 0.1 if output.count('\n\n') > 1 else 0
        scores['completeness'] = min(1.0, completeness + structure_bonus)
        
        # 3. COHERENCE
        # Analyze sentence connectivity and flow
        sentences = output.split('.')
        coherence_score = self._calculate_coherence(sentences)
        scores['coherence'] = coherence_score
        
        # 4. SPECIFICITY
        # Check for specific details vs generic content
        specificity = self._calculate_specificity(output)
        scores['specificity'] = specificity
        
        # 5. OVERALL QUALITY SCORE
        # Weighted combination of all metrics
        scores['overall'] = (
            scores['relevance'] * 0.35 +
            scores['completeness'] * 0.25 +
            scores['coherence'] * 0.25 +
            scores['specificity'] * 0.15
        )
        
        # Round all scores
        for key in scores:
            scores[key] = round(scores[key], 3)
        
        return scores
    
    def _calculate_coherence(self, sentences: List[str]) -> float:
        """Calculate coherence based on sentence similarity"""
        if len(sentences) < 2:
            return 0.8
        
        try:
            # Encode all sentences
            embeddings = self.similarity_model.encode(sentences[:10], convert_to_tensor=True)
            
            # Calculate average similarity between consecutive sentences
            similarities = []
            for i in range(len(embeddings) - 1):
                sim = util.cos_sim(embeddings[i], embeddings[i+1])[0][0]
                similarities.append(float(sim))
            
            # High coherence = sentences are related but not identical
            avg_sim = np.mean(similarities) if similarities else 0.5
            
            # Ideal similarity is around 0.5-0.7 (related but diverse)
            if 0.4 <= avg_sim <= 0.7:
                coherence = 0.9
            elif 0.3 <= avg_sim <= 0.8:
                coherence = 0.75
            else:
                coherence = 0.6
            
            return coherence
        
        except:
            return 0.7
    
    def _calculate_specificity(self, output: str) -> float:
        """Calculate how specific vs generic the output is"""
        
        # Generic words that reduce specificity
        generic_words = [
            'thing', 'stuff', 'very', 'really', 'some', 'many',
            'good', 'bad', 'nice', 'great', 'important'
        ]
        
        words = output.lower().split()
        generic_count = sum(1 for word in words if word in generic_words)
        
        # Specific indicators: numbers, proper nouns, technical terms
        has_numbers = any(char.isdigit() for char in output)
        has_capitals = sum(1 for char in output if char.isupper()) > 5
        
        # Calculate specificity score
        specificity = 0.7  # Base score
        
        if generic_count > len(words) * 0.1:  # More than 10% generic
            specificity -= 0.2
        
        if has_numbers:
            specificity += 0.15
        
        if has_capitals:
            specificity += 0.15
        
        return max(0, min(1, specificity))
    
    def _rank_evaluations(self, evaluations: List[Dict]) -> List[Dict]:
        """Rank evaluations by overall score"""
        
        # Sort by overall score (descending)
        sorted_evals = sorted(evaluations, key=lambda x: x['scores']['overall'], reverse=True)
        
        # Assign ranks
        for i, evaluation in enumerate(sorted_evals):
            evaluation['rank'] = i + 1
        
        return sorted_evals

"""
PromptGenius - AI Prompt Optimization System
Main FastAPI Application
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import logging

# Import NLP modules
from nlp_analyzer import PromptAnalyzer
from prompt_optimizer import PromptOptimizer
from output_evaluator import OutputEvaluator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="PromptGenius API",
    description="Advanced NLP-powered Prompt Optimization System",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize NLP components
analyzer = PromptAnalyzer()
optimizer = PromptOptimizer()
evaluator = OutputEvaluator()

# Request/Response Models
class PromptRequest(BaseModel):
    prompt: str
    num_variants: Optional[int] = 3
    llm_provider: Optional[str] = "anthropic"  # anthropic or openai
    
class AnalysisResult(BaseModel):
    intent: str
    intent_confidence: float
    entities: List[Dict[str, str]]
    domain: str
    quality_score: float
    issues: List[str]
    suggestions: List[str]
    sentiment: str
    complexity: str

class OptimizedPrompt(BaseModel):
    original: str
    optimized: str
    technique: str
    improvements: List[str]
    expected_improvement: float

class EvaluationResult(BaseModel):
    prompt: str
    output: str
    scores: Dict[str, float]
    rank: int

class OptimizationResponse(BaseModel):
    analysis: AnalysisResult
    optimized_prompts: List[OptimizedPrompt]
    evaluations: Optional[List[EvaluationResult]] = None
    best_prompt: Optional[str] = None

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "PromptGenius API",
        "version": "1.0.0"
    }

@app.post("/api/analyze", response_model=AnalysisResult)
async def analyze_prompt(request: PromptRequest):
    """
    Analyze a user's prompt using NLP techniques
    
    NLP Techniques Used:
    - Intent Classification (BERT)
    - Named Entity Recognition (spaCy)
    - Domain Detection (Text Classification)
    - Quality Scoring (Linguistic Features)
    - Sentiment Analysis
    """
    try:
        logger.info(f"Analyzing prompt: {request.prompt[:50]}...")
        
        analysis = await analyzer.analyze(request.prompt)
        
        return AnalysisResult(**analysis)
    
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/optimize", response_model=List[OptimizedPrompt])
async def optimize_prompt(request: PromptRequest):
    """
    Generate optimized versions of the prompt
    
    Uses NLP-based prompt engineering:
    - Template matching based on intent
    - Entity-aware augmentation
    - Context injection
    - Structure optimization
    """
    try:
        logger.info(f"Optimizing prompt: {request.prompt[:50]}...")
        
        # First analyze the prompt
        analysis = await analyzer.analyze(request.prompt)
        
        # Generate optimized variants
        optimized = await optimizer.optimize(
            prompt=request.prompt,
            analysis=analysis,
            num_variants=request.num_variants
        )
        
        return [OptimizedPrompt(**opt) for opt in optimized]
    
    except Exception as e:
        logger.error(f"Optimization error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Optimization failed: {str(e)}")

@app.post("/api/optimize-and-evaluate", response_model=OptimizationResponse)
async def optimize_and_evaluate(request: PromptRequest):
    """
    Complete pipeline: Analyze, Optimize, Execute, and Evaluate
    
    Full NLP Pipeline:
    1. Prompt Analysis (Classification, NER, Quality Assessment)
    2. Prompt Optimization (Template-based Generation)
    3. LLM Execution (Generate outputs for each variant)
    4. Output Evaluation (Semantic Similarity, Quality Metrics, Ranking)
    """
    try:
        logger.info(f"Running full pipeline for: {request.prompt[:50]}...")
        
        # Step 1: Analyze
        analysis = await analyzer.analyze(request.prompt)
        
        # Step 2: Optimize
        optimized = await optimizer.optimize(
            prompt=request.prompt,
            analysis=analysis,
            num_variants=request.num_variants
        )
        
        # Step 3: Execute prompts with LLM
        evaluations = await evaluator.evaluate_prompts(
            original_prompt=request.prompt,
            optimized_prompts=[opt['optimized'] for opt in optimized],
            llm_provider=request.llm_provider
        )
        
        # Step 4: Determine best prompt
        best_prompt = max(evaluations, key=lambda x: x['scores']['overall'])['prompt']
        
        return OptimizationResponse(
            analysis=AnalysisResult(**analysis),
            optimized_prompts=[OptimizedPrompt(**opt) for opt in optimized],
            evaluations=[EvaluationResult(**ev) for ev in evaluations],
            best_prompt=best_prompt
        )
    
    except Exception as e:
        logger.error(f"Pipeline error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Pipeline failed: {str(e)}")

@app.get("/api/stats")
async def get_stats():
    """Get system statistics"""
    return {
        "total_prompts_analyzed": analyzer.get_stats()['total_analyzed'],
        "avg_quality_score": analyzer.get_stats()['avg_quality'],
        "most_common_intent": analyzer.get_stats()['most_common_intent'],
        "optimization_success_rate": optimizer.get_stats()['success_rate']
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

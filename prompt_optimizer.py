"""
Prompt Optimizer Module
Generates improved prompt versions using NLP and prompt engineering techniques
"""

from typing import List, Dict
import re
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

class PromptOptimizer:
    def __init__(self):
        """Initialize prompt optimization engine"""
        logger.info("Initializing Prompt Optimizer...")
        
        # Prompt engineering templates by intent
        self.templates = {
            "text generation": [
                {
                    "name": "Structured Generation",
                    "template": "Write a {length} {format} about {topic}. Target audience: {audience}. Tone: {tone}. Include: {elements}.",
                    "improvements": ["Added structure", "Specified length", "Defined audience", "Set tone"]
                },
                {
                    "name": "Few-Shot with Examples",
                    "template": "Generate {output_type} about {topic}.\n\nExample 1: [Insert example]\nExample 2: [Insert example]\n\nNow create one about {topic} with similar style.",
                    "improvements": ["Added examples", "Defined output type", "Clear style guidance"]
                },
                {
                    "name": "Chain-of-Thought",
                    "template": "Let's create {output} about {topic}. First, outline the key points. Then, elaborate on each point with details. Finally, write a cohesive {format}.",
                    "improvements": ["Step-by-step process", "Structured thinking", "Clear progression"]
                }
            ],
            "question answering": [
                {
                    "name": "Contextual Q&A",
                    "template": "Context: {context}\n\nQuestion: {question}\n\nProvide a detailed answer with supporting evidence and examples.",
                    "improvements": ["Added context", "Request for evidence", "Clear structure"]
                },
                {
                    "name": "Expert Role",
                    "template": "You are a {expert_role} with expertise in {domain}. Answer this question: {question}. Provide a comprehensive response with technical details and practical examples.",
                    "improvements": ["Assigned expert role", "Domain specification", "Quality criteria"]
                }
            ],
            "summarization": [
                {
                    "name": "Structured Summary",
                    "template": "Summarize the following in {length}: {content}\n\nInclude:\n- Main points\n- Key takeaways\n- Important details\n\nFormat: {format}",
                    "improvements": ["Specified length", "Clear components", "Defined format"]
                },
                {
                    "name": "Audience-Targeted Summary",
                    "template": "Create a summary of {content} for {audience}. Focus on {focus_areas}. Keep it {tone} and {length}.",
                    "improvements": ["Target audience", "Focus areas", "Tone specification"]
                }
            ],
            "code generation": [
                {
                    "name": "Detailed Code Request",
                    "template": "Write {language} code to {task}.\n\nRequirements:\n- {requirement_1}\n- {requirement_2}\n\nInclude comments and handle edge cases.",
                    "improvements": ["Language specified", "Requirements listed", "Quality standards"]
                },
                {
                    "name": "Test-Driven",
                    "template": "Create {language} code for {task}. First, write test cases. Then implement the solution. Include error handling and documentation.",
                    "improvements": ["Test-driven approach", "Error handling", "Documentation required"]
                }
            ],
            "creative writing": [
                {
                    "name": "Detailed Creative Brief",
                    "template": "Write a {format} about {topic}.\n\nGenre: {genre}\nTone: {tone}\nLength: {length}\nKey elements: {elements}\nTarget audience: {audience}",
                    "improvements": ["Genre specified", "Tone defined", "Key elements listed"]
                },
                {
                    "name": "Story Structure",
                    "template": "Create a {format} with:\n- Setting: {setting}\n- Characters: {characters}\n- Conflict: {conflict}\n- Theme: {theme}\nStyle: {style}",
                    "improvements": ["Structural elements", "Character definition", "Theme clarity"]
                }
            ],
            "explanation": [
                {
                    "name": "ELI5 Format",
                    "template": "Explain {topic} as if I'm {level}. Use analogies, simple language, and examples from {domain}.",
                    "improvements": ["Audience level", "Analogy request", "Relatable examples"]
                },
                {
                    "name": "Progressive Depth",
                    "template": "Explain {topic} in three levels:\n1. Simple overview (2-3 sentences)\n2. Detailed explanation with examples\n3. Advanced concepts and implications",
                    "improvements": ["Layered complexity", "Progressive detail", "Comprehensive coverage"]
                }
            ]
        }
        
        # Default general template
        self.default_templates = [
            {
                "name": "Comprehensive Instruction",
                "template": "{action} about {topic}. Provide {detail_level} information. Format: {format}. Consider {considerations}.",
                "improvements": ["Clear action", "Detail specification", "Format defined"]
            }
        ]
        
        # Statistics
        self.stats = {
            'total_optimized': 0,
            'success_count': 0
        }
        
        logger.info("Prompt Optimizer initialized")
    
    async def optimize(self, prompt: str, analysis: Dict, num_variants: int = 3) -> List[Dict]:
        """
        Generate optimized prompt variants
        
        Strategies:
        1. Template-based enhancement (intent-specific)
        2. Entity-aware augmentation
        3. Context injection
        4. Structure optimization
        """
        self.stats['total_optimized'] += 1
        
        optimized_prompts = []
        intent = analysis['intent']
        entities = analysis['entities']
        
        # Get relevant templates
        templates = self.templates.get(intent, self.default_templates)
        
        # Strategy 1: Template-based optimization
        for i, template_config in enumerate(templates[:num_variants]):
            optimized = self._apply_template(
                prompt=prompt,
                template_config=template_config,
                analysis=analysis
            )
            optimized_prompts.append(optimized)
        
        # If we need more variants, add custom strategies
        while len(optimized_prompts) < num_variants:
            if len(optimized_prompts) == 1:
                # Strategy 2: Add explicit constraints
                optimized = self._add_constraints(prompt, analysis)
            elif len(optimized_prompts) == 2:
                # Strategy 3: Add role-playing
                optimized = self._add_role_playing(prompt, analysis)
            else:
                # Strategy 4: Add chain-of-thought
                optimized = self._add_chain_of_thought(prompt, analysis)
            
            optimized_prompts.append(optimized)
        
        self.stats['success_count'] += 1
        
        return optimized_prompts[:num_variants]
    
    def _apply_template(self, prompt: str, template_config: Dict, analysis: Dict) -> Dict:
        """Apply a prompt engineering template"""
        
        # Extract key information from original prompt
        extracted = self._extract_prompt_info(prompt, analysis)
        
        # Build optimized prompt using template
        template = template_config['template']
        
        # Fill in template placeholders with extracted info or defaults
        optimized = template.format(
            topic=extracted.get('topic', 'the subject'),
            format=extracted.get('format', 'detailed response'),
            length=extracted.get('length', 'comprehensive'),
            tone=extracted.get('tone', 'professional'),
            audience=extracted.get('audience', 'general audience'),
            elements=extracted.get('elements', 'key information'),
            action=extracted.get('action', 'write'),
            detail_level=extracted.get('detail_level', 'detailed'),
            considerations=extracted.get('considerations', 'accuracy and clarity'),
            output_type=extracted.get('output_type', 'content'),
            output=extracted.get('output', 'content'),
            context=extracted.get('context', ''),
            question=extracted.get('question', prompt),
            expert_role=extracted.get('expert_role', 'expert'),
            domain=analysis.get('domain', 'this field'),
            content=prompt,
            focus_areas=extracted.get('focus_areas', 'main points'),
            language=extracted.get('language', 'Python'),
            task=extracted.get('task', 'the requested functionality'),
            requirement_1=extracted.get('requirement_1', 'clean code'),
            requirement_2=extracted.get('requirement_2', 'proper documentation'),
            genre=extracted.get('genre', 'general'),
            setting=extracted.get('setting', 'relevant setting'),
            characters=extracted.get('characters', 'appropriate characters'),
            conflict=extracted.get('conflict', 'interesting conflict'),
            theme=extracted.get('theme', 'meaningful theme'),
            style=extracted.get('style', 'engaging'),
            level=extracted.get('level', 'a beginner')
        )
        
        # Calculate expected improvement
        improvement_score = self._calculate_improvement(prompt, optimized)
        
        return {
            'original': prompt,
            'optimized': optimized,
            'technique': template_config['name'],
            'improvements': template_config['improvements'],
            'expected_improvement': improvement_score
        }
    
    def _extract_prompt_info(self, prompt: str, analysis: Dict) -> Dict:
        """Extract key information from the original prompt"""
        info = {}
        
        # Extract topic (use entities if available)
        if analysis.get('entities'):
            topics = [ent['text'] for ent in analysis['entities']]
            info['topic'] = ', '.join(topics) if topics else 'the given topic'
        else:
            # Simple extraction: take first few meaningful words
            words = [w for w in prompt.split() if len(w) > 3]
            info['topic'] = ' '.join(words[:3]) if words else 'the topic'
        
        # Detect action verbs
        action_words = ['write', 'create', 'generate', 'explain', 'summarize', 'analyze', 'describe']
        for action in action_words:
            if action in prompt.lower():
                info['action'] = action
                break
        
        # Detect format mentions
        formats = ['essay', 'article', 'report', 'summary', 'email', 'code', 'story', 'poem']
        for fmt in formats:
            if fmt in prompt.lower():
                info['format'] = fmt
                break
        
        # Extract length if mentioned
        length_patterns = [r'(\d+)\s*words?', r'(\d+)\s*pages?', r'short', r'long', r'brief']
        for pattern in length_patterns:
            match = re.search(pattern, prompt.lower())
            if match:
                info['length'] = match.group(0)
                break
        
        return info
    
    def _add_constraints(self, prompt: str, analysis: Dict) -> Dict:
        """Add explicit constraints and requirements"""
        optimized = f"""{prompt}

Requirements:
- Length: [Specify appropriate length]
- Format: [Specify format]
- Tone: {analysis.get('sentiment', 'professional')}
- Include specific examples and evidence
- Structure the response clearly"""
        
        return {
            'original': prompt,
            'optimized': optimized,
            'technique': 'Constraint-Based Enhancement',
            'improvements': ['Added explicit requirements', 'Defined structure', 'Quality criteria'],
            'expected_improvement': 0.75
        }
    
    def _add_role_playing(self, prompt: str, analysis: Dict) -> Dict:
        """Add role-playing/persona"""
        domain = analysis.get('domain', 'this field')
        
        optimized = f"""You are an expert in {domain} with 10+ years of experience.

Task: {prompt}

Provide a professional, detailed response drawing from your expertise. Include specific examples and best practices."""
        
        return {
            'original': prompt,
            'optimized': optimized,
            'technique': 'Role-Based Prompting',
            'improvements': ['Assigned expert role', 'Domain context', 'Quality expectations'],
            'expected_improvement': 0.80
        }
    
    def _add_chain_of_thought(self, prompt: str, analysis: Dict) -> Dict:
        """Add chain-of-thought reasoning"""
        optimized = f"""{prompt}

Let's approach this step-by-step:
1. First, identify the key components needed
2. Then, elaborate on each component
3. Finally, synthesize into a comprehensive response

Think through each step carefully before providing your answer."""
        
        return {
            'original': prompt,
            'optimized': optimized,
            'technique': 'Chain-of-Thought Prompting',
            'improvements': ['Step-by-step reasoning', 'Structured thinking', 'Careful consideration'],
            'expected_improvement': 0.85
        }
    
    def _calculate_improvement(self, original: str, optimized: str) -> float:
        """Estimate expected improvement score"""
        # Simple heuristic: more detail, structure, and length generally improve prompts
        orig_words = len(original.split())
        opt_words = len(optimized.split())
        
        # Check for added structure (newlines, bullets, numbers)
        structure_bonus = 0.1 if optimized.count('\n') > original.count('\n') else 0
        
        # Length increase (up to a point)
        length_factor = min(opt_words / max(orig_words, 1), 3.0)
        
        # Base score
        score = min(0.5 + (length_factor - 1) * 0.2 + structure_bonus, 0.95)
        
        return round(score, 2)
    
    def get_stats(self) -> Dict:
        """Get optimizer statistics"""
        success_rate = (self.stats['success_count'] / self.stats['total_optimized'] * 100) if self.stats['total_optimized'] > 0 else 0
        
        return {
            'total_optimized': self.stats['total_optimized'],
            'success_rate': round(success_rate, 2)
        }

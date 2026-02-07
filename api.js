/**
 * API Service
 * Handles all communication with the FastAPI backend
 */

const API_BASE_URL = 'http://localhost:8000/api';

class APIError extends Error {
  constructor(message, status) {
    super(message);
    this.status = status;
    this.name = 'APIError';
  }
}

/**
 * Analyze a prompt using NLP techniques
 * @param {string} prompt - The prompt to analyze
 * @returns {Promise<Object>} Analysis results
 */
export async function analyzePrompt(prompt) {
  try {
    const response = await fetch(`${API_BASE_URL}/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new APIError(error.detail || 'Analysis failed', response.status);
    }

    return await response.json();
  } catch (error) {
    if (error instanceof APIError) throw error;
    throw new APIError('Network error: Could not connect to server', 0);
  }
}

/**
 * Optimize a prompt
 * @param {string} prompt - The prompt to optimize
 * @param {number} numVariants - Number of variants to generate
 * @returns {Promise<Object>} Optimization results
 */
export async function optimizePrompt(prompt, numVariants = 3) {
  try {
    const response = await fetch(`${API_BASE_URL}/optimize`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        prompt,
        num_variants: numVariants,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new APIError(error.detail || 'Optimization failed', response.status);
    }

    return await response.json();
  } catch (error) {
    if (error instanceof APIError) throw error;
    throw new APIError('Network error: Could not connect to server', 0);
  }
}

/**
 * Run full pipeline: analyze, optimize, and evaluate
 * @param {string} prompt - The prompt to process
 * @param {number} numVariants - Number of variants to generate
 * @param {string} llmProvider - LLM provider to use ('anthropic' or 'openai')
 * @returns {Promise<Object>} Complete results
 */
export async function optimizeAndEvaluate(prompt, numVariants = 3, llmProvider = 'anthropic') {
  try {
    const response = await fetch(`${API_BASE_URL}/optimize-and-evaluate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        prompt,
        num_variants: numVariants,
        llm_provider: llmProvider,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new APIError(error.detail || 'Pipeline failed', response.status);
    }

    return await response.json();
  } catch (error) {
    if (error instanceof APIError) throw error;
    throw new APIError('Network error: Could not connect to server', 0);
  }
}

/**
 * Get system statistics
 * @returns {Promise<Object>} System stats
 */
export async function getStats() {
  try {
    const response = await fetch(`${API_BASE_URL}/stats`);

    if (!response.ok) {
      throw new APIError('Failed to fetch stats', response.status);
    }

    return await response.json();
  } catch (error) {
    if (error instanceof APIError) throw error;
    throw new APIError('Network error: Could not connect to server', 0);
  }
}

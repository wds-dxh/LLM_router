from .openai import OpenAIEngine

class OllamaEngine(OpenAIEngine):
    """
    Ollama引擎实现
    完全继承OpenAIEngine的实现，因为它们的API完全兼容
    """
    pass

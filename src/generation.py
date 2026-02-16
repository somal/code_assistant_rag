from typing import Dict, List

from openai import OpenAI

prompt_template = '''
You are an expert Ultralytics YOLO code assistant. 
Answer technical questions about YOLO source code using ONLY the provided code chunks.

CONTEXT:
{code_chunks}

USER QUESTION: {question}

INSTRUCTIONS:
1. Reference specific file paths and line numbers
2. Quote relevant code snippets with proper formatting
3. Explain how the code works step-by-step
4. If code is unclear, say what you'd need to see
5. Answer concisely but completely
6. Use markdown for code blocks

RESPONSE FORMAT:
**File: <path>:<line>**
```python
'''


class Generation(object):
    def __init__(self, model_name: str, api_key: str):
        self._model_name = model_name
        self._client = OpenAI(api_key=api_key,
                              base_url="https://openrouter.ai/api/v1",
                              max_retries=5)

    def generate_answer(self, user_request: str, code_chunks: List[Dict]) -> str:
        prompt = prompt_template.format(code_chunks=str(code_chunks),
                                        question=user_request)
        response = self._client.chat.completions.create(
            model=self._model_name,
            messages=[dict(role='system', content=prompt)],
            temperature=0.5,
            max_tokens=1000,
            extra_body={
                "reasoning": {
                    "effort": "minimal"
                }
            },
            stream=False)
        answer = response.choices[0].message.content
        print(answer)
        return answer

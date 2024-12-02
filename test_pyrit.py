import os
import uuid

from pyrit.prompt_target import OllamaChatTarget
from pyrit.models import PromptRequestPiece, PromptRequestResponse, ChatMessageRole

with OllamaChatTarget(
    endpoint="http://127.0.0.1:11434/api/chat",
    model_name="llama3.2",
    ) as target_llm:

    prompt = PromptRequestPiece(role="user", original_prompt_text="Test").to_prompt_request_response()
    
    print(target_llm.send_prompt(prompt_request=prompt))
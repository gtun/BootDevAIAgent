import os
import sys
from openai import OpenAI
from openai.types.chat import ChatCompletion
from dotenv import load_dotenv

TESTING_MODE = "-t" in sys.argv
FAKE_RESPONSE = ChatCompletion.model_validate({
    "id": "gen-fake-123",
    "object": "chat.completion",
    "created": 1759000000,
    "model": "fake/test-model",
    "choices": [
        {
            "index": 0,
            "finish_reason": "stop",
            "message": {
                "role": "assistant",
                "content": "This is a fake response from TESTING_MODE.",
            },
        }
    ],
    "usage": {
        "prompt_tokens": 20,
        "completion_tokens": 10,
        "total_tokens": 30,
    },
})

def main():
    print("Hello from bootdevaiagent!")
    
    load_dotenv()
    
    # Testing mode check
    if TESTING_MODE:
        print("Running in TESTING_MODE. No requests to OpenRouter AI will be made")
    
    if not (api_key := os.environ.get("OPENROUTER_API_KEY")):
        raise RuntimeError("OPENROUTER_API_KEY not set")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    
    response = call_llm(client)
    
    if response.usage:
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
    else:
        raise RuntimeError("no usage data from LLM response")
    print(response.choices[0].message.content)

def call_llm(client):
    if TESTING_MODE:
        return FAKE_RESPONSE
    return client.chat.completions.create(
            model="openrouter/free",
            messages=[
                {
                    "role": "user",
                    "content": "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
                }
            ],
        )


if __name__ == "__main__":
    main()

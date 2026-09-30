import os
import sys
import argparse
import prompts
import call_function
import config
from openai import OpenAI
from openai.types.chat import ChatCompletion
from dotenv import load_dotenv

TESTING_MODE = False
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
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("-t", "--test", action="store_true", help="Suppress actual LLM calls")
    args = parser.parse_args()
    
    # Testing mode check
    global TESTING_MODE
    TESTING_MODE = args.test
    if TESTING_MODE:
        print("Running in TESTING_MODE. No requests to OpenRouter AI will be made")
    
    if not (api_key := os.environ.get("OPENROUTER_API_KEY")):
        raise RuntimeError("OPENROUTER_API_KEY not set")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    
    
    messages = [
        {
            "role": "system",
            "content": prompts.system_prompt
        },
        {
            "role": "user",
            "content": args.user_prompt
        }
    ] 
    
    for _ in range(config.ITERATION_CAP):
        response = call_llm(client, messages)
        
        
        if response.usage:
            if args.verbose:
                print(f"User prompt: {args.user_prompt}")
                print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
        else:
            raise RuntimeError("no usage data from LLM response")
        
        message = response.choices[0].message
        messages.append(message)
        
        if message.tool_calls:            
            for tool_call in message.tool_calls:
                result_message = call_function.call_function(tool_call, args.verbose)
                
                if not result_message["content"]:
                    raise Exception("Returned tool message has no content!")
                
                if args.verbose:
                    print(f"-> {result_message['content']}")
                    
                messages.append(result_message)
        else:
            print("Final response:")
            print(message.content)
            return
        
    print(f"Max iterations of {config.ITERATION_CAP} reached!")
    print("Exiting...")
    exit(1)
                      
            
            

def call_llm(client, messages):
    if TESTING_MODE:
        return FAKE_RESPONSE
    return client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=call_function.available_functions,
            temperature=0,
        )

if __name__ == "__main__":
    main()
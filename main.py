import os
import sys
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from functions.call_function import available_functions, call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
   
    for iteration in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
                temperature=0
            ),
        )

        if response.usage_metadata is None:
            raise ValueError("Response metadata is missing!")

    
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if args.verbose:
            print(f"--- Iteration {iteration + 1} ---")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
        calls = response.function_calls

        if calls:
            function_result_parts = []

            for function_call in calls:
                function_call_result = call_function(function_call, args.verbose)

                if not function_call_result.parts:
                    raise Exception("Parts list is empty")
                
               
                function_result_parts.append(function_call_result.parts[0])

                if args.verbose:
                    result_data = function_call_result.parts[0].function_response.response
                    print(f"Function Result [{function_call.name}]: {result_data.get('result')}")

            messages.append(types.Content(role="user", parts=function_result_parts))

        else:
            print("\nResponse:")
            print(response.text)
            return  
   
    print(f"Error: Agent failed to reach a conclusion within 20 iterations.")
    sys.exit(1)




if __name__ == "__main__":
    main()

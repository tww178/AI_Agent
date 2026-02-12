import os
import sys
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`


    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])] #I don't understsand this line
    client = genai.Client(api_key=api_key) #https://googleapis.github.io/python-genai/genai.html#genai.client.Client
    
       
    
    for _ in range(20):
        response = client.models.generate_content( #https://googleapis.github.io/python-genai/genai.html#genai.models.Models, https://googleapis.github.io/python-genai/genai.html#genai.models.Models.generate_content
            model="gemini-2.5-flash",
            contents=messages, #Why can it be a list?
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt, temperature=0), #https://googleapis.github.io/python-genai/genai.html#genai.types.GenerateContentConfig
        )

         

        #https://googleapis.github.io/python-genai/genai.html#genai.types.GenerateContentConfig.tools
        #https://googleapis.github.io/python-genai/genai.html#genai.types.GenerateContentConfig.system_instruction
        #https://googleapis.github.io/python-genai/genai.html#genai.types.GenerateContentConfig.temperature

        #The generate_content method returns a GenerateContentResponse object. Print the .text property of the response to see the model's answer.
        #https://googleapis.github.io/python-genai/genai.html#genai.types.GenerateContentResponse
        #The GenerateContentResponse object returned by the Gemini API includes a usage_metadata property. The usage_metadata in turn has both:
        #a prompt_token_count property, showing the number of tokens in the prompt that was sent to the model; and
        #a candidates_token_count property, showing the number of tokens in the model's response.

        if not response.usage_metadata:
            raise RuntimeError("Gemini API response appears to be malformed")

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        if response.candidates:
            for c in response.candidates:
                if c.content: # add this guard to avoid appending None candidates
                    messages.append(c.content)

        #print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        #print("Response tokens:", response.usage_metadata.candidates_token_count)

        if not response.function_calls:
            print("Final response:")
            print(response.text)
            return

        function_responses = []
        
        for function_call in response.function_calls:
            #print(f"Calling function: {function_call.name}({function_call.args})")
            function_call_result = call_function(function_call, args.verbose)
            if not function_call_result.parts:
                raise Exception("The types.Content object that we return from call_function should have a non-empty .parts list.")
            if function_call_result.parts[0].function_response == None:
                raise Exception("The FunctionResponse object is None.")
            if function_call_result.parts[0].function_response.response == None:
                raise Exception("Actual function result is None.")
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            function_responses.append(function_call_result.parts[0])
        
        messages.append(types.Content(role="user", parts=function_responses))

    print("Maximum iterations (20) reached")
    sys.exit(1)
        



    


if __name__ == "__main__":
    main()

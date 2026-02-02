import os
from dotenv import load_dotenv
from google import genai


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
    )

    #The generate_content method returns a GenerateContentResponse object. Print the .text property of the response to see the model's answer.
    #The GenerateContentResponse object returned by the Gemini API includes a usage_metadata property. The usage_metadata in turn has both:
    #a prompt_token_count property, showing the number of tokens in the prompt that was sent to the model; and
    #a candidates_token_count property, showing the number of tokens in the model's response.

    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)
    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()

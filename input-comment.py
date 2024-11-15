from openai import OpenAI
import os
import sys

apikey = os.getenv("OPENAI_API_KEY")
if not apikey:
    raise ValueError("Missing API Key. Please set OPENAI_API_KEY in the environment.")
client = OpenAI(api_key=apikey)

def analyse_comment(comment):
    prompt = (  "For the following comment:\n"
            f"\"{comment}\"\n"
            "1. Analyze the overall sentiment (positive, negative, or neutral).\n"
            "2. Calculate the stop word ratio (ratio of stop words to total words).\n"
            "3. Provide feedback on the use of stop words and clarity of the comment.\n"
            "4. Offer suggestions for improving tone and clarity, if needed."
            "Finally, list all positive words used, and negative words used. Omit any programming specific terms, e.g. 'error'."
    )

    response = get_openai_response(comment)
    
    return response

def get_openai_response(prompt):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert in code reviews, and analysing code review comments."},
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return completion.choices[0].message.content
    except:
        return "Error retrieving OpenAI response."

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py '<comment>'")
        sys.exit(1)
    
    comment = sys.argv[1]
    feedback = analyse_comment(comment)
    print(feedback)

if __name__ == "__main__":
    main()
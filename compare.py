import os
from dotenv import load_dotenv
from openai import OpenAI
import openai

# Load environment variables
load_dotenv()

api_key = os.getenv("GRAPHRAG_API_KEY")
llm_model = os.getenv("GRAPHRAG_LLM_MODEL")

def compare_responses(aspect, response1, response2):
    # Define a comprehensive system prompt
    system_prompt = """
    You are very skilled at qualitative data analysis.
    """

    # Create the comparison prompt with the question and responses
    prompt = f"""
    You are tasked with analyzing the commonalities and differences of a specified aspect between two datasets based on given responses. Your goal is to carefully evaluate the responses and provide a comprehensive comparison.

    The aspect being analyzed is:
    <aspect>
    {aspect}
    </aspect>

    Here are the responses for Dataset 1:
    <dataset1_responses>
    {response1}
    </dataset1_responses>

    Here are the responses for Dataset 2:
    <dataset2_responses>
    {response2}
    </dataset2_responses>

    To complete this task, follow these steps:

    1. Carefully read and analyze the responses for both datasets.

    2. Identify commonalities:
    - Look for similar themes, patterns, or characteristics mentioned in both sets of responses.
    - Consider both explicit and implicit similarities.
    - Note any consistent language or concepts used across both datasets.

    3. Identify differences:
    - Look for unique themes, patterns, or characteristics mentioned in one dataset but not the other.
    - Consider variations in emphasis or importance placed on certain aspects.
    - Note any contrasting or conflicting information between the two datasets.

    4. Evaluate the significance of the commonalities and differences:
    - Consider how these similarities and differences relate to the specified aspect.
    - Assess the potential implications of these findings.

    5. Organize your analysis into a structured response using the following format:

    <analysis>
    <commonalities>
    [List and explain the common elements found in both datasets regarding the specified aspect. Provide specific examples from the responses to support your points.]
    </commonalities>

    <differences>
    [List and explain the differences found between the two datasets regarding the specified aspect. Provide specific examples from the responses to support your points.]
    </differences>

    <conclusion>
    [Summarize the key findings of your analysis, highlighting the most significant commonalities and differences. Offer insights into what these findings might imply about the specified aspect in relation to the two datasets.]
    </conclusion>
    </analysis>

    Ensure that your analysis is thorough, balanced, and supported by evidence from the provided responses. Avoid making assumptions beyond what is presented in the data. If you encounter any ambiguities or need clarification, state this in your analysis.
    """

    client = OpenAI(api_key=api_key)

    # Send the request to OpenAI
    completion = client.chat.completions.create(
        model=llm_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message.content

if __name__ == "__main__":
    # Example question and responses
    question = "What are the main causes of climate change?"
    response1 = "Climate change is influenced by greenhouse gases."
    response2 = "Climate change is driven by greenhouse gases and deforestation."

    print("Question:", question)
    print("Response from Dataset A:", response1)
    print("Response from Dataset B:", response2)

    print("\nComparing responses with GPT-4o-mini...")
    differences = compare_responses(question, response1, response2)

    print("\nDifferences identified by GPT-4o-mini:\n", differences)

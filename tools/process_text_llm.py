from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_llm_chain(description):
    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama3-70b-8192"
    )

    prompt = PromptTemplate(
        input_variables=["text"],
        template="""
You are **RagBot**, an AI-powered assistant trained to help users format a User Input.

Your job is to analyze the text and identify important information. Format the output in a structured way.

---

**User Input**:
{text}

---

**Answer**:

Job Title: Jobs mentioned in the text
Description: Description of the job

- If the text does not contain any job information, respond with "No job information found."
"""
    )

    chain = LLMChain(
        llm=llm,
        prompt=prompt
    )
    
    results = chain.run(description)
    return results





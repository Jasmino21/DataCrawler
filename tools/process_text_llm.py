from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_llm_chain():
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

    # Ask a question
    question = "URGENT HIRING!\n\nTrackerteer Web Dev Corp. is [#hiring](https://www.facebook.com/hashtag/hiring?__eep__=6&__cft__[0]=AZWolMVuY55nPmgL64GiradADnC9kP8cvYfWF0aiVNB-X1g2yZSrqEGGXm9z5g7GV-zV6fDjOuhC2h-1sZew9-OBgKxW4RF3GkzLgZILvZpdApfAjeje19cUzHBFlTHdcMZD5RlBVCt6nyNokBS4u1mSuJZViuGz2xkqU4d07fHjd8_-dn_hALYCgtdlZQQes_QmdA8Vt8fnQW9J7-oD-y-y&__tn__=*NK-R) for an 𝗜𝗧 𝗛𝗘𝗟𝗣𝗗𝗘𝗦𝗞 𝗦𝗨𝗣𝗣𝗢𝗥𝗧 𝗦𝗣𝗘𝗖𝗜𝗔𝗟𝗜𝗦𝗧 (𝗠𝗜𝗗-𝗟𝗘𝗩𝗘𝗟)\n\n𝗝𝗼𝗯 𝗗𝗲𝘀𝗰𝗿𝗶𝗽𝘁𝗶𝗼𝗻:\n\nWe are currently seeking a motivated and customer-oriented individual to join our Development Department as an IT Helpdesk Support Specialist. This role will be responsible for providing technical assistance and support to our internal development team members, ensuring the smooth operation of hardware, software, and other IT systems.\n\n𝗞𝗲𝘆 𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗶𝗯𝗶𝗹𝗶𝘁𝗶𝗲𝘀:\n\n- Provide first-level technical support and troubleshooting assistance to development team members via phone, email, ticketing system, or in person.\n\n- Diagnose and resolve hardware, software, and network issues, including but not limited to desktops, laptops, printers, mobile devices, operating systems, and applications.\n\n- Install, configure, and maintain software applications and development tools used by the development team, ensuring compatibility and optimal performance.\n\n- Collaborate with the IT team to escalate and resolve complex technical issues promptly, and provide follow-up support and documentation as needed.\n\n- Set up and configure new user accounts, permissions, and access rights according to company policies and procedures.\n\n- Perform routine maintenance tasks such as software updates, patches, and system backups to ensure data integrity and security.\n\n- Assist in the deployment and rollout of new hardware, software, and IT systems, and provide training and support to end users as needed.\n\n- Document technical procedures, troubleshooting steps, and solutions in the knowledge base for future reference and training purposes.\n\n- Stay current with emerging technologies, trends, and best practices in IT support and development tools, and provide recommendations for process improvements and system enhancements.\n\n- Adhere to IT policies, standards, and guidelines, and maintain confidentiality and security of sensitive information.\n\n𝗤𝘂𝗮𝗹𝗶𝗳𝗶𝗰𝗮𝘁𝗶𝗼𝗻𝘀:\n\n- Bachelor's degree in Information Technology, Computer Science, or related field preferred.\n\n- 1-3 years of experience in IT support or helpdesk role, preferably in a software development environment.\n\n- Strong technical knowledge of desktop and laptop hardware, Windows and/or macOS operating systems, Microsoft Office Suite, and common software development tools (e.g., IDEs, version control systems).\n\n- Familiarity with networking concepts, protocols, and troubleshooting techniques.\n\n- Excellent communication and interpersonal skills, with the ability to explain technical concepts to non-technical users.\n\n- Customer service-oriented mindset with a focus on delivering high-quality support and solutions.\n\n- Ability to prioritize tasks, manage time effectively, and work independently or as part of a team.\n\n- Certifications such as CompTIA A+, Network+, or Microsoft Certified Professional (MCP) are a plus.\n\nIf you feel that you are the right person for the job, please email your CV, a cover letter stating your salary expectations, and an example of published work to hr@trackerteer.com with “IT Helpdesk Support Specialist (Mid-Level)” in the subject line.\n\nCheck this link: [https://www.rfr.bz/fm8ehp5](https://www.rfr.bz/fm8ehp5?fbclid=IwZXh0bgNhZW0CMTAAYnJpZBExdDhqdXNHWFZ3S0Vicks1agEepQUfN57ALly0GdCP10eb9jokgdq5Kt_4xPK1PWX4P8PcirBFnuaVM7NsuYU_aem_7kjrvhrv2fpMNpAAuVp88w)\n\nNote: Office-based inside Clark Freeport Zone, Pampanga\n\nLocation: Old - FPMI Building, New - HOCB Building,\n\nJ. Abad Santos Cr., Manunggal Street, Clark Freeport Zone, Pampanga 2023\n\nSchedule: Mid Shift or Graveyard Shift\n\nSalary Range: To be discussed."
    response = chain.run(question)

    print(response)

get_llm_chain()
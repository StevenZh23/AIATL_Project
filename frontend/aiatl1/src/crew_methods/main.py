import os
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai import Agent, Task, Crew, Process, LLM
from aiatl1.src.crew_methods.crew import Aiatl1Crew
import os
from dotenv import load_dotenv

def run(symptoms, name, race, gender):
    load_dotenv()
    """
    Run the crew with user input.
    """

    crew_instance = Aiatl1Crew()
    # symptoms = input("put symptoms")
    # name = input("put name")
    # race = input("put race")
    # gender = input("put gender")

    inputs = {
        'symptoms': symptoms,  
        'name': name,
        'race': race,
        'gender': gender,
    }

    crew_instance.crew().kickoff(inputs = inputs)
# if __name__ == "__main__":
#    run()
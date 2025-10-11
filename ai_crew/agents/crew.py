from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import os
from crewai import LLM
from ai_crew.tools.medical_rag import CardioMedicalReportRAG, PulmoMedicalReportRAG, NeuroMedicalReportRAG
from crewai_tools import FileWriterTool, FileReadTool	
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# Define the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

file_writer_tool = FileWriterTool()
file_reader_tool = FileReadTool()
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
google_api_key = os.getenv("GOOGLE_API_KEY")

# Create LLM with proper configuration
llm = LLM(
    model="gemini/gemini-2.0-flash-lite", 
    verbose=True, 
    temperature=0.9, 
    api_key=google_api_key
)



@CrewBase
class Aiatl1Crew():
    """Aiatl1 crew"""

    @agent
    def cardiologist(self) -> Agent:
        return Agent(
            config=self.agents_config['cardiologist'],
            verbose=True,
            llm=llm,
            memory = True,
            tools = [CardioMedicalReportRAG()],
            allow_delegation = False,
            max_iter = 3,
        )

    @agent
    def pulmonologist(self) -> Agent:
        return Agent(
            config=self.agents_config['pulmonologist'],
            verbose=True,
            llm=llm,
            memory = True,
            tools = [PulmoMedicalReportRAG()],
            allow_delegation = False,
            max_iter = 3,
        )

    @agent
    def neurologist(self) -> Agent:
        return Agent(
            config=self.agents_config['neurologist'],
            verbose=True,
            llm=llm,
            memory = True,
            tools = [NeuroMedicalReportRAG()],
            allow_delegation = False,
            max_iter = 3,
        )

    @agent
    def diagnosis_decider(self) -> Agent:
        return Agent(
            config=self.agents_config['diagnosis_decider'],
            verbose=True,
            llm=llm, #cllm for claude
            memory = True,
            max_iter = 3,
            tools = [file_reader_tool],
        )
    @agent
    def diagnosis_dei(self) -> Agent:
        return Agent(
            config=self.agents_config['diagnosis_dei'],
            verbose=True,
            llm=llm,
            memory = True,
            max_iter = 3,
        )
    
    @agent
    def diagnosis_deliverer(self) -> Agent:
        return Agent(
            config=self.agents_config['diagnosis_deliverer'],
            verbose=True,
            llm=llm,
            memory = True,
            allow_delegation = False,
            max_iter = 3,
        )

    @task
    def diagnosis_task_cardiologist(self) -> Task:
        return Task(
            config=self.tasks_config['diagnosis_task_cardiologist'],
            output_file=os.path.join(PROJECT_ROOT, 'data', 'analysis_outputs', 'cardiologist_analysis.txt'),
            tools=[file_writer_tool],
        )

    @task
    def diagnosis_task_pulmonologist(self) -> Task:
        return Task(
            config=self.tasks_config['diagnosis_task_pulmonologist'],
            output_file=os.path.join(PROJECT_ROOT, 'data', 'analysis_outputs', 'pulmonologist_analysis.txt'),
            tools=[file_writer_tool],
        )
    
    @task
    def diagnosis_task_neurologist(self) -> Task:
        return Task(
            config=self.tasks_config['diagnosis_task_neurologist'],
            output_file=os.path.join(PROJECT_ROOT, 'data', 'analysis_outputs', 'neurologist_analysis.txt'),
            tools=[file_writer_tool],
        )

    @task
    def diagnosis_decision(self) -> Task:
        analysis_dir = os.path.join(PROJECT_ROOT, 'data', 'analysis_outputs')
        return Task(
            config=self.tasks_config['diagnosis_decision'],
            tools = FileReadTool(file_paths=[
                os.path.join(analysis_dir, 'pulmonologist_analysis.txt'), 
                os.path.join(analysis_dir, 'cardiologist_analysis.txt'),
                os.path.join(analysis_dir, 'neurologist_analysis.txt')
            ]),
            respect_context_window = True,
        )
    
    @task
    def diagnosis_dei_customizer(self) -> Task:
        return Task(
            config=self.tasks_config['diagnosis_dei_customizer'],
        )

    @task
    def diagnosis_delivery(self) -> Task:
        return Task(
            config=self.tasks_config['diagnosis_delivery'],
            output_file=os.path.join(PROJECT_ROOT, 'data', 'analysis_outputs', 'final_report.txt'),
            tools=[file_writer_tool],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Aiatl1 crew"""
        return Crew(
            agents=self.agents,
            tasks=[
                self.diagnosis_task_cardiologist(), 
                self.diagnosis_task_pulmonologist(), 
                self.diagnosis_task_neurologist(), 
                self.diagnosis_decision(), 
                self.diagnosis_dei_customizer(), 
                self.diagnosis_delivery()
            ],
            process=Process.sequential,
            verbose=True,
        )
import os
from crewai import Agent, Task, Crew, Process, LLM
from ai_crew.agents.crew import Aiatl1Crew
from dotenv import load_dotenv

def run(symptoms, name, race, gender):
    load_dotenv()
    """
    Run the crew with user input and handle file writing deterministically.
    """
    
    # Define file paths
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    analysis_dir = os.path.join(PROJECT_ROOT, 'data', 'analysis_outputs')
    
    # Ensure analysis directory exists
    os.makedirs(analysis_dir, exist_ok=True)
    
    # Clear existing files
    for file in os.listdir(analysis_dir):
        if file.endswith('.txt'):
            os.remove(os.path.join(analysis_dir, file))

    crew_instance = Aiatl1Crew()
    
    inputs = {
        'symptoms': symptoms,  
        'name': name,
        'race': race,
        'gender': gender,
    }

    # Run the crew and capture outputs
    result = crew_instance.crew().kickoff(inputs=inputs)
    
    # Write outputs to files deterministically
    try:
        # Define file paths
        cardiologist_file = os.path.join(analysis_dir, 'cardiologist_analysis.txt')
        pulmonologist_file = os.path.join(analysis_dir, 'pulmonologist_analysis.txt')
        neurologist_file = os.path.join(analysis_dir, 'neurologist_analysis.txt')
        final_report_file = os.path.join(analysis_dir, 'final_report.txt')
        
        # Write the complete result to final report
        if result:
            with open(final_report_file, 'w', encoding='utf-8') as f:
                f.write(str(result))
            print(f"Analysis complete! Results saved to {final_report_file}")
        else:
            with open(final_report_file, 'w', encoding='utf-8') as f:
                f.write("Analysis completed but no results were generated.")
            print("Analysis completed but no results were generated.")
        
        # For now, we'll create placeholder files for individual analyses
        # In a more sophisticated setup, you'd capture individual task outputs
        placeholder_text = "Individual analysis will be available in future versions."
        
        with open(cardiologist_file, 'w', encoding='utf-8') as f:
            f.write(placeholder_text)
        with open(pulmonologist_file, 'w', encoding='utf-8') as f:
            f.write(placeholder_text)
        with open(neurologist_file, 'w', encoding='utf-8') as f:
            f.write(placeholder_text)
                
    except Exception as e:
        print(f"Error writing files: {e}")
        # Still write something to the final report
        final_report_file = os.path.join(analysis_dir, 'final_report.txt')
        with open(final_report_file, 'w', encoding='utf-8') as f:
            f.write(f"Analysis completed but file writing failed: {e}")
# if __name__ == "__main__":
#    run()
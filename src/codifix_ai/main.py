

import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

from typing import List

from crewai import Crew
from crewai_tools import DirectoryReadTool, \
                         FileReadTool

directory_read_tool = DirectoryReadTool(directory='running-crew/erros')
directory_read_tool_kotlin = DirectoryReadTool(directory='running-crew/kotlin-files')
file_read_tool = FileReadTool()


from .models import custom_models  as cm
from .tools import custom_tools as ct




 # 0 = OFF, 1 = DEBUG, 2 = INFO
verbose_type = 1 #TODO - extrair .env

from .tasks import FirebaseErrorTasks
from .agents import FirebaseErrorAgents

tasks = FirebaseErrorTasks()
agents = FirebaseErrorAgents()

bigquery_research_tool = ct.BigQueryResearchTool()
git_search_tool = ct.GitSearchTool()
webhhok_tool = ct.WebhookTool()

# Define Agents
senior_research_agent = agents.senior_research_agent()
git_manager_agent = agents.git_master_agent()
senior_analyst_identifier_agent = agents.senior_analyst_identifier_agent() 
senior_analyst_suggester_agent = agents.senior_analyst_suggester_agent()
senior_engineer_agent = agents.senior_engineer_agent()
qa_engineer_agent = agents.qa_engineer_agent()
chief_qa_engineer_agent = agents.chief_qa_engineer_agent()
webhhok_agent = agents.microsoft_teams_agent()

# Define Tasks
research_solution = tasks.research_task(
										agent=senior_research_agent, 
										json_model=cm.BigQueryError, 
										tools_list=[directory_read_tool, file_read_tool, bigquery_research_tool]
										)

def suggest_solution(stack_trace, original_code): 
	return tasks.suggest_task(agent=senior_analyst_suggester_agent,stack_trace=stack_trace, original_code=original_code)

def code_solution(stack_trace, suggest, original_code): 
	return tasks.code_task(agent=senior_engineer_agent, stack_trace=stack_trace, suggest=suggest, original_code=original_code)

def review_solution(original_code, suggested_code, stack_trace): 
	return tasks.review_task(agent=qa_engineer_agent, stack_trace=stack_trace, original_code=original_code, suggested_code=suggested_code)

def approve_solution(stack_trace, suggested_code): 
	return tasks.evaluate_task(agent=chief_qa_engineer_agent, stack_trace=stack_trace, suggested_code=suggested_code)

def send_notification(notification_message):
	return tasks.microsoft_teams_task(agent=webhhok_agent, json_model=cm.WebhookModel, message=notification_message, webhook_tool=[webhhok_tool])


# review_solution.context = [suggest_solution, code_solution]
# approve_solution.context = [suggest_solution, code_solution, review_solution]

def print_results(solution):
	print("\n\n##########################")
	print("## Resultado da Solução ##")
	print("##########################\n")
	print(solution)

# Create Crew responsible for Copy
def kickoff_builded_research_crew():

	crew = Crew(
		agents=[
			senior_research_agent
		],
		tasks=[
			research_solution
		],
		verbose=verbose_type
	)

	researched_solution = crew.kickoff()
	return researched_solution

def kickoff_builded_crew_repo(researcher_notes):
	getting_files_solution = tasks.git_crawler_task(
													agent=git_manager_agent, 
													json_model=cm.GitFileError, 
													researcher_notes=researcher_notes, 
													tools_list=[git_search_tool]
													)
	
	crawler_files_solution = tasks.git_crawler_task(
													agent=git_manager_agent, 
													json_model=cm.GitFileError, 
													researcher_notes=researcher_notes, 
													tools_list=[directory_read_tool_kotlin, file_read_tool]
													)
	
	crew_repo = Crew(
		agents=[
			git_manager_agent,
			git_manager_agent,
		],
		tasks=[
			getting_files_solution,
			crawler_files_solution
		],
		verbose=verbose_type
	)

	repo_solution = crew_repo.kickoff()
	return repo_solution

def kickoff_builded_crew_identify(stack_trace, full_code):
	suggest_solution_identified = tasks.suggest_task(senior_analyst_suggester_agent, stack_trace, full_code)
	crew_identify_suggest = Crew(
		agents=[
			senior_analyst_suggester_agent,
		],
		tasks=[
			suggest_solution_identified,			
		],
		verbose=verbose_type
	)

	suggest_identified_solution = crew_identify_suggest.kickoff()
	return suggest_identified_solution

def kickoff_builded_crew_suggest(query_solution, repository_solution):

	identify_solution = tasks.identify_task(senior_analyst_identifier_agent, query_solution)


	crew = Crew(
		agents=[
			senior_analyst_identifier_agent,
			senior_analyst_suggester_agent
		],
		tasks=[
			identify_solution,
			suggest_solution(stack_trace=query_solution, original_code=repository_solution)
		],
		verbose=verbose_type
	)

	suggestion_solution = crew.kickoff()
	return suggestion_solution

def kickoff_builded_crew_dev(stack_trace, suggest_solution, repository_solution):

	crew = Crew(
		agents=[
			senior_engineer_agent
		],
		tasks=[
			code_solution(stack_trace=stack_trace,suggest=suggest_solution,original_code=repository_solution)
		],
		verbose=verbose_type
	)

	dev_solution = crew.kickoff()
	return dev_solution

def kickoff_builded_crew_qa(query_solution, repository_solution, dev_solution):

	crew = Crew(
		agents=[
			qa_engineer_agent,
		],
		tasks=[
			review_solution(original_code=repository_solution, suggested_code=dev_solution, stack_trace=query_solution),
		],
		verbose=verbose_type
	)

	qa_solution = crew.kickoff()
	return qa_solution

def codifixCrew():
	repo_dir = "current_repo_temp"
	directory_path = 'running-crew/erros'
	error_directory = Path(directory_path)
	destinarion_dir = "running-crew/kotlin-files"
	file_path = Path(destinarion_dir)

	print('Iniciando aplicação...\n')

	print('... Etapa 1 ...\n')
	crew_research_step = kickoff_builded_research_crew()
	print('\n\n\n---------------------\n\n\n')
	print('... Etapa 2 ...\n')
	crew_repo_step = kickoff_builded_crew_repo(researcher_notes=crew_research_step) # retorna o arquivo completo
	print('\n\n\n---------------------\n\n\n')
	print('... Etapa 3 ...\n')
	crew_identify_step = kickoff_builded_crew_identify(stack_trace=crew_research_step, full_code=crew_repo_step) # retorna uma análise do stackTrace
	print('\n\n\n---------------------\n\n\n')
	print('... Etapa 4 ...\n')
	crew_suggest_step = kickoff_builded_crew_suggest(query_solution=crew_research_step,repository_solution=crew_repo_step)
	print('\n\n\n---------------------\n\n\n')
	print('... Etapa 5 ...\n')
	crew_dev_step = kickoff_builded_crew_dev(stack_trace=crew_research_step, suggest_solution=crew_suggest_step, repository_solution=crew_repo_step)
	print('\n\n\n---------------------\n\n\n')
	print('... Etapa 6 ...\n')
	qa_crew_step = kickoff_builded_crew_qa(query_solution=crew_research_step, repository_solution=crew_repo_step, dev_solution=crew_dev_step)
	print(qa_crew_step)
	print('\n\n\n---------------------\n')
	print('\n---------------------\n')
	print('Aplicação concluída...\n')



def run():
    codifixCrew()
    
if __name__ == '__main__':
	codifixCrew()
 
 
 
 
 
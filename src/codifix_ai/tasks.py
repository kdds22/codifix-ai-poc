
from textwrap import dedent
from crewai import Task


human_input_value = True

tasks_config = 'config/tasks.yaml'

class FirebaseErrorTasks():

	def research_task(self, agent, json_model, tools_list: list):
		return Task(
			config=tasks_config['research_task'],
			tools=tools_list,
			agent=agent,
			output_json=json_model,
			output_file="main_error_report.json",
			human_input=human_input_value,
		)
  
	def git_repo_task(self, agent, json_model, tools_list):
		return Task(
			config=tasks_config['git_repo_task'],
			tools=tools_list,
			agent=agent,
			output_json=json_model,
			output_file="kotlin_file_error_reported.json",
			human_input=human_input_value,
		)
	
	def git_crawler_task(self, agent, json_model, tools_list): # input = {researcher_notes}
		return Task(
			config=tasks_config['git_file_task'],
			tools=tools_list,
			agent=agent,
			output_json=json_model,
			output_file="kotlin_file_error_reported.json",
			human_input=human_input_value,
		)
	
	def identify_task(self, agent): # input = {researcher_notes}
		return Task(
			config=tasks_config['identify_task'],
			agent=agent,
			human_input=human_input_value,
		)
	
	def suggest_task(self, agent): # input = {researcher_notes}, {original_code}
		return Task(
			config=tasks_config['suggest_task'],
   			agent=agent,
			human_input=human_input_value,
		)

	def code_task(self, agent): # input = {researcher_notes}, {original_code}, {ai_suggest}
		return Task(
			config=tasks_config['code_task'],
			agent=agent,
			human_input=human_input_value,
		)

	def review_task(self, agent): # input = {researcher_notes}, {original_code}, {final_ai_suggest}
		return Task(
			config=tasks_config['review_task'],
			agent=agent,
			human_input=human_input_value,
			output_file="file_error_solved.md",
		)

	def evaluate_task(self, agent):  # input = {researcher_notes}, {review_final_ai_suggest}
		return Task(
			config=tasks_config['evaluate_task'],
        	agent=agent,
			human_input=human_input_value,
			output_file="final_file_error_solved.md",
		)
	

	def microsoft_teams_task(self, agent, json_model, webhook_tool): # input = {message}
		return Task(
			config=tasks_config['microsoft_teams_task'],
			agent=agent,
			human_input=human_input_value,
			output_json=json_model,
			output_file="microsoft_teams_notification.json",
			tools=webhook_tool,
		)
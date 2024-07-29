from textwrap import dedent
from crewai import Task
from pydantic import BaseModel
from typing import List
from crewai_tools import BaseTool
import webhook

class SectionModel(BaseModel):
	activityTitle: str
	activitySubtitle: str

class WebhookModel(BaseModel):
	themeColor: str
	summary: str
	sections: List[SectionModel]

class WebhookTool(BaseTool):
    name: str ="Webhook Tool"
    description: str = ("Sending a webhook to a specified channel "
         "to notify about the error.")
    
    def _run(self, text: str) -> str:
        webhook_model = WebhookModel(
            themeColor="#0078D7",
            summary="CodiFix - Sugestão ",
            sections=[
                SectionModel(
                    activityTitle="Mensagem de Erro",
                    activitySubtitle="CodiFix webhook XPTO",
                ),
            ],
        )
        return webhook.send_teams_by_model(webhook_model)


human_input_value = True

class FirebaseErrorTasks():

	def research_task(self, agent, json_model, tools_list: list):
		return Task(
			description=(
				"""
				Your task is to analyze and identify the root cause of the firebase error. 
				With help from your BigQuery tool, you only need to provide the 
				error message and the relevant code snippet. 
				"""
			),
			expected_output=("""
			A expected output should be a report documenting the root cause of the firebase error. 
			"""
			),
			tools=tools_list,
			agent=agent,
			output_json=json_model,
			output_file="firebase_error_report.json",
			human_input=human_input_value,
		)
	
	def git_crawler_task(self, agent, json_model, researcher_notes, tools_list):
		"""researcher_notes = Senior Researcher Notes."""
		return Task(
			description=dedent(f"""\
				Your task is to manage Git operations for a specific project. Begin by cloning the repository with tool. 
				After cloning, list all files in the repository and locate the ones previously identified by the Senior Software Researcher as containing errors. 
				Open and confirm the contents of these files, preparing them for further analysis by subsequent agents in our workflow.

				Senior Researcher Notes
				-----------------------
				 "big_query_error":{researcher_notes}

				Instructions
				------------
				2. Locate and list the necessary files.
				3. Review these files.
				4. Your Final answer must be the entire code kotlin file, only the kotlin code and nothing else.
				5. Don't change the Senior Research Notes in your final answer."""),
			expected_output=dedent("""
				A entire reported code error kotlin file.
				"""),
			tools=tools_list,
			agent=agent,
			output_json=json_model,
			output_file="kotlin_file_error_reported.json",
			human_input=human_input_value,
		)
	
	def identify_task(self, agent, error):
		return Task(
			description=dedent(f"""
			You will receive some 'stacktraces' of a reported errors, 
			and will analyze and identify possible Kotlin solutions for the error, these are the instructions:

			Instructions
			------------
    		{error}

			Your final answer should be a full analyze about the reported errors, 
			just a full analyze about the reported errors and nothing else.
			"""),
			expected_output="""Analyze of the reported error in bullet point format, just the analyze of the reported error and nothing else.""",
			agent=agent,
			human_input=human_input_value,
		)
	
	def suggest_task(self, agent, stack_trace, original_code):
		"""stack_trace = erro informado pelo agente anterior.\n
		original_code = codigo original que causou o erro."""
		return Task(
			description=dedent(f"""
			You will receive some 'stacktraces' of a reported errors, 
			and will suggest a possible Kotlin solutions for the errors, these are the instructions:

			Begin Base Instructions
					  
			--------------
			Error Reported
			--------------
    		{stack_trace}

			-------------
			Original Code
			-------------
			{original_code}

			-------------
			End Base Instructions

			Your final answer should be code suggestions in Kotlin as well as your explanations in comment format, 
			just code suggestions in Kotlin as well as your explanations in comment format and nothing else.
			All your comments explanations should be clear, concise and in brazilian portuguese. 
			"""),
			# sugestao do codigo para resolver o erro, com explicação de como chegou ao codigo sugerido.
			expected_output="Code suggestions to solve error, with explanations how you got to the suggested code.",
			agent=agent,
			human_input=human_input_value,
		)

	def code_task(self, agent, stack_trace, suggest, original_code):
		"""suggest = sugestão dada pelo agente anterior.\n
		original_code = codigo original que causou o erro."""
		return Task(description=dedent(f"""
			You will receive code that has had a bug reported and with analysis done by the 
			best software analyst on your team, you must implement the best solution to 
			resolve the error using Kotlin, these are the instructions:

			Instructions
			------------
			Guardrails:
			- Do not change the type of the objects
			- If to change the type is necessary, create a comment above line as needed
			- Don't ident any original line, only ident the new lines added to resolve the error.
			- Don't change the order of the code, only add new code to resolve the error.
			------------
								 
			Error Reported:
					 
			{stack_trace}
			------------

			Suggest: 
    		
			{suggest}
			------------

			Original Code:

			{original_code}
			------------

			Your Final answer must be the full kotlin code, only the koltin code and nothing else.
			All your comments explanations should be clear, concise and in brazilian portuguese.
			"""),
			expected_output="Original code kotlin with the solution implemented.",
			agent=agent,
			human_input=human_input_value,
		)

	def review_task(self, agent, stack_trace, original_code, suggested_code):
		"""original_code = codigo original que causou o erro.\n
		suggested_code = codigo sugerido pelo agente anterior."""
		return Task(description=dedent(f"""\
			You are helping to implement code to resolve the reported error using Kotlin, these are the instructions::

			Instructions
			------------
			Error Reported:
					 
			{stack_trace}
			------------
								 
			Original Code:
			
			{original_code}
			------------

			Suggested Code:

			{suggested_code}
			------------

			Using the code you got, check for errors. Check for logic errors,
			syntax errors, missing imports, variable declarations, mismatched brackets,
			and security vulnerabilities.

			Your Final answer must be the full kotlin code, only the kotlin code and nothing else.
			All your comments explanations should be clear, concise and in brazilian portuguese.
			"""),
			expected_output="Full code kotlin file with the bug solved and comments of it explanations in bullet point format at the start of kotlin file.",
			agent=agent,
			human_input=human_input_value,
			output_file="file_error_solved.md",
		)

	def evaluate_task(self, agent, stack_trace, suggested_code):
		"""stack_trace = resposta do Bigquery Agent.

		suggested_code = codigo sugerido pelo agente anterior."""
		return Task(description=dedent(f"""\
			You are helping to implement code to resolve the reported error using Kotlin, these are the instructions::

			Instructions
			------------
			Error Reported:
			
			{stack_trace}
			------------

			Suggested Code to solve error:
			{suggested_code}
			------------

			You will look over the code to insure that it is complete and
			does the job that it is supposed to do.


			All your comments explanations should be clear, concise and in brazilian portuguese.
			If doesn't have anything to change in the Suggested Code, so your final answer is the full Suggest Code.
			Your Final answer must be the full kotlin code, only the kotlin code and nothing else.
			"""),
			expected_output="Full code kotlin file with the bug solved and comments of it explanations in bullet point format at the start of kotlin file.",
			agent=agent,
			human_input=human_input_value,
			output_file="file_error_solved.md",
		)
	

	# agent webhook microsoft teams
	# this agent should send a notification to microsoft teams channel
	# def microsoft_teams_agent(self):
	# 	return Agent(
	# 		role='Microsoft Teams Agent',
	# 		goal='Send notification to microsoft teams channel',
	# 		backstory=dedent("""\
	# 			You are a Microsoft Teams Agent. You are responsible for sending 
	# 			notifications to the microsoft teams channel."""),
	# 		allow_delegation=False,
	# 		# #llm=azure_llm,
	# 		verbose=True
	# 	)
	# and your task should be:
	def microsoft_teams_task(self, agent, json_model, message, webhook_tool):
		return Task(
			description=dedent(f"""\
				Your task is to send a notification to the microsoft teams channel. 
				You will send the following message:

				{message}

				Your final answer should be the message sent to the microsoft teams channel.
				"""),

			expected_output=f"Message sent to microsoft teams channel: {message}",
			agent=agent,
			human_input=human_input_value,
			output_json=json_model,
			output_file="microsoft_teams_notification.json",
			tools=webhook_tool,
		)
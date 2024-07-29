import os
from dotenv import load_dotenv
load_dotenv()
from textwrap import dedent
from crewai import Agent
from langchain_openai import AzureChatOpenAI, ChatOpenAI

# azure_llm = ChatOpenAI(
# # 	model=os.environ.get("AZURE_OPENAI_DEPLOYMENT"),
# # 	azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
# # 	azure_ad_token=os.environ.get("AZURE_OPENAI_KEY"),
# # 	#api_version=os.environ.get("AZURE_OPENAI_VERSION"),
# # 	#base_url=os.environ.get("AZURE_OPENAI_ENDPOINT_BASE")
# # )
# 	# model ="phi-3-medium-128k-instruct-1",
#    	base_url ="https://z-nkkdw.eastus2.inference.ml.azure.com/v1",
# 	api_key="eyJhbGciOiJSUzI1NiIsImtpZCI6Ijk3QTcyRUQyOUNFMjMwMTQwQjVGNzFEOTkyODk2NzBDRDRGNEJFMzUiLCJ0eXAiOiJKV1QifQ.eyJjYW5SZWZyZXNoIjoiRmFsc2UiLCJ3b3Jrc3BhY2VJZCI6IjgwNTNlYWFkLTNiYmUtNDdhZC04M2FlLWJmNDc1MDdlMTlkYyIsInRpZCI6IjU0OTk4MDljLWVlYzAtNDkxZC04Y2VhLTQ2ZGM3ZTFmZmNmOCIsIm9pZCI6IjUxZjU5OWFkLTQ1ODEtNDE3Mi04NzBjLTIyMGRhZDdmYmVkZCIsImFjdGlvbnMiOiJbXCJNaWNyb3NvZnQuTWFjaGluZUxlYXJuaW5nU2VydmljZXMvd29ya3NwYWNlcy9vbmxpbmVFbmRwb2ludHMvc2NvcmUvYWN0aW9uXCJdIiwiZW5kcG9pbnROYW1lIjoiei1ua2tkdyIsInNlcnZpY2VJZCI6InotbmtrZHciLCJleHAiOjE3MTc2MTA2MTMsImlzcyI6ImF6dXJlbWwiLCJhdWQiOiJhenVyZW1sIn0.0YWV3j-to0Db3dzBpnNG0a9SyY7ozO6cQ6Arva1LwwbVZXePM_FNzCBZKfXMI5tkKLsKFiucopxvcphE2p1_kac7qIIjZ7ZOLtJN2LWR0vicNFSwi4EbuL0ym5SNgf0Xgx5ez0ap28FTs4OOB73n9sfxcnzb6xCeH1gwg7Kc_QHTF5Ks6xiGts7kATLdpAiplSzT-e5BOFNeJp-mV_mt6G6tjDs5tQi8eU3OhmBIyj194q8SgCTtIZ4uSjR8Ioepwslkf0XSPRqIhBLVRNjBhrJi_g2gTm_CV0eU9sF_bzO_JXE814OAj7yEm5LgqGI04L1Hl8ThxRGhcIQvIeDxew"
# )


class FirebaseErrorAgents():
	def senior_research_agent(self):
		return Agent(
			role='Senior Software Researcher',
			goal='Research firebase error, identify and report causes as needed',
			backstory=dedent("""\
				You are a Senior Software Research at a leading tech think tank.
				Your mastery in Google BigQuery and Firebase error analysis. 
				Especially getting error and report to the team to help them to fix the error. 
				Your role is crucial in identifying the root cause of the error. 
				Ensures that all operations are performed efficiently and accurately, 
				maintaining the highest standards of data management."""),
			allow_delegation=False,
			# #llm=azure_llm,
			verbose=True
		)
	
	def git_master_agent(self):
		return Agent(
			role='Git Master',
			goal='Perform comprehensive Git operations, including managing repositories, branching, merging, and troubleshooting',
			backstory=dedent("""\
				You are a Git Master at a leading tech think tank. 
				With comprehensive expertise in Git operations, 
				you handle a wide range of tasks including cloning, fetching, 
				pulling, pushing, branching, merging, and resolving conflicts. 
				Your role is crucial in maintaining the integrity and 
				synchronization of the repositories. You also excel in 
				pinpointing specific files where errors have been reported, 
				aiding in swift error resolution. Your mastery in Git 
				ensures that all operations are performed efficiently 
				and accurately, maintaining the highest standards of 
				code management."""),
			allow_delegation=False,
			verbose=True
		)

	def senior_analyst_identifier_agent(self):
		return Agent(
			role='Senior Software Analyst',
			goal='Analyze the error, identify possible causes as needed',
			backstory=dedent("""\
				You are a Senior Software Analyst at a leading tech think tank.
				Your expertise in programming Kotlin code. Especially identifying 
				possible causes of errors. and do your best to provide the best analysis."""),
			allow_delegation=False,
			# #llm=azure_llm,
			verbose=True
		)
	
	def senior_analyst_suggester_agent(self):
		return Agent(
			role='Senior Software Analyst',
			goal='Analyze the error, suggesting possible solutions as needed',
			backstory=dedent("""\
				You are a Senior Software Analyst at a leading tech think tank.
				Your expertise in programming Kotlin code. Especially analyzing errors and 
				suggesting solutions. and do your best to provide the best suggest."""),
			allow_delegation=False,
			#llm=azure_llm,
			verbose=True
		)
	
	def senior_engineer_agent(self):
		return Agent(
			role='Senior Software Engineer',
			goal='Solve a kotlin code with errors as needed',
			backstory=dedent("""\
				You are a Senior Software Engineer at a leading tech think tank.
				After receiving the analysis from the 'Senior Software Analyst', 
				your sharp logic to solve the problem code is activated.
				Your expertise in programming in Kotlin. and do your best to
				produce perfect code"""),
			allow_delegation=False,
			#llm=azure_llm,
			verbose=True
		)

	def qa_engineer_agent(self):
		return Agent(
			role='Software Quality Control Engineer',
  			goal='create prefect code, by analizing the code that is given for errors',
  			backstory=dedent("""\
				You are a software engineer that specializes in checking code
  			for errors. You have an eye for detail and a knack for finding
				hidden bugs.
  			You check for missing imports, variable declarations, mismatched
				brackets and syntax errors.
  			You also check for security vulnerabilities, and logic errors"""),
			allow_delegation=False,
			#llm=azure_llm,
			verbose=True
		)

	def chief_qa_engineer_agent(self):
		return Agent(
			role='Chief Software Quality Control Engineer',
  			goal='Ensure that the code does the job that it is supposed to do',
  			backstory=dedent("""\
				You feel that programmers always do only half the job, so you are
				super dedicate to make high quality code."""),
			allow_delegation=False,
			# #llm=azure_llm,
			verbose=True
		)
	
	# agent webhook microsoft teams
	# this agent should send a notification to microsoft teams channel
	def microsoft_teams_agent(self):
		return Agent(
			role='Microsoft Teams Agent',
			goal='Send notification to microsoft teams channel',
			backstory=dedent("""\
				You are a Microsoft Teams Agent. You are responsible for sending 
				notifications to the microsoft teams channel."""),
			allow_delegation=False,
			# #llm=azure_llm,
			verbose=True
		)
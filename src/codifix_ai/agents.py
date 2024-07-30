import os
from dotenv import load_dotenv
load_dotenv()
from textwrap import dedent
from crewai import Agent

agents_config = 'config/agents.yaml'

class CrewAgents():
	def senior_research_agent(self):
		return Agent(
      		config=agents_config['researcher'],
			allow_delegation=False,
			verbose=True
		)
	
	def git_master_agent(self):
		return Agent(
			config=agents_config['git_analyst'],
			allow_delegation=False,
			verbose=True
		)

	def senior_analyst_identifier_agent(self):
		return Agent(
			config=agents_config['software_analyst'],
			allow_delegation=False,
			verbose=True
		)
	
	def senior_analyst_suggester_agent(self):
		return Agent(
			config=agents_config['software_analyst_suggester'],
			allow_delegation=False,
			verbose=True
		)
	
	def senior_engineer_agent(self):
		return Agent(
			config=agents_config['software_engineer'],
			allow_delegation=False,
			verbose=True
		)

	def qa_engineer_agent(self):
		return Agent(
			config=agents_config['qa_software_engineer'],
			allow_delegation=False,
			verbose=True
		)

	def chief_qa_engineer_agent(self):
		return Agent(
			config=agents_config['cf_qa_software_engineer'],
			allow_delegation=False,
			verbose=True
		)
	
	def microsoft_teams_agent(self):
		return Agent(
			config=agents_config['microsft_teams_notifier'],
			allow_delegation=False,
			verbose=True
		)
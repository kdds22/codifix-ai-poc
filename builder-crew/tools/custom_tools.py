
import models.custom_models as cm
from crewai_tools import BaseTool

import bigquery_script
import repo_downloader
import webhook


class BigQueryResearchTool(BaseTool):
    name: str ="Google BigQuery Research Tool"
    description: str = ("Getting the error data of bigquery "
         "to identify possible error causes.")
    
    def _run(self, text: str) -> str:
        return bigquery_script.start_bigquery('running-crew/erros')


class GitSearchTool(BaseTool):
	name: str="Git Helper Tool"
	description: str = ("Getting the project files repository to "
					 "to analyze the reported errors.")
	
	def _run(self, text: str) -> str:
		return repo_downloader.start_repo_downloader("current_repo_temp",'running-crew/erros',"running-crew/kotlin-files")


class WebhookTool(BaseTool):
    name: str ="Webhook Tool"
    description: str = ("Sending a webhook to a specified channel "
         "to notify about the error.")
    
    def _run(self, text: str) -> str:
        webhook_model = cm.WebhookModel(
            themeColor="#0078D7",
            summary="CodiFix - Sugestão ",
            sections=[
                cm.SectionModel(
                    activityTitle="Mensagem de Erro",
                    activitySubtitle="CodiFix webhook XPTO",
                ),
            ],
        )
        return webhook.send_teams_by_model(webhook_model)
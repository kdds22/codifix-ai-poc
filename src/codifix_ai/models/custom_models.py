
from pydantic import BaseModel
from typing import List

class BigQueryError(BaseModel):
	title: str
	file: str
	line: int
	function: str
	description: str
	stack_trace: str

class GitFileError(BaseModel):
	full_kotlin_code: str

class SectionModel(BaseModel):
	activityTitle: str
	activitySubtitle: str

class WebhookModel(BaseModel):
	themeColor: str
	summary: str
	sections: List[SectionModel]
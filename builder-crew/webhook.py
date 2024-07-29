# {
#   "themeColor": "00FF00",
#   "summary": "Automated Notification",    
#   "sections": [{
#     "activityTitle": "Medium Automated Notification",
#     "activitySubtitle": "The content of that message is part of the Teams WebHook tutorial 🧑‍💻"
#   }]
# }

import requests
from pydantic import BaseModel
from typing import List

class SectionModel(BaseModel):
	activityTitle: str
	activitySubtitle: str

class WebhookModel(BaseModel):
	themeColor: str
	summary: str
	sections: List[SectionModel]

webhook_url_base = "https://havan.webhook.office.com/webhookb2/8d2228f6-37f9-444e-910c-86f753fcecc0@5499809c-eec0-491d-8cea-46dc7e1ffcf8/IncomingWebhook/6f1eba9553d74e5a92c7ccf28f3f80a1/156c5bb1-b1b8-4826-ab37-2857791feb5e"

def send_teams(webhook_url:str = webhook_url_base, content:str='', title:str='', color:str="000000") -> int:
    """
      - Send a teams notification to the desired webhook_url
      - Returns the status code of the HTTP request
        - webhook_url : the url you got from the teams webhook configuration
        - content : your formatted notification content
        - title : the message that'll be displayed as title, and on phone notifications
        - color (optional) : hexadecimal code of the notification's top line color, default corresponds to black
    """
    response = requests.post(
        url=webhook_url,
        headers={"Content-Type": "application/json"},
        json={
            "themeColor": color,
            "summary": title,
            "sections": [{
                "activityTitle": title,
                "activitySubtitle": content
            }],
        },
    )
    return response.status_code # Should be 200

def send_teams_by_model(model: WebhookModel) -> str:
    """
      - Send a teams notification to the desired webhook_url
      - Returns the status code of the HTTP request
        - webhook_url : the url you got from the teams webhook configuration
        - content : your formatted notification content
        - title : the message that'll be displayed as title, and on phone notifications
        - color (optional) : hexadecimal code of the notification's top line color, default corresponds to black
    """
    response = requests.post(
        url=webhook_url_base,
        headers={"Content-Type": "application/json"},
        json=model.model_dump()
    )
    return str(response.status_code) # Should be 200
import json
import urllib
from apiclient.discovery import build

service = build('kgsearch', 'v1', 
        developerKey = 'AIzaSyAi5lV0-M-BIGUB_EMGlC9x9CqNo6FLfPE') 
entities = service.entities()
request = entities.search(query='taylor swift')
json_obj = request.execute()
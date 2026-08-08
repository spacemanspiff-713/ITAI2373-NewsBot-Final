import pandas as pd
from src.conversation.query_processor import QueryProcessor
from src.conversation.response_generator import ResponseGenerator

def test_intent_parameters_and_followup_context():
 processor=QueryProcessor(); first=processor.parse("Show me positive tech news from this week","2022-09-14"); assert first["parameters"]["category"]=="TECH" and first["parameters"]["sentiment"]=="positive"
 follow=processor.parse("What about negative ones?","2022-09-14",{"last_filters":{"category":"TECH"}}); assert follow["parameters"]["category"]=="TECH" and follow["parameters"]["inherited_category"] is True

def test_grounded_response_cites_local_rows():
 frame=pd.DataFrame({"article_id":[1],"title":["Tech title"],"category":["TECH"],"date":["2022-01-01"],"full_text":["Technology update"]}); parsed=QueryProcessor().parse("show tech news"); response=ResponseGenerator().respond(parsed,frame); assert response["results"][0]["article_id"]==1

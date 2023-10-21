from managers.n4j import reset, execute_query
from neo4j_uploader import upload

def upload_data(creds: (str, str, str), 
                data: dict,
                should_reset: bool = True
                ):
    upload(creds, data, should_reset)


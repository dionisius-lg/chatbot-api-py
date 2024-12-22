import json
import requests
import logging
from typing import List, Dict
from app.helpers.value import is_empty, is_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("client-api")

def send(clients: List[Dict], body: Dict) -> Dict:
    result = {"success": 0, "error": 0}

    if len(clients) > 0:
        responses = []

        for client in clients:
            client_url = client.get("url")
            client_auth = client.get("auth")

            if not is_empty(client_url):
                headers = {"Content-Type": "application/json"}

                if not is_empty(client_auth) and isinstance(client_auth, dict):
                    headers.update(client_auth)

                try:
                    response = requests.post(client_url, json=body, headers=headers)
                    responses.append({'status': 'fulfilled', 'response': response})
                except requests.exceptions.RequestException as err:
                    responses.append({'status': 'rejected', 'error': err, 'url': client_url})

        # process responses
        for res in responses:
            if res['status'] == 'fulfilled':
                response = res['response']
                try:
                    logger.info(f"Send to {response.url} success!")
                    logger.debug({
                        'from': 'webhook-api',
                        'message': f"Send to {response.url} success!",
                        'result': {
                            'request': json.loads(response.request.body) if response.request.body else None,
                            'response': response.json() if response.status_code == 200 else None
                        }
                    })
                    print(response.json())
                    print(json.loads(response.request.body))
                    result["success"] += 1
                except Exception as e:
                    logger.error(f"Error logging response from {response.url}: {e}")
            else:
                error = res['error']
                logger.error(f"Send to {res['url']} error! {str(error)}")
                result["error"] += 1

    return result
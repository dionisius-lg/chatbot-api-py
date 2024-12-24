import os
import json
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from app.helpers.response import ok as send_ok
from app.helpers.request import filter_data
from app.helpers import client_api
from app.controllers import app_clients as app_clients_controller
from app.schemas import webhook as schema
from app.utils.model import Model

__route = os.path.splitext(os.path.basename(__file__))[0]
router = APIRouter(prefix=f"/{__route}", tags=[__route])

@router.post("/chat")
async def chat_message(body: schema.Chat):
    data = filter_data(jsonable_encoder(body))

    # create trained model
    model = Model(model_path='model.pkl', vectorizer_path='vectorizer.pkl')

    # load intents from JSON file
    with open('intents.json', 'r') as json_file:
        intents = json.load(json_file)

    chat_session_id, message = data.values()

    predicted_class, probabilities = model.predict_class(message)
    chat_response = model.get_response(predicted_class, message, probabilities, intents)

    result = {
        "total": 1,
        "data": {
            "chat_session_id": chat_session_id,
            "message": chat_response
        }
    }

    app_clients = await app_clients_controller.get_all(dict(is_active="1"))

    if app_clients["total"] > 0:
        clients = list(map(lambda row: {
            "url": row["url"],
            "auth": {row["auth"]["key"]: row["auth"]["value"]} if row.get("auth") else None
        }, app_clients["data"]))
        client_data=dict(chat_session_id=chat_session_id, text=chat_response)
        client_api.send(clients=clients, body=client_data)

    return send_ok(**result)

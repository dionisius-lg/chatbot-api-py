# Chatbot API

## Python Version

`3.11.9`

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Documentation](#documentation)

## Installation

To get started with the Chatbot API, clone the repository and install the required dependencies in `requirements.txt`:
```bash
git clone https://github.com/dionisius-lg/chatbot-api-py.git
cd chatbot-api
venv/Scripts/activate
pip install -r requirements.txt
```

## Configuration

Rename or copy `.env.example` to `.env`, then setup the 'datasources' for your application.

## API Endpoints

### App Clients

1. Fetch App Client Data\
`GET /app_clients`\
This endpoint is used to show all data

2. Create New App Client Data\
`POST /app_clients`\
This endpoint is used to create new data

3. Create Multiple New App Client Data\
`POST /app_clients/many`\
This endpoint is used to create bulk new data

4. Create Multiple New App Client On Duplicate Update Data\
`POST /app_clients/many/update`\
This endpoint is used to create bulk new on duplicate update data

5. Fetch App Client by ID\
`GET /app_clients/{id}`\
This endpoint is used to show data by ID

6. Update App Client Data by ID\
`PUT /app_clients/{id}`\
This endpoint is used to update existing data by ID

7. Delete App Client Data by ID\
`DELETE /app_clients/{id}`\
This endpoint is used to delete data by ID

### Bot

1. Train Bot\
`GET /bot/train`\
This endpoint is used to train bot

2. Chat Bot\
`POST /bot/chat`\
This endpoint is used to chat with bot

### Exports

1. Export Intent Data\
`GET /exports/intents`\
This endpoint is used to export data to excel

2. Export Pattern Data\
`GET /exports/patterns`\
This endpoint is used to export data to excel

3. Export Response Data\
`GET /exports/responses`\
This endpoint is used to export data to excel

4. Export User Data\
`GET /exports/users`\
This endpoint is used to export data to excel

### Files

1. Download File\
`GET /files/{id}`\
This endpoint is used to download file

### Intents

1. Fetch Intent Data\
`GET /intents`\
This endpoint is used to show all data

2. Create New Intent Data\
`POST /intents`\
This endpoint is used to create new data

3. Create Multiple New Intent Data\
`POST /intents/many`\
This endpoint is used to create bulk new data

4. Create Multiple New Intent On Duplicate Update Data\
`POST /intents/many/update`\
This endpoint is used to create bulk new on duplicate update data

5. Fetch Intent by ID\
`GET /intents/{id}`\
This endpoint is used to show data by ID

6. Update Intent Data by ID\
`PUT /intents/{id}`\
This endpoint is used to update existing data by ID

7. Delete Intent Data by ID\
`DELETE /intents/{id}`\
This endpoint is used to delete data by ID

### Patterns

1. Fetch Pattern Data\
`GET /patterns`\
This endpoint is used to show all data

2. Create New Pattern Data\
`POST /patterns`\
This endpoint is used to create new data

3. Create Multiple New Pattern Data\
`POST /patterns/many`\
This endpoint is used to create bulk new data

4. Create Multiple New Pattern On Duplicate Update Data\
`POST /patterns/many/update`\
This endpoint is used to create bulk new on duplicate update data

5. Fetch Pattern by ID\
`GET /patterns/{id}`\
This endpoint is used to show data by ID

6. Update Pattern Data by ID\
`PUT /patterns/{id}`\
This endpoint is used to update existing data by ID

7. Delete Pattern Data by ID\
`DELETE /patterns/{id}`\
This endpoint is used to delete data by ID

### Responses

1. Fetch Response Data\
`GET /responses`\
This endpoint is used to show all data

2. Create New Response Data\
`POST /responses`\
This endpoint is used to create new data

3. Create Multiple New Response Data\
`POST /responses/many`\
This endpoint is used to create bulk new data

4. Create Multiple New Response On Duplicate Update Data\
`POST /responses/many/update`\
This endpoint is used to create bulk new on duplicate update data

5. Fetch Response by ID\
`GET /responses/{id}`\
This endpoint is used to show data by ID

6. Update Response Data by ID\
`PUT /responses/{id}`\
This endpoint is used to update existing data by ID

7. Delete Response Data by ID\
`DELETE /responses/{id}`\
This endpoint is used to delete data by ID

### Users

1. Fetch User Data\
`GET /users`\
This endpoint is used to show all data

2. Create New User Data\
`POST /users`\
This endpoint is used to create new data

3. Create Multiple New User Data\
`POST /users/many`\
This endpoint is used to create bulk new data

4. Create Multiple New User On Duplicate Update Data\
`POST /users/many/update`\
This endpoint is used to create bulk new on duplicate update data

5. Fetch User by ID\
`GET /users/{id}`\
This endpoint is used to show data by ID

6. Update User Data by ID\
`PUT /users/{id}`\
This endpoint is used to update existing data by ID

7. Delete User Data by ID\
`DELETE /users/{id}`\
This endpoint is used to delete data by ID

### Webhook

1. Chat Message\
`POST /chat`\
This endpoint is used to post chat message

## Documentation

Swagger Documentation
```sh
/docs
```
# dango-backend

## Create a virtual environment
```
python3 -m venv venv
```

## Activate the virtual environment
```
source venv/bin/activate
```

## Install dependencies
```
pip install openai
pip install fastapi
pip install uvicorn
```

## Set the openai api key
```
export OPENAI_API_KEY=your-api-key
```

## Run the server
```
uvicorn back_end:app --reload
```
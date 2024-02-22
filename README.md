# dango-backend

## create a virtual environment
```
python3 -m venv venv
```

## activate the virtual environment
```
source venv/bin/activate
```

## install dependencies
```
pip install openai
pip install fastapi
pip install uvicorn
```

## set the openai api key
```
export OPENAI_API_KEY=your-api-key
```

## run the server
```
uvicorn back_end:app --reload
```
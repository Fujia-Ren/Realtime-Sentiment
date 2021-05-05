# Realtime-Sentiment
Cloud Computing (CS5412) Final Project  

## Components:

Cloud DB
- This will store a dict of {hashtag:(frequency, avg_sentiment)}

Azure functions
- Using a Twitter API, we can write functions to randomly sample a number of tweets every x minutes

Microservices
- to compute the sentiment analysis

ML Model
- Google cloud, etc. 

## References
[Twitter Stream API](https://developer.twitter.com/en/docs/twitter-api/tweets/sampled-stream/introduction)  
[Azure fucntion output binding to CosmosDB (python)](https://evan-wong.medium.com/create-api-using-azure-function-with-python-and-azure-cosmos-db-afda09338d82)  
[VADER Sentiment Analysis](https://github.com/cjhutto/vaderSentiment)
[Queue input binding and DB query example](https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-cosmosdb-v2-input?tabs=python#queue-trigger-look-up-id-from-json-python)
[Non-string values dont work](https://stackoverflow.com/questions/48619140/azure-function-http-trigger-inputting-cosmos-db-document)
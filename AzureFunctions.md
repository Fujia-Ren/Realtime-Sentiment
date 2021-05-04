# Guideline for Azure Functions
## Useful commands
* `func azure functionapp fetch-app-settings TweetSentimentApp` is supposed to get the local.settings but I remember it making things complicated (it loaded the encrypted setttings?) so don't use this - just use the current `local.settings.json`.
## Azure Resource Organization 
* Resource Group: tweetsnetimentapp
  * App: TweetSentimentApp
  * Cosmos DB Account: maininstance
    * Database: main-database
      * Container: hashtags 
      * Container: main-container

## Functions
* sentiment_calc: http (text:text, hashtag:hashtag), container:hashtags -> container: hashtags
* fetchtweets: http -> http
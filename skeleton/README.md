# Two Databases
Two databases (containers, whatever - two types)  
* TEXT DB: Has the texts we could use for ML analysis  
* HASH DB: Has hashtag data entities, which has the count, sentiment value for each hashtag  
  
# Three Scripts  
Ran by Azure Function? Run Every 1 minute or so in the end, but let's just start with 24 hours (or whenever we call it)
* Acquire text: uses twitch api to get text and store it in TEXT DB
* Analyze text: get TEXTS from the TEXT DB analyze it, and update the hashtag entities in the HASH DB accordingly
* Disply: read hastag entities from HASH DB, and update the display accordingly
import logo from './logo.svg';
import './App.css';
import React, { useState, useEffect } from 'react';

import axios from 'axios';

function MostFrequent(){
  return axios
    .get('http://localhost:7071/api/Frontend?id=display_frequent&type=mylife')
    .then((response) => response.data);
}

function App() {

  const [data, setData] = useState();

  useEffect(() => {
      MostFrequent().then(data => setData(data));
  }, []);

  const dataSection = data 
    ? <HashTagList hashtags={data} />
    : <div id="data">Loading...</div>

  return (
    <div className="App">
      <header className="App-header">
        <p>
          Most Frequent Hashtags:
        </p>
        {dataSection}

      </header>
    </div>
  );
}

const HashTagList = ({ hashtags }) => {
  const hashTagSections = hashtags.map(hashtag => (
    <HashTagSection 
      tweets={hashtag.tweets}
      sentiment={hashtag.sentiment}
      frequency={hashtag.frequency}
      id={hashtag.id}
      key={hashtag.id}
    />
  ));

  return <div>{hashTagSections}</div>
};

const HashTagSection = ({ tweets, sentiment, frequency, id }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const handleClick = () => setIsExpanded(!isExpanded);
  const tweetList = tweets.map((tweet, idx) => <li key={idx}>{tweet}</li>);

  return (
    <div onClick={handleClick}>
      <h3>Hashtag: {id}</h3>
      <h3>Frequency: {frequency}</h3>
      <h3>Sentiment: {sentiment}</h3>
      {isExpanded && <ul>{tweetList}</ul>}
    </div>
  );
};

export default App;

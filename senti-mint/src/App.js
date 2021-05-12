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
    ? <HashtagList hashtags={data} />
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

const HashtagList = ({ hashtags }) => {
  const hashTagSections = hashtags.map(hashtag => (
    <HashtagSection 
      tweets={hashtag.tweets}
      sentiment={hashtag.sentiment}
      frequency={hashtag.frequency}
      id={hashtag.id}
      key={hashtag.id}
    />
  ));

  return <div>{hashTagSections}</div>
};

const HashtagSection = ({ tweets, sentiment, frequency, id }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const handleClick = () => setIsExpanded(!isExpanded);
  const tweetList = tweets.map((tweet, idx) => <li key={idx}>{tweet}</li>);

  let tweetListClassName = "hashtag-tweetlist";

  if (!isExpanded) {
    tweetListClassName += " hidden";
  }

  return (
    <div onClick={handleClick} className="hashtag-section">
      
      <div className="hashtag-box">
        <div className="idAndFrequency">
          <div className="hashtag-id">#{id}</div>
          <div className="hashtag-frequency">Frequency: {frequency}</div>
        </div>
        <div className="hashtag-sentiment"><br/>Sentiment: {sentiment}</div>
      </div>
      <ul className={tweetListClassName}>{tweetList}</ul>
    </div>
  );
};

export default App;

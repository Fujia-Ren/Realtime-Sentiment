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
    ? <ul>{data.map(item => <li>{item}</li>)}</ul>
    : <div id="data">Loading...</div>

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Most Frequent Hashtags:
        </p>
        {dataSection}

      </header>
    </div>
  );
}

export default App;

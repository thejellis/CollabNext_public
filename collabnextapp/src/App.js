import React, { useState, useEffect } from 'react';

import './App.css';

function App() {
  const [inputText, setInputText] = useState('');
  const [displayText, setDisplayText] = useState('');
  const [queryResults, setQueryResults] = useState('');
  const [isChecked, setIsChecked] = useState(false);
  const [selectedOption, setSelectedOption] = useState('');
  const [one, setOne] = useState('');
  const [two, setTwo] = useState('');
  const [three, setThree] = useState('');
  const [selectedTopicOption, setSelectedTopicOption] = useState('');
  const [topicOne, setTopicOne] = useState('');
  const [topicTwo, setTopicTwo] = useState('');
  const [topicThree, setTopicThree] = useState('');
  const [authorResults, setAuthorResults] = useState('');
  
  const handleInputChange = (event) => {
    setInputText(event.target.value);
  };

  const handleCheckboxChange = (event) => {
    setIsChecked(event.target.checked);
  };

  const handleSubmit = () => {
    fetch('http://localhost:5000/update-text', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ inputText, isChecked }),
    })
    .then(res => res.json())
    .then(data => {
      setDisplayText(data.updatedText);
      setQueryResults(data.queryResults);
    });
  };  

  const handleDropdownChange = (event) => {
    setSelectedOption(event.target.value)
  };

  const handleDropdownTopicChange = (event) => {
    setSelectedTopicOption(event.target.value)
  };

  const getInstitutions = () => {
    fetch('http://localhost:5000/get-institutions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    .then(res => res.json())
    .then(data => {
      setOne(data.one);
      setTwo(data.two);
      setThree(data.three);
    });
  };

  const getTopics = () => {
    fetch('http://localhost:5000/get-topics', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ selectedOption }),
    })
    .then(res => res.json())
    .then(data => {
      setTopicOne(data.one);
      setTopicTwo(data.two);
      setTopicThree(data.three);
    });
  };

  const getAuthors = () => {
    fetch('http://localhost:5000/get-authors', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ selectedTopicOption, selectedOption }),
    })
    .then(res => res.json())
    .then(data => {
      setAuthorResults(data.authors)
    });
  };

  return (
    <div className="App">
      <header className="App-header">
        <p>Enter a SPARQL Query Here!</p>
        <input
          type="text"
          value={inputText}
          placeholder="Enter Query Here!"
          onChange={handleInputChange}
        />
        <button onClick={handleSubmit}>
          Submit
        </button>
        <p>
          Unchecked box queries from SOA, checked box queries from Frink.
        </p>
        <input 
          type="checkbox"
          id="switch"
          checked={isChecked}
          onChange={handleCheckboxChange}
        />
        <p>Your Query: {displayText}</p>
        <p>Results: {queryResults}</p>
        <p>-------------------------------------------------</p>
        <div>
          <h2>Select an Option:</h2>
          <select value={selectedOption} onChange={handleDropdownChange} onClick={getInstitutions}>
            <option value="">Select...</option>
            <option value={one}>{one}</option>
            <option value={two}>{two}</option>
            <option value={three}>{three}</option>
          </select>
        </div>
        <div>
          <select value={selectedTopicOption} onChange={handleDropdownTopicChange} onClick={getTopics}>
            <option value="">Select...</option>
            <option value={topicOne}>{topicOne}</option>
            <option value={topicTwo}>{topicTwo}</option>
            <option value={topicThree}>{topicThree}</option>
          </select>
        </div>
        <button onClick={getAuthors}>
          Search
        </button>
        <p>{authorResults}</p>
      </header>
    </div>
  );
}

export default App;
import React, { useState } from 'react';
import './MainNavigation.css'; 
import NetworkMap from './NetworkMap.png';

const MainNavigation = () => {
  const [isNetworkMap, setIsNetworkMap] = useState(false);
  const [universityName, setUniversityName] = useState('');
  const [topicType, setTopicType] = useState('');
  const [institutionType, setInstitutionType] = useState('');
  const [researcherType, setResearcherType] = useState('');

  const handleToggle = () => {
    setIsNetworkMap(!isNetworkMap);
  };

  return (
    <div className="main-content">
      <div className="sidebar">
        <input
          type="text"
          value={universityName}
          onChange={(e) => setUniversityName(e.target.value)}
          placeholder="University Name"
          className="textbox"
        />
        <input
          type="text"
          value={topicType}
          onChange={(e) => setTopicType(e.target.value)}
          placeholder="Type Topic"
          className="textbox"
        />
        <select
          value={institutionType}
          onChange={(e) => setInstitutionType(e.target.value)}
          className="dropdown"
        >
          <option value="" disabled>Institution Type</option>
          <option value="HBCU">HBCU</option>
          <option value="HSI">HSI</option>
          <option value="University">University</option>
        </select>
        <input
          type="text"
          value={researcherType}
          onChange={(e) => setResearcherType(e.target.value)}
          placeholder="Type Researcher"
          className="textbox"
        />
        <button onClick={handleToggle}>
          {isNetworkMap ? 'See List Map' : 'See Network Map'}
        </button>
      </div>
      <div className="content">
        {isNetworkMap ? (
          <div className="network-map">
            <img src={NetworkMap} alt="Network Map" />
          </div>
        ) : (
          <div className="list-map">
            <h2>{universityName}</h2>
            <a href="http://ror.org/rorid">RORID</a><br />
            <a href="http://example.com">URL</a>
            <p>Total 20 people</p>
            <p>Total 50 works</p>
            <p>Total 70 citations</p>
            <p>Medicine: 200 people, 3000 works</p>
            <p>Engineering: 112 people, 2700 works</p>
            <p>Agriculture: 145 people, 2810 works</p>
            <a href="http://openalex.org">View on OpenAlex</a>
          </div>
        )}
      </div>
    </div>
  );
};

export default MainNavigation;

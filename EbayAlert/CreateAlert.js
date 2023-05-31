import React, { useState } from 'react';
import axios from 'axios';

const CreateAlert = () => {
  const [searchPhrase, setSearchPhrase] = useState('');
  const [email, setEmail] = useState('');
  const [frequency, setFrequency] = useState('');

  const handleCreateAlert = () => {
    axios.post('/api/alerts/', { searchPhrase, email, frequency })
      .then(response => {
        // Handle the success response
        console.log(response.data);
      })
      .catch(error => {
        // Handle the error response
        console.error(error);
      });
  };

  return (
    <div>
      <h2>Create Alert</h2>
      <input
        type="text"
        placeholder="Search Phrase"
        value={searchPhrase}
        onChange={(e) => setSearchPhrase(e.target.value)}
      />
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <select value={frequency} onChange={(e) => setFrequency(e.target.value)}>
        <option value="">Select Frequency</option>
        <option value="2">Every 2 minutes</option>
        <option value="10">Every 10 minutes</option>
        <option value="30">Every 30 minutes</option>
      </select>
      <button onClick={handleCreateAlert}>Create Alert</button>
    </div>
  );
};

export default CreateAlert;

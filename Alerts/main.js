import React, { useState } from 'react';
import axios from 'axios';

const AlertForm = () => {
  const [searchPhrase, setSearchPhrase] = useState('');
  const [email, setEmail] = useState('');
  const [frequency, setFrequency] = useState('');

  const handleFormSubmit = (e) => {
    e.preventDefault();
    const alertData = {
      search_phrase: searchPhrase,
      email,
      frequency,
    };

    axios.post('/api/create_alert/', alertData)
      .then((response) => {
        console.log(response.data);
        // Optionally, you can perform any additional actions after successful submission
      })
      .catch((error) => {
        console.error(error);
        // Optionally, you can handle any errors that occur during submission
      });

    setSearchPhrase('');
    setEmail('');
    setFrequency('');
  };

  return (
    <form onSubmit={handleFormSubmit}>
      <label>
        Search Phrase:
        <input type="text" value={searchPhrase} onChange={(e) => setSearchPhrase(e.target.value)} />
      </label>
      <br />
      <label>
        Email:
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
      </label>
      <br />
      <label>
        Frequency:
        <input type="number" value={frequency} onChange={(e) => setFrequency(e.target.value)} />
      </label>
      <br />
      <button type="submit">Create Alert</button>
    </form>
  );
};

export default AlertForm;

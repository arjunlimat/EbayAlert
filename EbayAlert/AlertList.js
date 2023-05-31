import React, { useEffect, useState } from 'react';
import axios from 'axios';

const AlertList = () => {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    axios.get('/api/alerts/')
      .then(response => {
        setAlerts(response.data);
      })
      .catch(error => {
        // Handle the error response
        console.error(error);
      });
  }, []);

  return (
    <div>
      <h2>Alert List</h2>
      {alerts.length > 0 ? (
        <ul>
          {alerts.map((alert) => (
            <li key={alert.id}>{alert.searchPhrase}</li>
          ))}
        </ul>
      ) : (
        <p>No alerts found.</p>
      )}
    </div>
  );
};

export default AlertList;

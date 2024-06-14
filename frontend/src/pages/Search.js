// App.js
import React from 'react';
import Sidebar from '../components/Sidebar';
import MainNavigation from '../components/MainNavigation';

const App = () => {
  return (
    <div style={styles.container}>
      <Sidebar />
      <MainNavigation />
    </div>
  );
};

const styles = {
  container: {
    display: 'flex',
  },
};

export default App;

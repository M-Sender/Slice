import React from 'react';
import './App.css';
import Import_Button from './components/ImportButton';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>
          <Import_Button/>
        </h1>
        <img className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          App
        </a>
      </header>
    </div>
  );
}



export default App;

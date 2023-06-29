import React from 'react';
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

import Button from '@mui/material/Button';

import './App.css';

function App() {
    function analyse() {
        console.log('analysing')
    }
    return (
        <div>
            <header>
                <h3>Emission Calculation Engine</h3>
                <Button variant="contained" onClick={analyse}>Hello World</Button>
            </header>
        </div>
    );
}

export default App;

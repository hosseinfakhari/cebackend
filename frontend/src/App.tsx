import React, {ChangeEvent, ChangeEventHandler, useRef, useState} from 'react';
import axios from "axios";
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

import Button from '@mui/material/Button';

import './App.css';

function App() {
    // const [file,setFile]= useState<File | undefined>(undefined  )
    const [fileSelected, setFileSelected] = React.useState<File>();
    const handleImageChange = function (e: React.ChangeEvent<HTMLInputElement>) {
        const fileList = e.target.files;

        if (!fileList) return;

        setFileSelected(fileList[0]);
    };

    const uploadFile = function (e: React.MouseEvent<HTMLSpanElement, MouseEvent>) {
        const formData = new FormData();
        formData.append("file", fileSelected as Blob, fileSelected?.name as string);
        console.log(Object.fromEntries(formData))
        const body = formData;

        axios.put("http://localhost:8000/api/v1/emission", body,
            {headers:{"Content-Type": "multipart/form-data"}})
            .then(function (response) {
                console.log(response);
            })
            .catch(function (response) {
                console.log(response);
            });
    }

    return (
        <div>
            <header>
                <h3>Emission Calculation Engine</h3>
                <input type="file"
                       accept="text/csv"
                       id="file"
                       name='fileee'
                       multiple={false}
                       onChange={handleImageChange}
                />
                <Button variant="contained" onClick={uploadFile}>Analyze</Button>
            </header>
        </div>
    );
}

export default App;

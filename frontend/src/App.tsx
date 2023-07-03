import React, {ChangeEvent, ChangeEventHandler, useRef, useState} from 'react';
import Box from '@mui/material/Box';
import {DataGrid, GridColDef, GridValueGetterParams} from '@mui/x-data-grid';

import axios from "axios";
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

import Button from '@mui/material/Button';

import './App.css';
import {Container, dividerClasses, Input} from "@mui/material";


interface Activity {
    id: number,
    activity: string,
    category: number,
    co2e: number,
    scope: number,
}

const columns: GridColDef[] = [
    {field: 'id', headerName: 'ID', width: 90, type: 'number',},
    {
        field: 'activity',
        headerName: 'Activity',
        width: 150,
    },
    {
        field: 'category',
        headerName: 'Category',
        width: 150,
        type: 'number',
        sortable: false,
    },
    {
        field: 'co2e',
        headerName: 'CO2e',
        type: 'number',
        width: 110,

    },
    {
        field: 'scope',
        headerName: 'Scope',
        sortable: false,
        width: 160,
        type: 'number',
    },
];

function App() {
    const [activityData, setActivityData] = React.useState<Activity[]>([])
    const [fileSelected, setFileSelected] = React.useState<File>();
    const handleFileChange = function (e: React.ChangeEvent<HTMLInputElement>) {
        const fileList = e.target.files;
        if (!fileList) return;
        setFileSelected(fileList[0]);
    };

    const uploadFile = function (e: React.MouseEvent<HTMLSpanElement, MouseEvent>) {
        const formData = new FormData();
        formData.append("file", fileSelected as Blob, fileSelected?.name as string);
        console.log(Object.fromEntries(formData))
        const body = formData;

        axios.put("api/v1/emission/upload", body,
            {headers: {"Content-Type": "multipart/form-data"}})
            .then(function (response) {
                console.log(response);
            })
            .catch(function (response) {
                console.log(response);
            });
    }

    const getData = function () {
        axios.get("api/v1/emission/activity_data/")
            .then(res => {
                // @ts-ignore
                console.log(res.data, 'data')
                setActivityData(res.data.results)
            })
            .catch(err => console.error(err))
    }

    return (
        <div>
            <Container maxWidth="lg">
                <header>
                    <h3>Emission Calculation Engine</h3>
                    <input type="file"
                           accept="text/csv"
                           id="file"
                           name='fileee'
                           multiple={false}
                           onChange={handleFileChange}
                    />
                    <Button variant="contained" onClick={uploadFile}>Upload Activity Data</Button>
                    <hr/>

                    <Input placeholder={"Filter By Scope"} type={"number"}/>
                    <Input placeholder={"Filter By Category"} type={"number"}/>&nbsp;
                    <Button variant="contained" onClick={getData}>Get Emission Data</Button>
                </header>

                <Box sx={{height: 400, width: '100%'}}>
                    <DataGrid
                        rows={activityData}
                        columns={columns}
                        initialState={{
                            pagination: {
                                paginationModel: {
                                    pageSize: 5,
                                },
                            },
                        }}
                        pageSizeOptions={[20]}
                        disableRowSelectionOnClick
                    />
                </Box>
            </Container>
        </div>
    );
}

export default App;

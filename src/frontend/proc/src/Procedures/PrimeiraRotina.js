import React, {useEffect, useState} from "react";
import {Box, CircularProgress, Container, FormControl, InputLabel, MenuItem, Select} from "@mui/material";

function PrimeiraRotina() {

    const [selectedCountry, setSelectedCountry] = useState("");

    const [procData, setProcData] = useState(null);
    const [data, setData] = useState(null);
    const [gqlData, setGQLData] = useState(null);
    useEffect(() => {
        fetch('http://localhost:20001/api/city/get/')
            .then(response => response.json())
            .then(jsonData => setData(jsonData));
    }, [])


    useEffect(() => {
        if (selectedCountry) {
          fetch(`http://localhost:20004/api/PrimeiraRotina?name=${selectedCountry}`)
            .then(response => response.json())
            .then(jsonData => setProcData(jsonData));
        }
        console.log(procData)
      }, [selectedCountry]);

    return (
        <>
            <h1>Primeira Rotina</h1>

            <Container maxWidth="100%"
                       sx={{backgroundColor: 'background.default', padding: "2rem", borderRadius: "1rem"}}>
                <Box>
                    <h2 style={{color: "white"}}>Options</h2>
                    <FormControl fullWidth>
                        <InputLabel id="countries-select-label">City</InputLabel>
                        <Select
                            labelId="countries-select-label"
                            id="demo-simple-select"
                            value={selectedCountry}
                            label="Country"
                            onChange={(e, v) => {setSelectedCountry(e.target.value)}}
                        >
                            <MenuItem value={""}><em>None</em></MenuItem>
                            {
                            data ?
                            data.map(data => <MenuItem key={data} value={data}>{data}</MenuItem>)
                                    :
                                selectedCountry ? <CircularProgress/> : "--"
                            }
                        </Select>
                    </FormControl>
                </Box>
            </Container>

            <Container maxWidth="100%" sx={{
                backgroundColor: 'info.dark',
                padding: "2rem",
                marginTop: "2rem",
                borderRadius: "1rem",
                color: "white"
            }}>
                <h2>Results <small>(PROC)</small></h2>
                {
                    procData ?
                        <ul>
                            {
                                procData.map(data => <li key={data}>{data}</li>)
                            }
                        </ul> :
                        procData ? <CircularProgress/> : "--"
                }
                <h2>Results <small>(GraphQL)</small></h2>
                {/* {
                    gqlData ?
                        <ul>
                            {
                                gqlData.map(data => <li>{data.team}</li>)
                            }
                        </ul> :
                        selectedCountry ? <CircularProgress/> : "--"
                } */}
            </Container>
        </>
    );
}

export default PrimeiraRotina;
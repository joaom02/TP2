import React, {useEffect, useState} from "react";
import {Box, CircularProgress, Container, FormControl, Input, InputLabel, MenuItem, Select} from "@mui/material";

function SegundaRotina() {

    const [selectedCountry, setSelectedCountry] = useState("");

    const [procData, setProcData] = useState(null);
    const [gqlData, setGQLData] = useState(null);


    useEffect(() => {
        if (selectedCountry) {
          fetch(`http://localhost:20004/api/SegundaRotina?name=${selectedCountry}`)
            .then(response => response.json())
            .then(jsonData => setProcData(jsonData));
        }
      }, [selectedCountry]);

    return (
        <>
            <h1>Segunda Rotina</h1>

            <Container maxWidth="100%"
                       sx={{backgroundColor: 'background.default', padding: "2rem", borderRadius: "1rem"}}>
                <Box>
                    <h2 style={{color: "white"}}>Options</h2>
                    <FormControl fullWidth>
                        <InputLabel id="countries-select-label">City</InputLabel>
                        <Input
                            labelId="countries-select-label"
                            id="demo-simple-select"
                            value={selectedCountry}
                            label="Country"
                            onChange={(e, v) => {setSelectedCountry(e.target.value)}}
                        >
                        </Input>
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

export default SegundaRotina;
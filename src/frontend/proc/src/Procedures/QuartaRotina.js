import React, {useEffect, useState} from "react";
import {
    CircularProgress,
    Container,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow
} from "@mui/material";

function QuartaRotina() {

    const [procData, setProcData] = useState(null);
    const [gqlData, setGQLData] = useState(null);


    useEffect(() => {
          fetch(`http://localhost:20004/api/QuartaRotina`)
            .then(response => response.json())
            .then(jsonData => setProcData(jsonData));
          fetch(`http://localhost:20003/graphql/QuartaRotina`)
            .then(response => response.json())
            .then(jsonData => setGQLData(jsonData));
      }, []);

    return (
        <>
            <h1>Quarta Rotina</h1>
            <Container maxWidth="100%" sx={{
                backgroundColor: 'info.dark',
                padding: "2rem",
                marginTop: "2rem",
                borderRadius: "1rem",
                color: "white"
            }}>
                <h2>Results <small>(PROC)</small></h2>
                <TableContainer component={Paper}>
                <Table sx={{minWidth: 650}} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell component="th" width={"1px"} align="center">ID</TableCell>
                            <TableCell>Job Name</TableCell>
                            <TableCell>Company Name</TableCell>
                            <TableCell>City Name</TableCell>
                            <TableCell>Summary</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {
                            procData ?
                                procData.map((row) => (
                                    <TableRow
                                        key={row.id}
                                        style={{background: "gray", color: "black"}}
                                    >
                                        <TableCell component="td" align="center">{row.id}</TableCell>
                                        <TableCell component="td" scope="row">
                                            {row.name}
                                        </TableCell>
                                        <TableCell component="td" align="center" scope="row">
                                            {row.companyname}
                                        </TableCell>
                                        <TableCell component="td" align="center" scope="row">
                                            {row.cityname}
                                        </TableCell>
                                        <TableCell component="td" align="center" scope="row">
                                            {row.summary}
                                        </TableCell>
                                    </TableRow>
                                ))
                                :
                                <TableRow>
                                    <TableCell colSpan={3}>
                                        <CircularProgress/>
                                    </TableCell>
                                </TableRow>
                        }
                    </TableBody>
                </Table>
            </TableContainer>
                <h2>Results <small>(GraphQL)</small></h2>
                <TableContainer component={Paper}>
                <Table sx={{minWidth: 650}} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell component="th" width={"1px"} align="center">ID</TableCell>
                            <TableCell>Job Name</TableCell>
                            <TableCell>Company Name</TableCell>
                            <TableCell>City Name</TableCell>
                            <TableCell>Summary</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {
                            gqlData ?
                                JSON.parse(gqlData).map((row) => (
                                    <TableRow
                                        key={row.id}
                                        style={{background: "gray", color: "black"}}
                                    >
                                        <TableCell component="td" align="center">{row.id}</TableCell>
                                        <TableCell component="td" scope="row">
                                            {row.name}
                                        </TableCell>
                                        <TableCell component="td" align="center" scope="row">
                                            {row.companyname}
                                        </TableCell>
                                        <TableCell component="td" align="center" scope="row">
                                            {row.cityname}
                                        </TableCell>
                                        <TableCell component="td" align="center" scope="row">
                                            {row.summary}
                                        </TableCell>
                                    </TableRow>
                                ))
                                :
                                <TableRow>
                                    <TableCell colSpan={3}>
                                        <CircularProgress/>
                                    </TableCell>
                                </TableRow>
                        }
                    </TableBody>
                </Table>
            </TableContainer>
            </Container>
        </>
    );
}

export default QuartaRotina;
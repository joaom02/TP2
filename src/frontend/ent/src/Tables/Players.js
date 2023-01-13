import {useEffect, useState} from "react";
import {
    CircularProgress,
    Pagination,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow
} from "@mui/material";

function Players() {

    const PAGE_SIZE = 10;
    const [page, setPage] = useState(1);
    const [data, setData] = useState(null);

    useEffect(() => {
        fetch('http://localhost:20001/api/jobs/get/')
            .then(response => response.json())
            .then(jsonData => setData(jsonData));
    }, [])

    const [maxDataSize, setMaxDataSize] = useState(200);





    // useEffect(() => {
    //     //!FIXME: this is to simulate how to retrieve data from the server
    //     //!FIXME: the entities server URL is available on process.env.REACT_APP_API_ENTITIES_URL
    //     setData(null);
    //     setTimeout(() => {
    //         console.log(`fetching from ${process.env.REACT_APP_API_ENTITIES_URL}`)
    //         setData(DEMO_PLAYERS.filter((item, index) => Math.floor(index / PAGE_SIZE) === (page - 1)));
    //     }, 500);
    // }, [page])

    return (
        <>
            <h1>Jobs</h1>

            <TableContainer component={Paper}>
                <Table sx={{minWidth: 650}} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell component="th" width={"1px"} align="center">ID</TableCell>
                            <TableCell>Job Name</TableCell>
                            <TableCell>Summary</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {
                            data ?
                                data.map((row) => (
                                    <TableRow
                                        key={row.id}
                                        style={{background: "gray", color: "black"}}
                                    >
                                        <TableCell component="td" align="center">{row.id}</TableCell>
                                        <TableCell component="td" scope="row">
                                            {row.name}
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
            {
                maxDataSize && <div style={{background: "black", padding: "1rem"}}>
                    <Pagination style={{color: "black"}}
                                variant="outlined" shape="rounded"
                                color={"primary"}
                                onChange={(e, v) => {
                                    setPage(v)
                                }}
                                page={page}
                                count={Math.ceil(maxDataSize / PAGE_SIZE)}
                    />
                </div>
            }


        </>
    );
}

export default Players;

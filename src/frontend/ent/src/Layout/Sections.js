import Jobs from "../Tables/Jobs";
import Cities from "../Tables/Cities";
import Companies from "../Tables/Companies";


const Sections = [

    {
        id: "jobs",
        label: "Jobs",
        content: <Jobs/>
    },

    {
        id: "companies",
        label: "Companies",
        content: <Companies/>
    },

    {
        id: "cities",
        label: "Cities",
        content: <Cities/>
    }

];

export default Sections;
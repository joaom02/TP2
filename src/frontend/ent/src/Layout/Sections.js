import Jobs from "../Tables/Jobs";
import Cities from "../Tables/Cities";
import Companies from "../Tables/Companies";


const Sections = [

    {
        id: "jobs",
        label: "JObs",
        content: <Jobs/>
    },

    {
        id: "teams",
        label: "Teams",
        content: <Companies/>
    },

    {
        id: "cities",
        label: "Cities",
        content: <Cities/>
    }

];

export default Sections;
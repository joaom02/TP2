import PrimeiraRotina from "../Procedures/PrimeiraRotina";
import SegundaRotina from "../Procedures/SegundaRotina";
import TerceiraRotina from "../Procedures/TerceiraRotina";
import QuartaRotina from "../Procedures/QuartaRotina";
import QuintaRotina from "../Procedures/QuintaRotina";

const Sections = [

    {
        id: "primeiraRotina",
        label: "Trabalhos disponíveis numa determinada Cidade",
        content: <PrimeiraRotina/>
    },

    {
        id: "segundaRotina",
        label: "Companhias com determinada Rating",
        content: <SegundaRotina/>
    },
    {
        id: "terceiraRotina",
        label: "Trabalhos disponíveis numa determinada Companhia",
        content: <TerceiraRotina/>
    },
    {
        id: "quartaRotina",
        label: "Trabalho Aleatório",
        content: <QuartaRotina/>
    },    {
        id: "quintaRotina",
        label: "Companhias disponíveis numa determinada Cidade",
        content: <QuintaRotina/>
    },

];

export default Sections;
import "./App.css";
import axios from "axios";
import { useState, useEffect } from "react";
import Test from "./components/testComponent";

function App() {
  const [drugList, setDrugList] = useState([]);

  const loadDrugList = () => {
    axios
      .get("https://vet-anes.herokuapp.com/protocol/drugs") // deployed
      // .get("http://127.0.0.1:8000/protocol/drugs")  // local development
      .then((response) => {
        const updatedDrugList = response.data.map((drug) => {
          return {
            id: drug.id,
            name: drug.name,
            concentration: drug.concentration,
            concentration_units: drug.concentration_units,
            route: drug.route,
          };
        });
        setDrugList(updatedDrugList);
        // console.log(`🌸 ${JSON.stringify(drugList)}`);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  useEffect(loadDrugList, []);

  return (
    <div>
      <Test drugList={drugList} loadDrugList={loadDrugList}></Test>
    </div>
  );
}

export default App;

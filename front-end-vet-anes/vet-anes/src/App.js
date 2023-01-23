import "./App.css";
import axios from "axios";

function App() {
  axios
    .get()
    .then((response) => {
      console.log(`${JSON.stringify(response)}`);
      // DO STUFF
    })
    .catch((error) => {
      console.log(error);
    });

  return <h1>Hello!</h1>;
}

export default App;

import { useEffect, useState } from "react";
import api from "./services/api";

function App() {
  const [health, setHealth] = useState({
    status: "",
    message: "",
  });

  useEffect(() => {
    api
      .get("/health")
      .then((response) => {
        setHealth(response.data);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, []);

  return (
    <>
      <h2>React Main App</h2>
      <p>This value is coming from SQL to say BE is working</p>
      <p>
        <strong>Status:</strong> {health.status}
      </p>
      <p>
        <strong>Message:</strong> {health.message}
      </p>
    </>
  );
}

export default App;

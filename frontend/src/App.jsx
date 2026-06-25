import "./App.css";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import FraudQueue from "./pages/FraudQueue";

export default function App() {

    const token = localStorage.getItem("token");

    const page = localStorage.getItem("page") || "dashboard";

    if (!token) {
        return <Login />;
    }

    if (page === "threat") {
        return <FraudQueue />;
    }

    return <Dashboard />;
}
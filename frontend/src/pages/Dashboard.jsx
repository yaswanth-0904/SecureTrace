import { useEffect, useState } from "react";
import api from "../services/api";
import Sidebar from "../components/Sidebar";

function Dashboard() {

    const [stats, setStats] = useState(null);

    useEffect(() => {

        const loadDashboard = async () => {

            try {

                const token = localStorage.getItem("token");

                const response = await api.get(
                    "/dashboard",
                    {
                        params: {
                            token: token
                        }
                    }
                );

                console.log(response.data);

                setStats(response.data);

            } catch (error) {

                console.log(error);
            }
        };

        loadDashboard();

    }, []);

    if (!stats) {

        return (
            <h2>
                Loading Dashboard...
            </h2>
        );
    }

    return (

        <div className="layout">

            <Sidebar />

            <div className="content">

                <div className="dashboard">

                    <h1>
                        Securetrace Dashboard
                    </h1>

                    <div className="cards">

                        <div className="card">
                            <h3>Assets Tracked</h3>
                            <h1>{stats.total_dna_records}</h1>
                        </div>

                        <div className="card">
                            <h3>Threat Assets</h3>
                            <h1>{stats.Threat_Assets_records}</h1>
                        </div>

                        <div className="card">
                            <h3>Frozen</h3>
                            <h1>{stats.frozen_records}</h1>
                        </div>

                        <div className="card">
                            <h3>Recovered</h3>
                            <h1>{stats.recovered_records}</h1>
                        </div>

                        <div className="card">
                            <h3>Recovered Value</h3>
                            <h1>₹{stats.total_recovered_amount}</h1>
                        </div>

                    </div>

                </div>

            </div>

        </div>

    );
}

export default Dashboard;
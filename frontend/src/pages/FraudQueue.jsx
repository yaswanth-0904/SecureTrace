import { useEffect, useState } from "react";
import api from "../services/api";
import Sidebar from "../components/Sidebar";

function FraudQueue() {
    const [records, setRecords] = useState([]);
    const [selectedDNA, setSelectedDNA] = useState(null);
    const [familyTree, setFamilyTree] = useState(null);
    const [expandedDNA, setExpandedDNA] = useState(null);

    useEffect(() => {
        const loadFraudQueue = async () => {
            try {
                const token = localStorage.getItem("token");
                const response = await api.get("/fraud-queue", {
                    params: { token: token }
                });
                console.log("RESPONSE DATA");
                console.log(response.data);
                setRecords(response.data);
                console.log("Threat Queue Data:");
                console.log(response.data);
                console.log(response.data.length);
            } catch (error) {
                console.log(error);
            }
        };
        loadFraudQueue();
    }, []);

    const InspectDNA = async (dnaCode) => {
        try {
            const response = await api.get(`/trace/${dnaCode}`);
            setSelectedDNA(response.data);
        } catch (error) {
            console.log(error);
        }
    };

    const freezeDNA = async (dnaCode) => {
        try {
            const token = localStorage.getItem("token");
            await api.post(`/freeze-dna/${dnaCode}`, {}, {
                params: { token: token }
            });

            setRecords(
                records.map((item) =>
                    item.dna_code === dnaCode
                        ? { ...item, status: "FROZEN" }
                        : item
                )
            );
            
        } catch (error) {
            console.log(error);
            alert(JSON.stringify(error.response?.data));
        }
    };
    const recoverDNA = async (dnaCode) => {

    try {

        const token =
            localStorage.getItem(
                "token"
            );

        await api.post(
            `/recover-dna/${dnaCode}`,
            {},
            {
                params: {
                    token: token
                }
            }
        );

        setRecords(
            records.map(
                (item) =>
                    item.dna_code === dnaCode
                        ? {
                              ...item,
                              status: "RECOVERED"
                          }
                        : item
            )
        );

    } catch (error) {

        console.log(error);

        alert(
            JSON.stringify(
                error.response?.data
            )
        );
    }
};
const traceDNA = async (dnaCode) => {

    try {

        const response =
            await api.get(
                `/trace-full-family/${dnaCode}`
            );

        setFamilyTree(
            response.data
        );

        setExpandedDNA(
            dnaCode
        );

    } catch (error) {

        console.log(error);
    }
};
    return (
        <div className="layout">
            <Sidebar />

            <div className="content">
                <div className="page-header">

    <h1>Threat Queue</h1>

    <div className="dna-badge">
        {records.length} DNA Records
    </div>

</div>

                <table className="fraud-table">
                    <thead>
                        <tr>
                            <th>Asset ID</th>
                            <th>Amount</th>
                            <th>Threat Score</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {records.map((item, index) => (
                            <tr key={index}>
                                <td>
 <div className="dna-wrapper">

    <span className="dna-code">

       🧬  

        {item.dna_code}

    </span>

</div>
                                </td>
                                <td>₹{item.amount}</td>
                                <td>
                                    <span
                                        className={
                                            item.risk_score >= 80
                                                ? "risk-high"
                                                : item.risk_score >= 50
                                                ? "risk-medium"
                                                : "risk-low"
                                        }
                                    >
                                        {item.risk_score}
                                    </span>
                                </td>
                                <td>
                                    <div className="status-container">
                                        <span
                                            className={
                                                item.status === "FROZEN"
                                                    ? "status-dot-red"
                                                    : "status-dot-green"
                                            }
                                        ></span>
                                        <span className="status-text">
                                            <span className="status-text">

    {item.status === "FROZEN"
        ? "Frozen"
        : item.status === "RECOVERED"
        ? "Recovered"
        : "Active"
    }

</span>
                                        </span>
                                    </div>
                                </td>
                                <td>
                                    <button
                                        className="Inspect-btn"
                                        onClick={() => InspectDNA(item.dna_code)}
                                    >
                                        Inspect
                                    </button>
                                    <button
                                        className="freeze-btn"
                                        disabled={item.status === "FROZEN"}
                                        onClick={() => freezeDNA(item.dna_code)}
                                    >
                                        freeze
                                    </button>
                                    <button
    className="recover-btn"
    disabled={
        item.status === "RECOVERED"
    }
    onClick={() =>
        recoverDNA(
            item.dna_code
        )
    }
>
    Recover
</button>
                                    <button
    className="trace-btn"
    onClick={() =>
        traceDNA(
            item.dna_code
        )
    }
>
    trace
</button>
                                </td>
                            </tr>
                        
                        ))}
                    </tbody>
                </table>

                {selectedDNA && (
                    <div className="modal-overlay">
                        <div className="modal">
                            <h2>Asset Intelligence Report</h2>

                            <p>
                                <strong>Asset ID</strong>
                                <span className="value">
                                    {selectedDNA.dna_code}
                                </span>
                            </p>

                            <p>
                                <strong>Amount</strong>
                                <span className="value">
                                    ₹{selectedDNA.amount}
                                </span>
                            </p>

                            <p>
                                <strong>Threat Score</strong>
                                <span className="value">
                                    {selectedDNA.risk_score}
                                </span>
                            </p>

                            <p>
                                <strong>Status</strong>
                                <span className="value">
                                    {selectedDNA.status}
                                </span>
                            </p>

                            <p>
                                <strong>Remaining</strong>
                                <span className="value">
                                    ₹{selectedDNA.remaining_amount || selectedDNA.remaining}
                                </span>
                            </p>

                            <p>
                                <strong>Recovered</strong>
                                <span className="value">
                                    ₹{selectedDNA.recovered_amount || 0}
                                </span>
                            </p>

                            <p>
                                <strong>Transaction ID</strong>
                                <span className="value">
                                    {selectedDNA.transaction_id}
                                </span>
                            </p>

                            <button
                                className="Inspect-btn"
                                style={{ marginTop: "15px" }}
                                onClick={() => setSelectedDNA(null)}
                            >
                                Close
                            </button>
                        </div>
                    </div>
                )}
            </div>
            {familyTree && (

<div className="modal-overlay">

    <div className="modal-card">

        <h1>
            Asset Flow Explorer
        </h1>

        <h3>
            Primary Asset
        </h3>

        <div className="tree-root">
    🧬 {familyTree.root_dna}
        </div>
        

        <h3>
            children
        </h3>

        {familyTree.family_tree.map(
            (child, index) => (

                <div
                    key={index}
                    className="child-card"
                >
                    {child.dna_code}
                </div>

            )
        )}

        <button
            className="close-btn"
            onClick={() =>
                setFamilyTree(
                    null
                )
            }
        >
            Close
        </button>

    </div>

</div>

)}
        </div>
    );
}

export default FraudQueue;
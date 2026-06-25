import { useState } from "react";
import api from "../services/api";

function Login() {

    const [email, setEmail] = useState("");

    const login = async () => {

        try {

            const response = await api.post(
                "/login",
                {
                    email: email
                }
            );

            localStorage.setItem(
                "token",
                response.data.token
            );

            localStorage.setItem(
                "role",
                response.data.role
            );

            alert(
                "Access Granted"
            );

            window.location.reload();

        } catch (error) {

            console.log(error);

            alert(
                JSON.stringify(
                    error.response?.data
                )
            );
        }
    };

    return (

        <div className="login-container">

            <div className="login-card">

                <h1>
                    Securetrace
                </h1>

                <p className="login-subtitle">
                    Transaction Intelligence Platform
                </p>

                <input
                    type="email"
                    placeholder="Enter Email Address"
                    value={email}
                    onChange={(e) =>
                        setEmail(e.target.value)
                    }
                />

                <button
                    onClick={login}
                >
                    Secure Access
                </button>

                <div className="security-features">

                    <div>✓ Asset Monitoring</div>

                    <div>✓ Threat Intelligence</div>

                    <div>✓ Recovery Operations</div>

                    <div>✓ Audit Logging</div>

                </div>

            </div>

        </div>

    );
}

export default Login;
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { ApiError } from "../api/client";

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      await login(username, password);
      navigate("/");
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Login fehlgeschlagen");
    }
  }

  return (
    <div className="auth-page">
      <h1>Anmelden</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Benutzername
          <input value={username} onChange={(e) => setUsername(e.target.value)} required />
        </label>
        <label>
          Passwort
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </label>
        {error && <p className="form-error">{error}</p>}
        <button type="submit">Anmelden</button>
      </form>
      <p>
        Noch kein Konto? <Link to="/registrieren">Jetzt registrieren</Link>
      </p>
    </div>
  );
}

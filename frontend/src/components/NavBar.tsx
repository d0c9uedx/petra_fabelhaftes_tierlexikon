import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function NavBar() {
  const { user, logout } = useAuth();

  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand">
        🦔 Petras fabelhaftes Tierlexikon
      </Link>
      {user && (
        <div className="navbar-links">
          <Link to="/">Kategorien</Link>
          <Link to="/tages-tier">Tages-Tier</Link>
          <Link to="/entdecken">Entdecken</Link>
          <Link to="/quiz">Quiz</Link>
          <Link to="/profil">Profil</Link>
          <span className="navbar-user">{user.username}</span>
          <button onClick={logout}>Abmelden</button>
        </div>
      )}
    </nav>
  );
}

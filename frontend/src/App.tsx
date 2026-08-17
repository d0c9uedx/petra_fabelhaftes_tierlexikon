import { Outlet } from "react-router-dom";
import NavBar from "./components/NavBar";

export default function App() {
  return (
    <div className="app">
      <NavBar />
      <main className="app-content">
        <Outlet />
      </main>
    </div>
  );
}

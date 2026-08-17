import { createBrowserRouter } from "react-router-dom";
import App from "./App";
import ProtectedRoute from "./components/ProtectedRoute";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import CategoryOverviewPage from "./pages/CategoryOverviewPage";
import AnimalListPage from "./pages/AnimalListPage";
import AnimalDetailPage from "./pages/AnimalDetailPage";
import DailyAnimalPage from "./pages/DailyAnimalPage";
import DiscoverPage from "./pages/DiscoverPage";
import QuizPage from "./pages/QuizPage";
import ProfilePage from "./pages/ProfilePage";

export const router = createBrowserRouter([
  {
    element: <App />,
    children: [
      { path: "/login", element: <LoginPage /> },
      { path: "/registrieren", element: <RegisterPage /> },
      {
        element: <ProtectedRoute />,
        children: [
          { path: "/", element: <CategoryOverviewPage /> },
          { path: "/kategorie/:category", element: <AnimalListPage /> },
          { path: "/tier/:id", element: <AnimalDetailPage /> },
          { path: "/tages-tier", element: <DailyAnimalPage /> },
          { path: "/entdecken", element: <DiscoverPage /> },
          { path: "/quiz", element: <QuizPage /> },
          { path: "/profil", element: <ProfilePage /> },
        ],
      },
    ],
  },
]);

import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./contexts/AuthContext";
import { LanguageProvider } from "./contexts/LanguageContext";
import { Toaster } from "./components/ui/toaster";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Home from "./pages/Home";
import Boutique from "./pages/Boutique";
import Login from "./pages/Login";
import Checkout from "./pages/Checkout";
import Dashboard from "./pages/Dashboard";
import Admin from "./pages/Admin";
import ProtectionCharter from "./pages/ProtectionCharter";
import CanalDetails from "./pages/CanalDetails";
import Subscription from "./pages/Subscription";
import BotPreorder from "./pages/BotPreorder";
import Contest from "./pages/Contest";
import Bonus from "./pages/Bonus";
import AboutUs from "./pages/AboutUs";

function App() {
  return (
    <LanguageProvider>
      <AuthProvider>
        <BrowserRouter>
          <div className="App">
            <Navbar />
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/boutique" element={<Boutique />} />
              <Route path="/login" element={<Login />} />
              <Route path="/checkout" element={<Checkout />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/admin" element={<Admin />} />
              <Route path="/subscription" element={<Subscription />} />
              <Route path="/bot-preorder" element={<BotPreorder />} />
              <Route path="/contest" element={<Contest />} />
              <Route path="/bonus" element={<Bonus />} />
              <Route path="/about-us" element={<AboutUs />} />
              <Route path="/protection-charter" element={<ProtectionCharter />} />
              <Route path="/canal/:canalName" element={<CanalDetails />} />
            </Routes>
            <Footer />
            <Toaster />
          </div>
        </BrowserRouter>
      </AuthProvider>
    </LanguageProvider>
  );
}

export default App;

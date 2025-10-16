import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./contexts/AuthContext";
import { Toaster } from "./components/ui/toaster";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Home from "./pages/Home";
import Boutique from "./pages/Boutique";
import Login from "./pages/Login";
import Checkout from "./pages/Checkout";
import Dashboard from "./pages/Dashboard";

function App() {
  return (
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
          </Routes>
          <Footer />
          <Toaster />
        </div>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;

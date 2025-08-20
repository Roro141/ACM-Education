// App.tsx
import { Suspense, lazy } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

// Lazy load pages
const Home = lazy(() => import("./pages/Home"));
const Login = lazy(() => import("./pages/Login"));
const MentorView = lazy(() => import("./pages/MentorView"));
const MenteeView = lazy(() => import("./pages/MenteeView"));

function App() {
  return (
    <Router>
      {/* Suspense wraps all lazy components and shows a fallback until loaded */}
      <Suspense fallback={<div className="p-6 text-center">Loading...</div>}>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/home" element={<Home />} />
          <Route path="/mentee" element={<MenteeView />} />
          <Route path="/mentor" element={<MentorView />} />
        </Routes>
      </Suspense>
    </Router>
  );
}

export default App;

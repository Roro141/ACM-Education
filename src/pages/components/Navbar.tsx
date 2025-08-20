// src/components/Navbar.tsx
import { useState } from "react";
import { Link } from "react-router-dom";

const mentee_user = {
    'token':'AAAAAA',
    'mpStatus':'mentee',
    'session': true
}

const mentor_user= {
    'token':'AAAAA1',
    'mpStatus':'mentor',
    'session': true
}

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="fixed top-4 left-1/2 transform -translate-x-1/2 bg-emerald-600 shadow-lg rounded-2xl z-50 w-[90%] max-w-6xl">
  <div className="max-w-7xl mx-auto px-6">
    <div className="flex justify-between h-16">
      {/* Logo */}
      <div className="flex items-center">
        <Link to="/" className="text-2xl font-bold text-indigo-600">
          MyApp
        </Link>
      </div>

      {/* Desktop Menu */}
      <div className="hidden md:flex space-x-8 items-center">
        <Link to="/" className="text-gray-700 hover:text-indigo-600">
          Home
        </Link>
        <Link to="/home" className="text-gray-700 hover:text-indigo-600">
          About
        </Link>
        <Link to="/mentor" className="text-gray-700 hover:text-indigo-600">
          Check Mentee Progress
        </Link>
        <Link to="/mentee" className="text-gray-700 hover:text-indigo-600">
          Check Mentor Progress
        </Link>
      </div>

      {/* Mobile Menu Button */}
      <div className="flex md:hidden items-center">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="text-gray-700 hover:text-indigo-600 font-bold text-xl"
        >
          {isOpen ? "✕" : "☰"}
        </button>
      </div>
    </div>
  </div>
</nav>

  );
}

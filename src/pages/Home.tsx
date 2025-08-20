// src/pages/Home.tsx
import Navbar from "./components/Navbar";
import { useEffect, useState } from "react";

type ProgressItem = {
  id: number;
  label: string;
  completed: boolean;
};

export default function Home() {
  const [progress, setProgress] = useState<ProgressItem[]>([]);

  // Mock API call
  useEffect(() => {
    // Later replace with fetch("/api/progress")
    setProgress([
      { id: 1, label: "Attend kickoff event", completed: true },
      { id: 2, label: "Submit required materials", completed: false },
      { id: 3, label: "Complete first milestone", completed: false },
    ]);
  }, []);

  return (
    <>
      <Navbar />
      <main className="pt-24 px-6 max-w-6xl mx-auto space-y-12">
        {/* Quick Links */}
        <section>
          <h2 className="text-2xl font-bold mb-4 text-gray-800">Quick Links</h2>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <a
              href="https://example.com/docs"
              target="_blank"
              className="p-4 rounded-xl shadow hover:shadow-md transition bg-white"
            >
              📘 Documentation
            </a>
            <a
              href="https://example.com/community"
              target="_blank"
              className="p-4 rounded-xl shadow hover:shadow-md transition bg-white"
            >
              💬 Community
            </a>
            <a
              href="https://example.com/support"
              target="_blank"
              className="p-4 rounded-xl shadow hover:shadow-md transition bg-white"
            >
              🛠️ Support
            </a>
          </div>
        </section>

        {/* User Progress */}
        <section>
          <h2 className="text-2xl font-bold mb-4 text-gray-800">Your Progress</h2>
          <div className="space-y-3">
            {progress.map((item) => (
              <div
                key={item.id}
                className="flex items-center justify-between p-4 rounded-xl shadow bg-white"
              >
                <span className="text-gray-700">{item.label}</span>
                {item.completed ? (
                  <span className="text-green-600 font-semibold">✔ Done</span>
                ) : (
                  <span className="text-red-500 font-semibold">⏳ Pending</span>
                )}
              </div>
            ))}
          </div>
        </section>

        {/* Upcoming Events */}
        <section>
          <h2 className="text-2xl font-bold mb-4 text-gray-800">Upcoming Events</h2>
          <div className="rounded-xl overflow-hidden shadow bg-white">
            {/* Embed Google Calendar (public) */}
            <iframe
              src="https://calendar.google.com/calendar/embed?src=YOUR_CALENDAR_ID&ctz=America%2FNew_York"
              style={{ border: 0 }}
              width="100%"
              height="600"
              frameBorder="0"
              scrolling="no"
              title="Upcoming Events"
            ></iframe>
          </div>
        </section>
      </main>
    </>
  );
}

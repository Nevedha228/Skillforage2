import { useState } from "react";
import { Outlet } from "react-router-dom";
import { Sidebar } from "./Sidebar";
import { Navbar } from "./Navbar";

export function AppLayout() {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <div className="app-layout">
      <Sidebar mobileOpen={mobileOpen} onClose={() => setMobileOpen(false)} />
      <div className="main-wrapper">
        <Navbar onToggleMobile={() => setMobileOpen((open) => !open)} />
        <main className="page-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

export default AppLayout;

import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router-dom";

import { AssetListPage } from "./pages/AssetListPage";
import { AssetRequestPage } from "./pages/AssetRequestPage";
import { MyRequestsPage } from "./pages/MyRequestsPage";
import "./index.css";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AssetListPage />} path="/" />
        <Route element={<MyRequestsPage />} path="/my-requests" />
        <Route element={<AssetRequestPage />} path="/requests/:assetId" />
      </Routes>
    </BrowserRouter>
  );
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

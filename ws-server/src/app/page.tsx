"use client";

import { useEffect, useState } from "react";
import { socket } from "../socket";

export default function Home() {
  const [isConnected, setIsConnected] = useState(false);
  const [transport, setTransport] = useState("N/A");
  const [wallbActive, setWallbActive] = useState(false);

  const status = (status: string) => {
    console.log(status);
    if (JSON.parse(status).wallB === "active") {
      setWallbActive(true);
    }
  }

  useEffect(() => {
    if (socket.connected) {
      onConnect();
    }

    function onConnect() {
      setIsConnected(true);
      setTransport(socket.io.engine.transport.name);

      socket.io.engine.on("upgrade", (transport) => {
        setTransport(transport.name);
      });
    }

    function onDisconnect() {
      setIsConnected(false);
      setTransport("N/A");
    }

    socket.on("connect", onConnect);
    socket.on("disconnect", onDisconnect);

    socket.on("status", status);

    socket.emit("auth", "wallB");

    return () => {
      socket.off("connect", onConnect);
      socket.off("disconnect", onDisconnect);
    };
  }, []);

  return (
    <div>
      <p>{wallbActive ? "Wall-B Active!" : "Wall-B Inactive"}</p>
      <p>Status: { isConnected ? "connected" : "disconnected" }</p>
      <p>Transport: { transport }</p>
    </div>
  );
}
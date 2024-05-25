"use client";

import { useEffect, useState } from "react";
import { socket } from "../socket";
import { ChakraProvider } from '@chakra-ui/react'
import { Switch } from '@chakra-ui/react'
import Image from 'next/image'
import Joystick from "./Joystick";
import { ArrowForwardIcon } from '@chakra-ui/icons'

export default function Home() {
  const [isConnected, setIsConnected] = useState(false);
  const [transport, setTransport] = useState("N/A");
  const [wallbActive, setWallbActive] = useState(false);
  const [autocontrol, setAutocontrol] = useState(false);

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

    socket.emit("auth", "client");

    return () => {
      socket.off("connect", onConnect);
      socket.off("disconnect", onDisconnect);
    };
  }, []);

  return (
    <ChakraProvider>
      <div>
        <div className="main-header">
          <h2 className="main-title">
          <Image className="img" src="/emojis/robot.png" alt="Washing machine" width={52} height={52}  />
          <span>Wall-B Controls</span>
          </h2>
          <p className="wallbstat-cont">
            Wall-B {
            wallbActive ? 
            <span className="wallbstatus"><span className="status inactive"></span> Inactive</span> :
            <span className="wallbstatus"><span className="status active"></span> Active</span>
            }
          </p>
        </div>
        <div className="mode-cont">
          <p>
            <span className={`controlopt ${!autocontrol ? 'active' : ''}`}>Manual control</span>
            <Switch id='autocontrol' colorScheme='teal' isChecked={autocontrol} />
            <span className={`controlopt ${autocontrol ? 'active' : ''}`}>Autopilot</span>
          </p>
        </div>
        <div className="box">
        <h2>Server</h2>
        <p className="small">Status: { isConnected ? <span style={{color: "rgb(20, 220, 20)"}}>connected</span> : <span style={{color: "rgb(220, 20, 20)"}}>disconnected</span> }</p>
        <p className="small">Transport: <span style={{color: "rgb(140, 140, 140)"}}>{ transport }</span></p>
        </div>
        <Joystick />
        <div className="box">
          <h2>Actions</h2>
          <button className="btn">
            <Image className="img" src="/emojis/washing-machine.png" alt="Washing machine" width={20} height={20}  />
            I'm Stuck
          </button>
        </div>
        <div className="box">
          <h2>Say something</h2>
          <form className="message" action="">
            <input type="text" />
            <div className="button-cont">
              <button className="btn">
                Send
                <ArrowForwardIcon className="" w={4} h={4} />
            </button>
            </div>
          </form>
        </div>
      </div>
    </ChakraProvider>
  );
}
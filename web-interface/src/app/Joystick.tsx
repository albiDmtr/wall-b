"use client";
import { sendCommand } from "./commands";
import { useEffect, useState, useRef, use } from "react";
import { ArrowLeftIcon, ChevronLeftIcon } from "@chakra-ui/icons";

const Joystick = () => {
  const [isMouseDown, setIsMouseDown] = useState(false);
  const [angle, setAngle] = useState(0);
  const [distance, setDistance] = useState(0);
  const [keysPressed, setKeysPressed] = useState(0);
  const [joystickPointerStyle, setJoystickPointerStyle] = useState({});

  const joystickInner = useRef<HTMLDivElement | null>(null);
  const joystickPointer = useRef<HTMLDivElement | null>(null);
  const lastSendTime = useRef<number>(0);
  const throttleDelay = 50; // 50ms throttle - adjust as needed

  const handleMouseMove = (e: any) => {
    const rect = e.target.parentNode.getBoundingClientRect();
    const clientX = e.clientX || e.touches[0].clientX;
    const clientY = e.clientY || e.touches[0].clientY;
    const x = clientX - rect.left - rect.width / 2;
    const y = clientY - rect.top - rect.height / 2;

    setAngle(Math.atan2(y, x));
    setDistance(Math.hypot(x, y));
    if (isMouseDown) {
      setJoystickPointerStyle({
        position: "absolute",
        top: `calc(50% + ${Math.sin(angle) * 40}px)`,
        left: `calc(50% + ${Math.cos(angle) * 40}px)`,
      });
    } else {
      setJoystickPointerStyle({
        position: "absolute",
        top: "50%",
        left: "50%",
      });
    }
  };

  const handleMouseDown = (e: any) => {
    setIsMouseDown(true);
  };

  const handleMouseUp = (e: any) => {
    setIsMouseDown(false);
    setAngle(0);
    setDistance(0);
    setJoystickPointerStyle({
      position: "absolute",
      top: "50%",
      left: "50%",
    });
  };

  useEffect(() => {
    console.log("Joystick changed");
    console.log(isMouseDown, angle);

    if (!isMouseDown) {
      document.body.style.overflowY = "visible";
      document.body.style.position = "";
      sendCommand("standby");

      return;
    }

    // Throttle the sendCommand calls
    const now = Date.now();
    if (now - lastSendTime.current >= throttleDelay) {
      // New system: 0° is forward, 90° is right
      let angleDegrees = ((angle + Math.PI / 2) * 180) / Math.PI;

      // Normalize to -180 to 180 range
      while (angleDegrees > 180) angleDegrees -= 360;
      while (angleDegrees < -180) angleDegrees += 360;

      sendCommand("move", {
        angle: angleDegrees,
      });
      lastSendTime.current = now;
    }

    // disable scroll
    document.body.style.width = "100vw";
    document.body.style.height = "100vh";
    document.body.style.overflowY = "hidden";
    document.body.style.position = "fixed";
  }, [isMouseDown, angle]);

  // Handle cleanup when component unmounts or when mouse is released
  useEffect(() => {
    return () => {
      sendCommand("standby");
    };
  }, []);

  const handleKeyDown = (event: any) => {
    console.log(event.key);
    setKeysPressed(keysPressed + 1);
    setIsMouseDown(true);

    setDistance(40);
    let newAngle = angle;
    if (event.key === "ArrowUp" || event.key === "w") {
      newAngle = -Math.PI / 2;
    } else if (event.key === "ArrowDown" || event.key === "s") {
      newAngle = Math.PI / 2;
    } else if (event.key === "ArrowLeft" || event.key === "a") {
      newAngle = Math.PI;
    } else if (event.key === "ArrowRight" || event.key === "d") {
      newAngle = 0;
    } else {
      return;
    }
    setAngle(newAngle);

    setJoystickPointerStyle({
      position: "absolute",
      top: `calc(50% + ${Math.sin(newAngle) * 40}px)`,
      left: `calc(50% + ${Math.cos(newAngle) * 40}px)`,
    });
  };
  const handleKeyUp = () => {
    if (keysPressed == 0) {
      setDistance(0);
      setAngle(0);
      setIsMouseDown(false);
      setJoystickPointerStyle({
        position: "absolute",
        top: "50%",
        left: "50%",
      });
    }
  };

  useEffect(() => {
    window.addEventListener("keydown", handleKeyDown);
    window.addEventListener("keyup", handleKeyUp);

    return () => {
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, []);

  return (
    <div className="joystick-cont box">
      <ArrowLeftIcon className="arrow front" w={3} h={3} />
      <ChevronLeftIcon className="arrow left" w={5} h={5} />
      <ChevronLeftIcon className="arrow right" w={5} h={5} />
      <ChevronLeftIcon className="arrow back" w={5} h={5} />
      <div
        className="joystick-outer"
        onMouseLeave={handleMouseUp}
        onMouseMove={handleMouseMove}
        onTouchMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onTouchEnd={handleMouseUp}
      >
        <div className="joystick-inner" ref={joystickInner}>
          <div
            className="joystick-pointer"
            onMouseDown={handleMouseDown}
            onTouchStart={handleMouseDown}
            onMouseUp={handleMouseUp}
            onTouchEnd={handleMouseUp}
            ref={joystickPointer}
            style={joystickPointerStyle}
          >
            <div className="front"></div>
            <div className="left"></div>
            <div className="right"></div>
            <div className="back"></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Joystick;

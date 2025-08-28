"use client";
import { sendCommand } from "./commands";
import { useEffect, useState, useRef } from "react";
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
    if (!isMouseDown) return;

    // Prevent scrolling on touch devices
    if (e.touches) {
      e.preventDefault();
    }

    const rect = e.target.parentNode.getBoundingClientRect();
    const clientX = e.clientX || (e.touches && e.touches[0].clientX) || 0;
    const clientY = e.clientY || (e.touches && e.touches[0].clientY) || 0;
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

    // Prevent scrolling on touch devices
    if (e.touches) {
      e.preventDefault();
    }
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

    // Disable scrolling when joystick is active
    document.body.style.overflow = "hidden";
    document.body.style.position = "fixed";
  }, [isMouseDown, angle]);

  useEffect(() => {
    if (!isMouseDown) {
      // Re-enable scrolling when joystick is not in use
      document.body.style.overflow = "";
      document.body.style.position = "";
      sendCommand("standby");
      return;
    }
  }, [isMouseDown]);

  // Handle cleanup when component unmounts
  useEffect(() => {
    return () => {
      sendCommand("standby");
      // Restore normal scrolling behavior
      document.body.style.overflow = "";
      document.body.style.position = "";
    };
  }, []);

  const handleKeyDown = (event: any) => {
    setKeysPressed((prev) => prev + 1);
    setIsMouseDown(true);

    setDistance(40);
    let newAngle = angle;
    if (event.key === "ArrowUp") {
      newAngle = -Math.PI / 2;
    } else if (event.key === "ArrowDown") {
      newAngle = Math.PI / 2;
    } else if (event.key === "ArrowLeft") {
      newAngle = Math.PI;
    } else if (event.key === "ArrowRight") {
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
    setKeysPressed((prev) => {
      const newCount = prev - 1;
      if (newCount <= 0) {
        setDistance(0);
        setAngle(0);
        setIsMouseDown(false);
        setJoystickPointerStyle({
          position: "absolute",
          top: "50%",
          left: "50%",
        });
      }
      return Math.max(0, newCount);
    });
  };

  useEffect(() => {
    window.addEventListener("keydown", handleKeyDown);
    window.addEventListener("keyup", handleKeyUp);

    return () => {
      window.removeEventListener("keydown", handleKeyDown);
      window.removeEventListener("keyup", handleKeyUp);
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
        onTouchStart={(e) => e.preventDefault()}
      >
        <div className="joystick-inner" ref={joystickInner}>
          <div
            className="joystick-pointer"
            onMouseDown={handleMouseDown}
            onTouchStart={(e) => {
              e.preventDefault();
              handleMouseDown(e);
            }}
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
      <button
        className="joystick-stop-btn"
        onClick={() => sendCommand("standby")}
      >
        Stop
      </button>
    </div>
  );
};

export default Joystick;

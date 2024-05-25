'use client'
import { useEffect, useState, useRef } from "react";
import { ArrowLeftIcon, ChevronLeftIcon } from '@chakra-ui/icons'
import { position } from "@chakra-ui/react";

const Joystick = () => {
    const [isMouseDown, setIsMouseDown] = useState(false);
    const [angle, setAngle] = useState(0);
    const [distance, setDistance] = useState(0);
    const [keysPressed, setKeysPressed] = useState(0);
    const [joystickPointerStyle, setJoystickPointerStyle] = useState({});

    const joystickInner = useRef<HTMLDivElement | null>(null);
    const joystickPointer = useRef<HTMLDivElement | null>(null);

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
                })
        } else {
            setJoystickPointerStyle({
                position: "absolute",
                top: "50%",
                left: "50%",
            })
        }
    }

    const handleMouseDown = (e: any) => {
        setIsMouseDown(true);
    }

    const handleMouseUp = (e: any) => {
        setIsMouseDown(false);
        setAngle(0);
        setDistance(0);
        setJoystickPointerStyle({
            position: "absolute",
            top: "50%",
            left: "50%",
        })
    }

    const handleKeyDown = (event: any) => {
        setKeysPressed(keysPressed + 1);

        setDistance(40);
        let newAngle = angle;
        if (event.key === 'ArrowUp') {
            newAngle = -Math.PI / 2
        } else if (event.key === 'ArrowDown') {
            newAngle = Math.PI / 2
        } else if (event.key === 'ArrowLeft') {
            newAngle = Math.PI
        } else if (event.key === 'ArrowRight') {
            newAngle = 0
        } else {
            return;
        }
        setAngle(newAngle);

        setJoystickPointerStyle({
            position: "absolute",
            top: `calc(50% + ${Math.sin(newAngle) * 40}px)`,
            left: `calc(50% + ${Math.cos(newAngle) * 40}px)`,
        })

        console.log(newAngle);
    }
    const handleKeyUp = () => {
        if (keysPressed == 0) {
            setDistance(0);
            setAngle(0);
            setJoystickPointerStyle({
                position: "absolute",
                top: "50%",
                left: "50%",
            })
        }    
    }

    useEffect(() => {
        window.addEventListener('keydown', handleKeyDown);
        window.addEventListener('keyup', handleKeyUp);

        return () => {
            window.removeEventListener('keydown', handleKeyDown);
        };
    }, []);

    return (
    <div className="joystick-cont box">
        <ArrowLeftIcon className="arrow front" w={3} h={3} />
        <ChevronLeftIcon className="arrow left" w={5} h={5} />
        <ChevronLeftIcon className="arrow right" w={5} h={5} />
        <ChevronLeftIcon className="arrow back" w={5} h={5} />
        <div className="joystick-outer"
            onMouseLeave={handleMouseUp}
            onMouseMove={handleMouseMove}
            onTouchMove={handleMouseMove}
            onMouseUp={handleMouseUp}
            onTouchEnd={handleMouseUp}>
        <div className="joystick-inner"
            ref={joystickInner}>
            <div className="joystick-pointer"
                onMouseDown={handleMouseDown}
                onTouchStart={handleMouseDown}
                onMouseUp={handleMouseUp}
                onTouchEnd={handleMouseUp}
                ref={joystickPointer}
                style={joystickPointerStyle}>
            <div className="front"></div>
            <div className="left"></div>
            <div className="right"></div>
            <div className="back"></div>
            </div>
        </div>
        </div>
    </div>
)}

export default Joystick;
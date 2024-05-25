import { act, useState } from "react";
import { socket } from "../socket";
import { ArrowForwardIcon } from '@chakra-ui/icons'
import Image from 'next/image'

interface Props {
    actionType: string
    buttonText: string
    iconPath: string
}

const ActionWithParam = ({actionType, iconPath, buttonText}: Props) => {
    const [text, setText] = useState("")
    const [isOpen, setIsOpen] = useState(false)

    const sendAction = () => {
        socket.emit("action", {"action": actionType, "param": text});
        setText("");
        setIsOpen(false);
    }

    return (
        <>
            <div className={`box window ${isOpen ? 'open' : 'hidden'}`}>
                <h2>{buttonText}</h2>
                <form className="message" action=""
                    onSubmit={(event) => {
                    event.preventDefault();
                    sendAction();
                    }}>
                    <input type="text" value={text} onChange={event => setText(event.target.value)}/>
                    <div className="button-cont">
                    <button className="btn">
                        Cancel
                    </button>
                    <button className="btn" type="submit">
                        Send
                        <ArrowForwardIcon className="" w={4} h={4} />
                    </button>
                    </div>
                </form>
            </div>
            <button className="btn" onClick={() => {setIsOpen(!isOpen)}}>
                <Image className="img" src={iconPath} alt="Icon" width={18} height={18}  />
                {buttonText}
            </button>
        </>
    )
}

export default ActionWithParam;
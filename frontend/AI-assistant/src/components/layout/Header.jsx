import "./header.css";
import { Bot, Menu } from "lucide-react";

export default function Header({toggleSidebar}) {
    return (

        <div className="header">
            <button
                className="menu-btn"
                onClick={toggleSidebar}
            >
                <Menu size={22} />
            </button>


            <Bot size={32} />
            <h1>ResourcePlus AI Assistant</h1>
        </div>
    );
}
import "./sidebar.css";
import { FileText } from "lucide-react";
export default function Sidebar({

  isOpen,

  conversations,

  onNewChat,

  onSelectConversation

}) {



  return (

    <aside className={`sidebar ${!isOpen ? "closed" : ""}`}>

      <button
        className="new-chat-btn"
        onClick={onNewChat}
      >
        {!isOpen ? "+" : "+ New Chat"}
      </button>

      <div className="conversation-list">
        {conversations.map((chat) => (

          <button
            key={chat.session_id}
            className="conversation-item"
            onClick={() => onSelectConversation(chat.session_id)}
          >
            {isOpen ? (
              <>
                <FileText size={16} className="conversation-icon" />
                <span>{chat.title}</span>
              </>
            ) : (
              <FileText size={18} />
            )}
          </button>
        ))}
      </div>

    </aside >

  );
}
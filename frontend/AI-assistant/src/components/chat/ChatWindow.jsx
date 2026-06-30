
import Message from "./Message";
import "./chat.css";

export default function ChatWindow({ messages, loading, chatEndRef }) {
    return (
        <div className="chat-window">

            {messages.length === 0 ? (

                <div className="empty-chat">
                    <div className="empty-icon">🤖</div>

                    <h2>How can I help you today?</h2>

                    <p>
                        Ask anything about ResourcePlus.
                    </p>

                </div>

            ) : (

                messages.map((msg, index) => (
                    <Message
                        key={index}
                        msg={msg}
                        index={index}
                    />
                ))

            )}

            {loading && (
                <div className="thinking">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            )}

            <div ref={chatEndRef}></div>

        </div>
    );
}
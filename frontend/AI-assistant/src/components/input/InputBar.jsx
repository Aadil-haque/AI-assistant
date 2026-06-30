import { Mic, Send } from "lucide-react";
import "./input.css";

export default function InputBar({   question,  setQuestion,  sendQuestion,  startListening, }) {

    return (
        <div className="input-area">

            <input
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyDown={(e) => {
                    if (e.key === "Enter") {
                        sendQuestion();
                    }
                }}
                placeholder="Ask a question..."
            />

            <button
                className="icon-btn"
                onClick={startListening}
            >
                <Mic size={18} />
            </button>

            <button
                className="icon-btn send"
                onClick={sendQuestion}
            >
                <Send size={18} />
            </button>


        </div>
    );
}
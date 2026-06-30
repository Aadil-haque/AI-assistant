import { motion } from "framer-motion";
import ReactMarkdown from "react-markdown";
import { Bot, User } from "lucide-react";

export default function Message({ msg, index }) {
  return (
    <motion.div
      key={index}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`message ${msg.sender}`}
    >

      <div className="avatar">
        {msg.sender === "bot"
          ? <Bot size={18} />
          : <User size={18} />
        }
      </div>

      <div className="message-content">

        <ReactMarkdown>
          {msg.text}
        </ReactMarkdown>

        {msg.sources && msg.sources.length > 0 && (

          <div className="sources">

            <strong>Sources</strong>

            <ul>

              {msg.sources.map((source, i) => (

                <li key={i}>{source}</li>

              ))}

            </ul>

          </div>

        )}

      </div>

    </motion.div>
  );
}
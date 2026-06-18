import { useState, useEffect, useRef } from "react";
import axios from "axios";
import "./App.css";
import ReactMarkdown from "react-markdown";
import {
  Send,
  Mic,
  Bot,
  User
} from "lucide-react";
import { motion } from "framer-motion";

function App() {

  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [listening, setListening] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({
      behavior: "smooth"
    });
  }, [messages]);

  const startListening = () => {


    const SpeechRecognition =
      window.SpeechRecognition ||
      window.webkitSpeechRecognition;

    if (!SpeechRecognition) {

      alert(
        "Speech Recognition is not supported in this browser."
      );

      return;
    }

    const recognition =
      new SpeechRecognition();

    recognition.lang = "en-US";

    recognition.start();

    setListening(true);

    recognition.onresult = (event) => {

      const transcript =
        event.results[0][0].transcript;

      setQuestion(transcript);
    };

    recognition.onend = () => {

      setListening(false);
    };

    recognition.onerror = () => {

      setListening(false);
    };
  };


  const sendQuestion = async () => {

    if (!question.trim()) return;

    const userMessage = {
      sender: "user",
      text: question
    };

    setMessages(prev => [...prev, userMessage]);

    const currentQuestion = question;

    setQuestion("");

    try {
      setLoading(true);

      const response = await axios.post(
        "http://127.0.0.1:8000/ask",
        {
          question: currentQuestion,
          history: messages
        }
      );

      const botMessage = {
        sender: "bot",
        text: response.data.answer,
        sources: response.data.sources

      };
      setLoading(false);

      setMessages(prev => [...prev, botMessage]);

    } catch (error) {

      console.log(error);

      console.log(error.response);

      setMessages(prev => [
        ...prev,
        {
          sender: "bot",
          text: JSON.stringify(
            error.response?.data || error.message
          )
        }
      ]);
    }
  };

  return (
    <div className="container">

      <div className="header">
        <Bot size={32} />
        <h1>ResourcePlus AI Assistant</h1>
      </div>

      <div className="chat-window">



        {messages.map((msg, index) => (

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

        ))}



        {loading && (
          <div className="bot">
            Thinking...
          </div>
        )}

      </div>
      {listening && (
        <div>
          Listening...
        </div>
      )}

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

    </div>
  );
}


export default App;
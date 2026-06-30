import { useState, useEffect, useRef } from "react";

import "./App.css";
import ReactMarkdown from "react-markdown";
import {
  Send,
  Mic,
  Bot,
  User
} from "lucide-react";
import { motion } from "framer-motion";
import Header from "./components/layout/Header";
import ChatWindow from "./components/chat/ChatWindow";
import InputBar from "./components/input/InputBar";
import AnimatedBackground from "./components/background/AnimatedBackground";
import MainLayout from "./components/layout/MainLayout";
import { askQuestion, getConversations, getConversation } from "./api/chatbot";
import Sidebar from "./components/sidebar/Sidebar";


function App() {

  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [listening, setListening] = useState(false);
  
  const chatEndRef = useRef(null);
  // One session ID per browser tab
  const sessionId = useRef(crypto.randomUUID());
  const [conversations, setConversations] = useState([]);
 
  const [sidebarOpen,setSidebarOpen]=useState(true);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({
      behavior: "smooth"
    });
  }, [messages]);

  useEffect(() => {
    async function loadConversations() {
      try {
        const data = await getConversations();
        setConversations(data);
      } catch (err) {
        console.error(err);
      }
    }

    loadConversations();

  }, []);

  const loadConversation = async (selectedSessionId) => {
    try {
      const history = await getConversation(selectedSessionId);

      console.log(history);

      const normalizedHistory = history.map(msg => ({
        ...msg,
        sender: msg.sender === "assistant" ? "bot" : msg.sender
      }));

      setMessages(normalizedHistory);

      sessionId.current = selectedSessionId;

    } catch (err) {
      console.error(err);
    }
  };

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

  const startNewChat = () => {

    sessionId.current = crypto.randomUUID();

    setMessages([]);

  };


  const sendQuestion = async () => {
    console.log("sendQuestion called");
    console.log(question);


    if (!question.trim()) return;

    const userMessage = {
      sender: "user",
      text: question
    };

    const updatedHistory = [...messages, userMessage];
    setMessages(updatedHistory);

    

    setQuestion("");

    try {
      setLoading(true);

    console.log("history:",updatedHistory);

    const response = await askQuestion({
        question,
        history: updatedHistory,
        session_id: sessionId.current,
    });

      const botMessage = {
        sender: "bot",
        text: response.answer,
        sources: response.sources

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
    <>
      <AnimatedBackground />

      <MainLayout
        sidebar={
          <Sidebar

            isOpen={sidebarOpen}

            conversations={conversations}

            onNewChat={startNewChat}

            onSelectConversation={loadConversation}

          />
        }
      >
        <Header
          toggleSidebar={() =>
            setSidebarOpen(!sidebarOpen)
          }
        />

        <ChatWindow
          messages={messages}
          loading={loading}
          chatEndRef={chatEndRef}
        />

        <InputBar
          question={question}
          setQuestion={setQuestion}
          sendQuestion={sendQuestion}
          startListening={startListening}
        />
      </MainLayout>
    </>
  );
}


export default App;
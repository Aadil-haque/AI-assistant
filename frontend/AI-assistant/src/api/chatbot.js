import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

/*
---------------------------------------
Ask AI
---------------------------------------
*/
export async function askQuestion(payload) {
  const response = await axios.post(
    `${API_URL}/ask`,
    payload
  );

  return response.data;
}

/*
---------------------------------------
Conversation List
---------------------------------------
*/
export async function getConversations() {
  const response = await axios.get(
    `${API_URL}/conversations`
  );

  return response.data;
}

/*
---------------------------------------
Load One Conversation
---------------------------------------
*/
export async function getConversation(sessionId) {
  const response = await axios.get(
    `${API_URL}/conversation/${sessionId}`
  );

  return response.data;
}
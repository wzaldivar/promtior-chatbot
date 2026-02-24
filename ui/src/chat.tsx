import { ChatRole, type ChatRoleType } from "./chat_role.ts";
import {
  type FunctionComponent,
  type KeyboardEvent,
  useEffect,
  useRef,
  useState,
} from "react";
import ChatItem from "./chat_item.tsx";

type ChatMessage = {
  id: number;
  role: ChatRoleType;
  message: string;
};
import "./chat.css";

const HOST = import.meta.env.VITE_API_HOST ?? "";

const Chat: FunctionComponent = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [isBotTyping, setIsBotTyping] = useState(false);

  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isBotTyping]);

  const handleSend = async () => {
    if (!input.trim() || isBotTyping) return;

    const userMessage: ChatMessage = {
      id: Date.now(),
      role: ChatRole.USER,
      message: input.trim(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsBotTyping(true);

    try {
      const res = await fetch(`${HOST}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: input,
        }),
      });

      if (!res.ok) {
        throw new Error(res.statusText);
      }

      const data = await res.json();

      const botMsg: ChatMessage = {
        id: Date.now() + 1,
        role: ChatRole.BOT,
        message: data.response,
      };

      setMessages((prev) => [...prev, botMsg]);
    } catch (e) {
      const message = e instanceof Error ? e.message : "Unknown error";

      const botMsg: ChatMessage = {
        id: Date.now() + 1,
        role: ChatRole.BOT,
        message: message,
      };

      setMessages((prev) => [...prev, botMsg]);
    } finally {
      setIsBotTyping(false);
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-layout">
      <h2>Chat</h2>
      <div className="messages-list" ref={scrollRef}>
        {messages.map((message) => (
          <ChatItem
            key={message.id}
            role={message.role}
            message={message.message}
          />
        ))}

        {isBotTyping && <ChatItem role={ChatRole.BOT} message="..." />}
      </div>

      <div className="input-group">
        <textarea
          value={input}
          disabled={isBotTyping}
          rows={3}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => handleKeyDown(e)}
          placeholder={isBotTyping ? "Bot is typing..." : "Input message ..."}
        />
        <button onClick={handleSend} disabled={isBotTyping || !input.trim()}>
          Send
        </button>
      </div>
    </div>
  );
};

export default Chat;

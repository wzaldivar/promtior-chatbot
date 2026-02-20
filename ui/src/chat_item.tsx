import { memo, type FunctionComponent } from "react";
import botAvatar from "./assets/bot.svg";
import userAvatar from "./assets/user.svg";
import { ChatRole, type ChatRoleType } from "./chat_role.ts";
import "./chat_item.css";

type ChatItemProps = {
  role: ChatRoleType;
  message: string;
};

const avatars = {
  [ChatRole.USER]: userAvatar,
  [ChatRole.BOT]: botAvatar,
};

const ChatItem: FunctionComponent<ChatItemProps> = memo(({ role, message }) => {
  return (
    <>
      <div className={`chat-line role-${role}`}>
        <img className={`avatar`} src={avatars[role]} />
        <div className="chat-text">{message}</div>
      </div>
    </>
  );
});

export default ChatItem;

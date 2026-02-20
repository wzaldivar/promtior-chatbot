export const ChatRole = {
  USER: "user",
  BOT: "bot",
};

export type ChatRoleType = (typeof ChatRole)[keyof typeof ChatRole];

import { create } from 'zustand';

interface Message {
  type: 'user' | 'bot';
  content: string;
}

interface ChatState {
  messages: Message[];
  hasFile: boolean;
  fileName: string | null;
  addMessage: (message: Message) => void;
  setFileStatus: (hasFile: boolean, fileName?: string) => void;
  clearChat: () => void;
}

export const useChatStore = create<ChatState>((set) => ({
  messages: [],
  hasFile: false,
  fileName: null,
  addMessage: (message) =>
    set((state) => ({ messages: [...state.messages, message] })),
  setFileStatus: (hasFile, fileName = undefined) => set({ hasFile, fileName }),
  clearChat: () => set({ messages: [], hasFile: false, fileName: null }),
}));
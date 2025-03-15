import { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Brain,
  LogOut,
  Send,
  Upload,
  FileText,
  Trash,
} from 'lucide-react';
import { useAuthStore } from '../store/authStore';
import { useChatStore } from '../store/chatStore';
import { getChatStatus, sendMessage, uploadFile } from '../api/chat';

function Chat() {
  const navigate = useNavigate();
  const clearToken = useAuthStore((state) => state.clearToken);
  const {
    messages,
    hasFile,
    fileName,
    addMessage,
    setFileStatus,
    clearChat,
  } = useChatStore();
  const [isLoading, setIsLoading] = useState(false);
  const [question, setQuestion] = useState('');
  const chatContainerRef = useRef<HTMLDivElement>(null);

  const handleLogout = () => {
    clearToken();
    clearChat();
    navigate('/login');
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const isValidType =
      file.type === 'application/pdf' ||
      file.type ===
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document';

    if (!isValidType) {
      alert('Please upload only PDF or Word documents');
      return;
    }

    setIsLoading(true);
    try {
      await uploadFile(file);
      const status = await getChatStatus();
      setFileStatus(status.file, status.data.extra_info.file_name);
    } catch (error) {
      console.error('File upload failed:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim() || !hasFile || isLoading) return;

    setIsLoading(true);
    addMessage({ type: 'user', content: question });
    setQuestion('');

    try {
      const response = await sendMessage(question);
      addMessage({ type: 'bot', content: response.answer });
    } catch (error) {
      console.error('Failed to send message:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    const checkStatus = async () => {
      try {
        const status = await getChatStatus();
        setFileStatus(status.file, status.data.extra_info.file_name);
      } catch (error) {
        console.error('Failed to get chat status:', error);
      }
    };
    checkStatus();
  }, []);

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="flex flex-col h-screen bg-gray-900">
      <header className="flex items-center justify-between px-6 py-4 bg-gray-800 border-b border-gray-700">
        <div className="flex items-center space-x-2">
          <Brain className="h-8 w-8 text-blue-500" />
          <h1 className="text-xl font-bold">Brain</h1>
        </div>
        <div className="flex items-center space-x-4">
          {!hasFile && (
            <label className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg cursor-pointer hover:bg-blue-700 transition-colors">
              <Upload className="h-5 w-5 mr-2" />
              Upload File
              <input
                type="file"
                accept=".pdf,.docx"
                className="hidden"
                onChange={handleFileUpload}
                disabled={isLoading}
              />
            </label>
          )}
          {fileName && (
            <div className="flex items-center px-3 py-1.5 bg-gray-700 rounded-lg">
              <FileText className="h-4 w-4 text-gray-400 mr-2" />
              <span className="text-sm text-gray-300 max-w-[150px] truncate">
                {fileName}
              </span>
              <button
                onClick={() => {
                  setFileStatus(false, undefined);
                  clearChat();
                }}
                className="ml-2 text-gray-400 hover:text-red-500 transition-colors"
              >
                <Trash className="h-4 w-4" />
              </button>
            </div>
          )}
          <button
            onClick={handleLogout}
            className="flex items-center px-4 py-2 text-gray-300 hover:text-white transition-colors"
          >
            <LogOut className="h-5 w-5 mr-2" />
            Logout
          </button>
        </div>
      </header>

      <div
        ref={chatContainerRef}
        className="flex-1 overflow-y-auto px-6 py-4 space-y-4"
      >
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${
              message.type === 'user' ? 'justify-end' : 'justify-start'
            }`}
          >
            <div
              className={`max-w-2xl p-4 rounded-lg ${
                message.type === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-800 text-gray-100'
              }`}
            >
              {message.content}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-800 rounded-lg p-4 max-w-[100px]">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
              </div>
            </div>
          </div>
        )}
      </div>

      <form
        onSubmit={handleSendMessage}
        className="px-6 py-4 bg-gray-800 border-t border-gray-700"
      >
        <div className="flex space-x-4">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder={
              hasFile
                ? 'Ask a question about your document...'
                : 'Upload a document to start chatting'
            }
            disabled={!hasFile || isLoading}
            className="flex-1 px-4 py-2 bg-gray-700 text-white rounded-lg placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={!hasFile || !question.trim() || isLoading}
            className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-blue-700 transition-colors"
          >
            <Send className="h-5 w-5" />
          </button>
        </div>
      </form>
    </div>
  );
}

export default Chat;
import api from './axios';
import { ChatResponse, DocumentResponse, FileUploadResponse } from '../types/auth';

export const uploadFile = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post<FileUploadResponse>('/chat/upload', formData);
  return response.data;
};

export const getChatStatus = async () => {
  const response = await api.get<DocumentResponse>('/chat');
  return response.data;
};

export const sendMessage = async (question: string) => {
  const response = await api.post<ChatResponse>('/chat/ask', { question });
  return response.data;
};

export const deleteFile = async () => {
  const response = await api.delete('/chat/delete');
  return response.data;
};
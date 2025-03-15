import api from './axios';
import { LoginCredentials, SignupCredentials, AuthResponse } from '../types/auth';

export const login = async (credentials: LoginCredentials) => {
  const response = await api.post<AuthResponse>('/auth/login', credentials);
  return response.data;
};

export const signup = async (credentials: SignupCredentials) => {
  const response = await api.post<AuthResponse>('/auth/signup', credentials);
  return response.data;
};
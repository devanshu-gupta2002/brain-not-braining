export interface LoginCredentials {
  email: string;
  password: string;
}

export interface SignupCredentials extends LoginCredentials {
  confirmPassword: string;
}

export interface AuthResponse {
  token: string;
}

export interface ChatResponse {
  answer: string;
}

export interface FileUploadResponse {
  filename: string;
  data: {
    message: string;
  };
}

export interface DocumentResponse {
  data: {
    doc_id: string;
    extra_info: {
      file_name: string;
      file_type: string;
      file_size: number;
      creation_date: string;
    };
  };
  file: boolean;
}
export interface User {
  user_id: number;
  email: string;
  username: string;
  role: string;
  is_active?: boolean;
  is_superuser?: boolean;
  full_name?: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface RegisterResponse {
  access_token: string;
  token_type: string;
  user: User;
}

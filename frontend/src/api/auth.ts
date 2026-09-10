import client from "./client";

export interface RegisterPayload {
  name: string;
  email: string;
  password: string;
}

export interface LoginPayload {
  email: string;
  password: string;
}

export const registerUser = (payload: RegisterPayload) =>
  client.post("/api/auth/register", payload);

export const loginUser = (payload: LoginPayload) =>
  client.post<{ access_token: string; token_type: string }>("/api/auth/login", payload);

export const getMe = () => client.get("/api/auth/me");
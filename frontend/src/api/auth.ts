import { apiFetch } from "./client";
import type { User } from "../types";

export interface Token {
  access_token: string;
  token_type: string;
}

export function register(username: string, password: string): Promise<User> {
  return apiFetch<User>("/auth/register", {
    method: "POST",
    body: { username, password },
    auth: false,
  });
}

export function login(username: string, password: string): Promise<Token> {
  return apiFetch<Token>("/auth/login", {
    method: "POST",
    form: { username, password },
    auth: false,
  });
}

export function me(): Promise<User> {
  return apiFetch<User>("/auth/me");
}

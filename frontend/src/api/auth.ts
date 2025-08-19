import { useMutation, useQuery } from '@tanstack/react-query'
import { queryClient } from '@/lib/react-query'

const BASE_URL = import.meta.env.VITE_BACKEND_URL ?? 'http://localhost:8000'

export type ApiResponse<T> = {
  status: 'success' | 'error'
  data: T
  message?: string
}

export type UserPublic = {
  email: string
  username: string
}

export type LoginResponse = {
  user: UserPublic
  access_token: string
  token_type: string
}

export type RegisterRequest = {
  email: string
  password: string
  username: string
}

export type LoginRequest = {
  email: string
  password: string
}

export type User = {
  email: string
  username: string
}

const TOKEN_KEY = 'bh_access_token'

export const tokenStorage = {
  get: (): string | null => {
    return (
      (typeof window !== 'undefined' && window.localStorage.getItem(TOKEN_KEY)) ||
      (typeof window !== 'undefined' && window.sessionStorage.getItem(TOKEN_KEY)) ||
      null
    )
  },
  set: (t: string, remember = true) => {
    if (remember) {
      window.localStorage.setItem(TOKEN_KEY, t)
    } else {
      window.sessionStorage.setItem(TOKEN_KEY, t)
    }
  },
  clear: () => {
    if (typeof window !== 'undefined') {
      window.localStorage.removeItem(TOKEN_KEY)
      window.sessionStorage.removeItem(TOKEN_KEY)
    }
  },
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const token = tokenStorage.get()
  const res = await fetch(`${BASE_URL}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers || {}),
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    credentials: 'omit',
  })
  if (!res.ok) {
    const text = await res.text().catch(() => '')
    throw new Error(text || `HTTP ${res.status}`)
  }
  return res.json()
}

export function useLoginMutation() {
  return useMutation<ApiResponse<LoginResponse>, Error, LoginRequest>({
    mutationFn: (body: LoginRequest) =>
      request<ApiResponse<LoginResponse>>('/api/user/login', {
        method: 'POST',
        body: JSON.stringify(body),
      }),
  })
}

export function useRegisterMutation() {
  return useMutation<ApiResponse<User>, Error, RegisterRequest>({
    mutationFn: (body: RegisterRequest) =>
      request<ApiResponse<User>>('/api/user/register', {
        method: 'POST',
        body: JSON.stringify(body),
      }),
  })
}

export function useMeQuery(enabled = true) {
  return useQuery<UserPublic | null>({
    queryKey: ['me'],
    enabled,
    queryFn: async () => {
      const token = tokenStorage.get()
      if (!token) return null
      try {
        const res = await request<ApiResponse<User>>('/api/user/me')
        // backend returns User with email and username
        return { email: res.data.email, username: res.data.username }
      } catch {
        tokenStorage.clear()
        return null
      }
    },
    staleTime: 1000 * 60,
  })
}

export function logout() {
  tokenStorage.clear()
  queryClient.setQueryData(['me'], null)
}

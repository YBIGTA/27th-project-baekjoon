import React, { createContext, useContext, useMemo } from 'react'
import { useMeQuery, tokenStorage } from '@/api/auth'

type AuthContextType = {
  user: { email: string; username: string } | null
  isAuthenticated: boolean
  token: string | null
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const token = typeof window !== 'undefined' ? tokenStorage.get() : null
  const { data: me } = useMeQuery(!!token)

  const value = useMemo<AuthContextType>(() => ({
    user: me ?? null,
    isAuthenticated: !!me,
    token: token ?? null,
  }), [me, token])

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}

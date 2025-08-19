import React from 'react'
import { redirect } from '@tanstack/react-router'
import { useAuth } from '@/context/auth'

export function Protected({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuth()
  if (!isAuthenticated && typeof window !== 'undefined') {
    throw redirect({ to: '/login' })
  }
  return <>{children}</>
}

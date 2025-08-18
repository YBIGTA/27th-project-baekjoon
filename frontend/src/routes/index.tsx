import * as React from 'react'
import { Search } from "lucide-react"
import { createFileRoute, Link, useNavigate } from '@tanstack/react-router'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Spinner } from "@/components/ui/spinner"
import Header from "@/components/organisms/header"
import Footer from "@/components/organisms/footer"


export const Route = createFileRoute('/')({
  component: HomePage,
})


function HomePage() {
  const [searchTerm, setSearchTerm] = React.useState("")
  const navigate = useNavigate()

  const [isSearching, setIsSearching] = React.useState(false)

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault()
      handleSearch()
    }
  }

  const handleSearch = async () => {
    const term = searchTerm.trim()
    if (!term) return
    
    setIsSearching(true)
    
    try {
      // 시뮬레이션을 위한 지연
      await new Promise(resolve => setTimeout(resolve, 500))
      
      // TODO: 실제 문제 검색 API 호출
      console.log('문제 검색:', term)
      
      navigate({ to: '/problem/$problemId', params: { problemId: term } })
    } catch (error) {
      console.error('검색 실패:', error)
    } finally {
      setIsSearching(false)
    }
  }

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Header currentPage="home" />

      {/* Main Content */}
      <main className="flex-1 flex items-center justify-center px-4 sm:px-6 lg:px-8">
        <div className="w-full max-w-2xl text-center space-y-8">
          {/* Logo and Title */}
          <div className="space-y-4">
            <h2 className="text-5xl sm:text-6xl font-bold text-foreground font-[family-name:var(--font-playfair)]">
              BaekjoonHelper
            </h2>
            <p className="text-lg text-muted-foreground">이젠 반례도 딸깍으로.</p>
          </div>

          {/* Search Bar */}
          <div className="space-y-4">
            <div className="relative">
              <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-muted-foreground h-5 w-5" />
              <Input
                type="text"
                onChange={(e) => setSearchTerm(e.target.value)}
                onKeyDown={handleKeyDown}
                value={searchTerm}
                placeholder="문제 번호를 입력하세요..."
                className="w-full pl-12 pr-4 py-4 text-lg bg-input border-border rounded-full shadow-sm focus:ring-2 focus:ring-ring focus:border-transparent"
              />
            </div>
            <div className="flex gap-3 justify-center">
              <Button 
                onClick={handleSearch}
                disabled={isSearching || !searchTerm.trim()}
                className="bg-primary hover:bg-primary/90 text-primary-foreground px-8 py-2 disabled:opacity-50"
              >
                {isSearching ? (
                  <>
                    <Spinner size="sm" />
                    검색 중...
                  </>
                ) : (
                  '검색'
                )}
              </Button>
            </div>
          </div>

          {/* Additional Info */}
          <div className="space-y-2">
            <p className="text-sm text-muted-foreground">백준 문제번호를 입력하고 엔터를 누르거나 검색 버튼을 클릭하세요</p>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  )
}

import { Button } from "@/components/ui/button"
import { Link, useRouter } from '@tanstack/react-router'
import { useAuth } from '@/context/auth'
import { logout } from '@/api/auth'

interface HeaderProps {
  showAuthButtons?: boolean
  currentPage?: "login" | "signup" | "home",
  maxWidth?: boolean
}

export default function Header({ showAuthButtons = true, currentPage = "home", maxWidth = true }: HeaderProps) {
  const { isAuthenticated, user } = useAuth()
  const router = useRouter()

  const handleLogout = () => {
    logout()
    router.navigate({ to: '/login' })
  }
  
  return (
    <header className="w-full bg-card shadow-sm border-b border-border">
      <div className={`mx-auto px-4 sm:px-6 lg:px-8 py-4 ${maxWidth ? "max-w-7xl" : ""}`}>
        <div className="flex justify-between items-center">
          <Link to="/">
            <h1 className="text-2xl font-bold text-primary font-[family-name:var(--font-playfair)] cursor-pointer hover:text-primary/80">
              BaekjoonHelper
            </h1>
          </Link>
          {showAuthButtons && (
            <div className="flex gap-3 items-center">
              {isAuthenticated ? (
                <>
                  <span className="text-sm text-muted-foreground">{user?.username}</span>
                  <Button variant="outline" onClick={handleLogout}>
                    로그아웃
                  </Button>
                </>
              ) : (
                <>
                  {currentPage !== "login" && (
                    <Link to="/login">
                      <Button variant="ghost" className="text-foreground hover:text-primary">
                        로그인
                      </Button>
                    </Link>
                  )}
                  {currentPage !== "signup" && (
                    <Link to="/signup">
                      <Button className="bg-primary hover:bg-primary/90 text-primary-foreground">회원가입</Button>
                    </Link>
                  )}
                </>
              )}
            </div>
          )}
        </div>
      </div>
    </header>
  )
}

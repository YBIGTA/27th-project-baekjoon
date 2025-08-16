import { Button } from "@/components/ui/button"
import { Link } from '@tanstack/react-router'

interface HeaderProps {
  showAuthButtons?: boolean
  currentPage?: "login" | "signup" | "home"
}

export default function Header({ showAuthButtons = true, currentPage = "home" }: HeaderProps) {
  return (
    <header className="w-full bg-card shadow-sm border-b border-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex justify-between items-center">
          <Link to="/">
            <h1 className="text-2xl font-bold text-primary font-[family-name:var(--font-playfair)] cursor-pointer hover:text-primary/80">
              BaekjoonHelper
            </h1>
          </Link>
          {showAuthButtons && (
            <div className="flex gap-3">
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
            </div>
          )}
        </div>
      </div>
    </header>
  )
}

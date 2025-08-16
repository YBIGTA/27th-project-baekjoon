import { Eye, EyeOff } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { useState } from "react"
import { Link, createFileRoute } from '@tanstack/react-router'
import Header from "@/components/organisms/header"
import Footer from "@/components/organisms/footer"


export const Route = createFileRoute('/login')({
  component: LoginPage,
})


function LoginPage() {
  const [showPassword, setShowPassword] = useState(false)

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Header currentPage="login" />

      {/* Main Content */}
      <main className="flex-1 flex items-center justify-center px-4 sm:px-6 lg:px-8">
        <div className="w-full max-w-md space-y-8">
          {/* Title */}
          <div className="text-center space-y-2">
            <h2 className="text-3xl font-bold text-foreground font-[family-name:var(--font-playfair)]">로그인</h2>
            <p className="text-muted-foreground">계정에 로그인하여 BaekjoonHelper를 이용하세요</p>
          </div>

          {/* Login Form */}
          <div className="space-y-6">
            <div className="space-y-4">
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-foreground mb-2">
                  이메일
                </label>
                <Input
                  id="email"
                  type="email"
                  placeholder="이메일을 입력하세요"
                  className="w-full bg-input border-border"
                />
              </div>

              <div>
                <label htmlFor="password" className="block text-sm font-medium text-foreground mb-2">
                  비밀번호
                </label>
                <div className="relative">
                  <Input
                    id="password"
                    type={showPassword ? "text" : "password"}
                    placeholder="비밀번호를 입력하세요"
                    className="w-full pr-12 bg-input border-border"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-muted-foreground hover:text-foreground"
                  >
                    {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                  </button>
                </div>
              </div>
            </div>

            <div className="flex items-center justify-between">
              <label className="flex items-center">
                <input type="checkbox" className="mr-2 rounded border-border" />
                <span className="text-sm text-muted-foreground">로그인 상태 유지</span>
              </label>
              <Link to="." className="text-sm text-primary hover:text-primary/80">
                비밀번호 찾기
              </Link>
            </div>

            <Button className="w-full bg-primary hover:bg-primary/90 text-primary-foreground py-3">로그인</Button>

            <div className="text-center">
              <span className="text-muted-foreground">계정이 없으신가요? </span>
              <Link to="/signup" className="text-primary hover:text-primary/80 font-medium">
                회원가입
              </Link>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  )
}

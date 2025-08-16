import { Eye, EyeOff } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { useState } from "react"
import { Link, createFileRoute } from '@tanstack/react-router'
import Header from "@/components/organisms/header"
import Footer from "@/components/organisms/footer"


export const Route = createFileRoute('/signup')({
  component: SignupPage,
})

function SignupPage() {
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Header currentPage="signup" />

      {/* Main Content */}
      <main className="flex-1 flex items-center justify-center px-4 sm:px-6 lg:px-8 py-8">
        <div className="w-full max-w-md space-y-8">
          {/* Title */}
          <div className="text-center space-y-2">
            <h2 className="text-3xl font-bold text-foreground font-[family-name:var(--font-playfair)]">회원가입</h2>
            <p className="text-muted-foreground">새 계정을 만들어 BaekjoonHelper를 시작하세요</p>
          </div>

          {/* Signup Form */}
          <div className="space-y-6">
            <div className="space-y-4">
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-foreground mb-2">
                  이름
                </label>
                <Input
                  id="name"
                  type="text"
                  placeholder="이름을 입력하세요"
                  className="w-full bg-input border-border"
                />
              </div>

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
                <p className="text-xs text-muted-foreground mt-1">8자 이상, 영문, 숫자, 특수문자 포함</p>
              </div>

              <div>
                <label htmlFor="confirmPassword" className="block text-sm font-medium text-foreground mb-2">
                  비밀번호 확인
                </label>
                <div className="relative">
                  <Input
                    id="confirmPassword"
                    type={showConfirmPassword ? "text" : "password"}
                    placeholder="비밀번호를 다시 입력하세요"
                    className="w-full pr-12 bg-input border-border"
                  />
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-muted-foreground hover:text-foreground"
                  >
                    {showConfirmPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                  </button>
                </div>
              </div>
            </div>

            <div className="space-y-4">
              <label className="flex items-start">
                <input type="checkbox" className="mr-3 mt-1 rounded border-border" />
                <span className="text-sm text-muted-foreground">
                  <Link to="." className="text-primary hover:text-primary/80">
                    이용약관
                  </Link>{" "}
                  및{" "}
                  <Link to="." className="text-primary hover:text-primary/80">
                    개인정보처리방침
                  </Link>
                  에 동의합니다
                </span>
              </label>

              <label className="flex items-start">
                <input type="checkbox" className="mr-3 mt-1 rounded border-border" />
                <span className="text-sm text-muted-foreground">마케팅 정보 수신에 동의합니다 (선택)</span>
              </label>
            </div>

            <Button className="w-full bg-primary hover:bg-primary/90 text-primary-foreground py-3">회원가입</Button>

            <div className="text-center">
              <span className="text-muted-foreground">이미 계정이 있으신가요? </span>
              <Link to="/login" className="text-primary hover:text-primary/80 font-medium">
                로그인
              </Link>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  )
}

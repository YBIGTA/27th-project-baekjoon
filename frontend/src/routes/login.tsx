import { Eye, EyeOff } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Spinner } from "@/components/ui/spinner"
import { useState } from "react"
import { Link, createFileRoute } from '@tanstack/react-router'
import { cn } from "@/lib/utils"
import Header from "@/components/organisms/header"
import Footer from "@/components/organisms/footer"


export const Route = createFileRoute('/login')({
  component: LoginPage,
})


function LoginPage() {
  const [showPassword, setShowPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    rememberMe: false
  })
  const [errors, setErrors] = useState<{[key: string]: string}>({})

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }))
    }
  }

  const validateForm = () => {
    const newErrors: {[key: string]: string} = {}
    
    if (!formData.email) {
      newErrors.email = '이메일을 입력해주세요'
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = '올바른 이메일 형식을 입력해주세요'
    }
    
    if (!formData.password) {
      newErrors.password = '비밀번호를 입력해주세요'
    } else if (formData.password.length < 6) {
      newErrors.password = '비밀번호는 6자 이상이어야 합니다'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!validateForm()) return
    
    setIsLoading(true)
    
    try {
      // TODO: 실제 로그인 API 호출
      console.log('로그인 시도:', formData)
      
      // 시뮬레이션을 위한 지연
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // TODO: 로그인 성공 후 리다이렉트
      console.log('로그인 성공!')
      
    } catch (error) {
      console.error('로그인 실패:', error)
      setErrors({ general: '로그인에 실패했습니다. 이메일과 비밀번호를 확인해주세요.' })
    } finally {
      setIsLoading(false)
    }
  }

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
          <form onSubmit={handleSubmit} className="space-y-6">
            {errors.general && (
              <div className="p-3 bg-destructive/10 border border-destructive/20 rounded-md">
                <p className="text-sm text-destructive">{errors.general}</p>
              </div>
            )}
            
            <div className="space-y-4">
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-foreground mb-2">
                  이메일
                </label>
                <Input
                  id="email"
                  name="email"
                  type="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  placeholder="이메일을 입력하세요"
                  className={cn(
                    "w-full",
                    errors.email && "border-destructive focus-visible:ring-destructive/20"
                  )}
                  required
                />
                {errors.email && (
                  <p className="text-sm text-destructive mt-1">{errors.email}</p>
                )}
              </div>

              <div>
                <label htmlFor="password" className="block text-sm font-medium text-foreground mb-2">
                  비밀번호
                </label>
                <div className="relative">
                  <Input
                    id="password"
                    name="password"
                    type={showPassword ? "text" : "password"}
                    value={formData.password}
                    onChange={handleInputChange}
                    placeholder="비밀번호를 입력하세요"
                    className={cn(
                      "w-full pr-12",
                      errors.password && "border-destructive focus-visible:ring-destructive/20"
                    )}
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                  >
                    {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                  </button>
                </div>
                {errors.password && (
                  <p className="text-sm text-destructive mt-1">{errors.password}</p>
                )}
              </div>
            </div>

            <div className="flex items-center justify-between">
              <label className="flex items-center space-x-2 cursor-pointer">
                <input 
                  type="checkbox" 
                  name="rememberMe"
                  checked={formData.rememberMe}
                  onChange={handleInputChange}
                  className="rounded border-border text-primary focus:ring-primary"
                />
                <span className="text-sm text-muted-foreground">로그인 상태 유지</span>
              </label>
              <Link to="." className="text-sm text-primary hover:text-primary/80">
                비밀번호 찾기
              </Link>
            </div>

            <Button 
              type="submit" 
              className="w-full bg-black hover:bg-gray-800 text-white py-3 text-base font-medium transition-colors"
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <Spinner size="sm" className="text-white" />
                  로그인 중...
                </>
              ) : (
                '로그인'
              )}
            </Button>

            <div className="text-center">
              <span className="text-muted-foreground">계정이 없으신가요? </span>
              <Link to="/signup" className="text-primary hover:text-primary/80 font-medium">
                회원가입
              </Link>
            </div>
          </form>
        </div>
      </main>

      <Footer />
    </div>
  )
}

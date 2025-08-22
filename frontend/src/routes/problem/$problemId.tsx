import { useState } from 'react'
import { createFileRoute } from '@tanstack/react-router'
import { useMutation } from '@tanstack/react-query'
import { ChevronDown, ChevronUp, Play, RotateCcw, Save } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Spinner } from "@/components/ui/spinner"
import Header from "@/components/organisms/header"
import Footer from "@/components/organisms/footer"


export const Route = createFileRoute('/problem/$problemId')({
  component: SearchResultPage,
})


interface CodeExecutionResult {
  output: string
  executionTime: number
  memoryUsage: number
  status: 'accepted' | 'wrong_answer' | 'time_limit_exceeded' | 'memory_limit_exceeded' | 'runtime_error'
  counterExample?: string
}

function SearchResultPage() {
  const { problemId } = Route.useParams()
  const [code, setCode] = useState(`// 여기에 코드를 작성하세요`)
  const [isTerminalOpen, setIsTerminalOpen] = useState(false)
  const [output, setOutput] = useState("")
  const [selectedLanguage, setSelectedLanguage] = useState("javascript")

  const [counterExample, setCounterExample] = useState<string | null>(null)
  const [executionResult, setExecutionResult] = useState<CodeExecutionResult | null>(null)

  // React Query를 사용한 코드 실행 함수
  const executeCodeMutation = useMutation({
    mutationFn: async ({ language, code }: { language: string; code: string }): Promise<CodeExecutionResult> => {
      const response = await fetch('http://localhost:8000/execute-code', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          language,
          code
        })
      })

      if (!response.ok) {
        throw new Error('코드 실행 실패')
      }

      return await response.json()
    }
  })

  // React Query를 사용한 결과 저장 함수
  const saveResultMutation = useMutation({
    mutationFn: async ({ problemId, code, counterExample }: { problemId: string; code: string; counterExample?: string }) => {
      const token = localStorage.getItem('authToken')
      
      const response = await fetch('http://localhost:8000/solved-problems/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          problem_id: parseInt(problemId),
          solution_code: code,
          counter_example: counterExample || null
        })
      })

      if (!response.ok) {
        throw new Error('저장 실패')
      }

      return await response.json()
    }
  })

  const handleRunCode = async () => {
    setIsTerminalOpen(true)
    
    try {
      const result = await executeCodeMutation.mutateAsync({ 
        language: selectedLanguage, 
        code 
      })
      setExecutionResult(result)
      setOutput(result.output)
      setCounterExample(result.counterExample || null)
      
    } catch (error) {
      console.error('코드 실행 실패:', error)
      setOutput("코드 실행 중 오류가 발생했습니다.")
    }
  }

  const handleSaveResult = async () => {
    if (!executionResult) {
      alert('먼저 코드를 실행해주세요.')
      return
    }

    try {
      await saveResultMutation.mutateAsync({
        problemId,
        code,
        counterExample: executionResult.counterExample
      })
      alert('결과가 성공적으로 저장되었습니다!')
    } catch (error) {
      alert('저장에 실패했습니다. 로그인 상태를 확인해주세요.')
    }
  }

  const handleReset = () => {
    setCode("// 여기에 코드를 작성하세요")
    setOutput("")
    setExecutionResult(null)
    setCounterExample(null)
  }

  const handleLanguageChange = (language: string) => {
    setSelectedLanguage(language)
  }

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Header showAuthButtons={false} maxWidth={false} />

      <main className="flex-1 flex flex-col h-[calc(100vh-120px)]">
        <div className="flex-1 flex min-h-0">
          <div className="w-1/2 border-r border-border p-6 overflow-y-auto">
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="text-2xl font-bold">문제 {problemId}: 숫자 반환하기</CardTitle>
                  <Badge variant="secondary" className="bg-emerald-100 text-emerald-800">
                    Level 1
                  </Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-6">
                <div>
                  <h3 className="text-lg font-semibold mb-3">문제 설명</h3>
                  <p className="text-muted-foreground leading-relaxed">
                    정수 n이 주어졌을 때, n을 그대로 반환하는 함수를 작성하세요. 이는 기본적인 함수 작성 연습
                    문제입니다. 이 문제는 프로그래밍의 기초를 다지는 데 도움이 됩니다. 함수의 기본 구조를 이해하고,
                    매개변수를 받아서 그대로 반환하는 과정을 연습할 수 있습니다.
                  </p>
                </div>

                <div>
                  <h3 className="text-lg font-semibold mb-3">제한사항</h3>
                  <ul className="list-disc list-inside space-y-1 text-muted-foreground">
                    <li>n은 1 이상 1,000,000 이하의 정수입니다.</li>
                    <li>함수명은 solution으로 고정입니다.</li>
                    <li>시간 복잡도는 O(1)이어야 합니다.</li>
                    <li>공간 복잡도는 O(1)이어야 합니다.</li>
                  </ul>
                </div>

                <div>
                  <h3 className="text-lg font-semibold mb-3">입출력 예</h3>
                  <div className="bg-muted p-4 rounded-lg">
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="border-b border-border">
                          <th className="text-left py-2">n</th>
                          <th className="text-left py-2">result</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr>
                          <td className="py-1">5</td>
                          <td className="py-1">5</td>
                        </tr>
                        <tr>
                          <td className="py-1">123</td>
                          <td className="py-1">123</td>
                        </tr>
                        <tr>
                          <td className="py-1">999999</td>
                          <td className="py-1">999999</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-semibold mb-3">입출력 예 설명</h3>
                  <p className="text-muted-foreground">
                    입력받은 정수 n을 그대로 반환하면 됩니다. 이 문제는 함수의 기본 동작을 이해하는 데 중점을 둡니다.
                    별도의 계산이나 변환 없이 입력값을 그대로 출력하는 것이 핵심입니다.
                  </p>
                </div>

                <div>
                  <h3 className="text-lg font-semibold mb-3">힌트</h3>
                  <p className="text-muted-foreground">
                    이 문제는 매우 간단합니다. 함수에서 매개변수로 받은 값을 return 문을 사용해 그대로 반환하면 됩니다.
                    각 언어별로 함수 선언 방식이 다르니 선택한 언어의 문법을 확인해보세요.
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>

          <div className="w-1/2 flex flex-col min-h-0">
            <div className="p-4 border-b border-border">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <h3 className="text-lg font-semibold">코드 작성</h3>
                  <Select value={selectedLanguage} onValueChange={handleLanguageChange}>
                    <SelectTrigger className="w-32">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="javascript">JavaScript</SelectItem>
                      <SelectItem value="python">Python</SelectItem>
                      <SelectItem value="java">Java</SelectItem>
                      <SelectItem value="cpp">C++</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="flex gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={handleReset}
                    className="flex items-center gap-2 bg-transparent"
                  >
                    <RotateCcw className="h-4 w-4" />
                    초기화
                  </Button>
                                      <Button 
                      onClick={handleRunCode} 
                      disabled={executeCodeMutation.isPending}
                      className="flex items-center gap-2 bg-primary hover:bg-primary/90 disabled:opacity-50"
                    >
                      {executeCodeMutation.isPending ? (
                      <>
                        <Spinner size="sm" />
                        실행 중...
                      </>
                    ) : (
                      <>
                        <Play className="h-4 w-4" />
                        실행
                      </>
                    )}
                  </Button>
                                      <Button 
                      onClick={handleSaveResult}
                      disabled={!executionResult || saveResultMutation.isPending}
                      variant="outline"
                      className="flex items-center gap-2"
                    >
                      {saveResultMutation.isPending ? (
                      <>
                        <Spinner size="sm" />
                        저장 중...
                      </>
                    ) : (
                      <>
                        <Save className="h-4 w-4" />
                        저장
                      </>
                    )}
                  </Button>
                </div>
              </div>
            </div>

            <div className={`flex-1 p-4 min-h-0 ${isTerminalOpen ? "flex-[0.6]" : "flex-1"}`}>
              <Textarea
                value={code}
                onChange={(e) => setCode(e.target.value)}
                className="w-full h-full font-mono text-sm resize-none border-border"
                placeholder="코드를 입력하세요..."
              />
            </div>

            <div className="border-t border-border">
              <div
                className="flex items-center justify-between p-3 bg-muted cursor-pointer hover:bg-muted/80"
                onClick={() => setIsTerminalOpen(!isTerminalOpen)}
              >
                <h3 className="text-sm font-semibold">실행 결과</h3>
                {isTerminalOpen ? <ChevronDown className="h-4 w-4" /> : <ChevronUp className="h-4 w-4" />}
              </div>
              {isTerminalOpen && (
                <div className="h-48 p-4 bg-card border-t border-border overflow-y-auto">
                  <pre className="text-sm font-mono text-muted-foreground whitespace-pre-wrap">
                    {output || "실행 버튼을 클릭하여 코드를 실행하세요."}
                  </pre>
                  {executionResult && (
                    <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-md">
                      <h4 className="font-semibold text-blue-800 mb-2">실행 정보</h4>
                      <div className="text-sm text-blue-700 space-y-1">
                        <div>실행 시간: {executionResult.executionTime}ms</div>
                        <div>메모리 사용량: {executionResult.memoryUsage.toFixed(2)}MB</div>
                        <div>상태: {executionResult.status}</div>
                      </div>
                    </div>
                  )}
                  {counterExample && (
                    <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-md">
                      <h4 className="font-semibold text-green-800 mb-2">반례 탐색 결과</h4>
                      <pre className="text-sm font-mono text-green-700 whitespace-pre-wrap">
                        {counterExample}
                      </pre>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  )
}
import { useState } from "react"
import { createFileRoute } from '@tanstack/react-router'
import { ChevronDown, ChevronUp, Play, RotateCcw } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import Header from "@/components/organisms/header"
import Footer from "@/components/organisms/footer"


export const Route = createFileRoute('/problem/$problemId')({
  component: SearchResultPage,
})


function SearchResultPage() {
  const { problemId } = Route.useParams()
  const [code, setCode] = useState(`// 여기에 코드를 작성하세요`)
  const [isTerminalOpen, setIsTerminalOpen] = useState(false)
  const [output, setOutput] = useState("")
  const [selectedLanguage, setSelectedLanguage] = useState("javascript")

  const handleRunCode = () => {
    // 간단한 코드 실행 시뮬레이션
    setOutput("실행 결과:\n입력: 5\n출력: 5\n\n테스트 케이스 1: 통과\n테스트 케이스 2: 통과")
    setIsTerminalOpen(true)
  }

  const handleReset = () => {
    setCode("// 여기에 코드를 작성하세요")
    setOutput("")
  }

  const handleLanguageChange = (language: string) => {
    setSelectedLanguage(language)
  }

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Header showAuthButtons={false} maxWidth={false} />

      <main className="flex-1 flex flex-col h-[calc(100vh-120px)]">
        {/* Main Content Area */}
        <div className="flex-1 flex min-h-0">
          {/* Left Panel - Problem Description */}
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

          {/* Right Panel - Code Editor and Terminal */}
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
                  <Button onClick={handleRunCode} className="flex items-center gap-2 bg-primary hover:bg-primary/90">
                    <Play className="h-4 w-4" />
                    실행
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
                <h3 className="text-sm font-semibold">반례</h3>
                {isTerminalOpen ? <ChevronDown className="h-4 w-4" /> : <ChevronUp className="h-4 w-4" />}
              </div>
              {isTerminalOpen && (
                <div className="h-48 p-4 bg-card border-t border-border overflow-y-auto">
                  <pre className="text-sm font-mono text-muted-foreground whitespace-pre-wrap">
                    {output || "실행 버튼을 클릭하여 코드를 실행하세요."}
                  </pre>
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
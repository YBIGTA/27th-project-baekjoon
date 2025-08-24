import { useState, useCallback } from "react"
import { createFileRoute, redirect } from '@tanstack/react-router'
import { ChevronDown, ChevronUp, Play, RotateCcw } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Spinner } from "@/components/ui/spinner"
import Header from "@/components/organisms/header"
import Footer from "@/components/organisms/footer"
import { Protected } from '@/components/Protected'
import Editor from '@monaco-editor/react'
import { ProblemViewer } from '@/components/organisms/problem-viewer'
import { useProblemMetadataQuery } from "@/api/problem"
import { tokenStorage, BASE_URL } from '@/api/auth'
import { CounterexampleEvent } from '@/api/websocket'
import useWebSocket, { ReadyState } from 'react-use-websocket'


export const Route = createFileRoute('/problem/$problemId')({
  beforeLoad: async ({ context, params }) => {
    // Auth check
    const token = tokenStorage.get()
    if (!token) {
      throw redirect({ to: '/login' })
    }

    // Param validation: only digits allowed
    if (!/^\d+$/.test(params.problemId)) {
      throw redirect({ to: '/' })
    }
  },
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
  const parsedProblemId = parseInt(problemId, 10)
  const { data, isLoading } = useProblemMetadataQuery(parsedProblemId)

  const [code, setCode] = useState(`// 여기에 코드를 작성하세요`)
  const [isTerminalOpen, setIsTerminalOpen] = useState(false)
  const [output, setOutput] = useState("")
  const [selectedLanguage, setSelectedLanguage] = useState("javascript")

  const [isRunning, setIsRunning] = useState(false)
  const [shouldConnect, setShouldConnect] = useState(false)
  const [runSeq, setRunSeq] = useState(0)
  const [currentNode, setCurrentNode] = useState<string | null>(null)
  const [counterExample, setCounterExample] = useState<string | null>(null)
  const [executionResult, setExecutionResult] = useState<CodeExecutionResult | null>(null)


  const wsUrl = `${BASE_URL.replace(/^http/, 'ws')}/ws/counterexample?run=${runSeq}`

  const { sendJsonMessage, readyState, getWebSocket } = useWebSocket(wsUrl, {
    share: false,
    shouldReconnect: () => false,
    onOpen: () => {
      sendJsonMessage({
        problem_id: parsedProblemId,
        user_code: code,
        language: selectedLanguage,
      })
    },
    onMessage: (e: MessageEvent) => {
      try {
        const ev = JSON.parse(e.data) as CounterexampleEvent
        if (ev.type === 'node_update') {
          setCurrentNode(ev.node)
          setOutput(prev => prev + `\n[노드] ${ev.node}`)
        } else if (ev.type === 'token') {
          setOutput(prev => prev + ev.content)
        } else if (ev.type === 'message') {
          setOutput(prev => prev + `\n[메시지] ${ev.content}`)
        } else if (ev.type === 'error') {
          setOutput(prev => prev + `\n[에러] ${ev.message}`)
          setIsRunning(false)
          setShouldConnect(false)
        } else if (ev.type === 'finish') {
          if (ev.counterexample_found && ev.counterexample_input) {
            setCounterExample(`반례 발견!\n\n입력:\n${ev.counterexample_input}`)
          } else {
            setCounterExample('반례를 찾지 못했습니다.')
          }
          setIsRunning(false)
          setShouldConnect(false)
        }
      } catch (err) {
        setOutput(prev => prev + `\n[파싱오류] ${(err as Error).message}`)
      }
    },
    onClose: () => {
      setIsRunning(false)
    }
  }, shouldConnect)

  const handleRunCode = useCallback(() => {
    setOutput('')
    setCounterExample(null)
    setCurrentNode(null)
    setIsTerminalOpen(true)
    setIsRunning(true)
    setRunSeq(s => s + 1)
    setShouldConnect(true)
  }, [])

  const handleReset = () => {
    try {
      getWebSocket()?.close()
    } catch (err) {
      console.error("WebSocket close error:", err)
    }
    setShouldConnect(false)
    setCode("// 여기에 코드를 작성하세요")
    setOutput("")
    setExecutionResult(null)
    setCounterExample(null)
    setCurrentNode(null)
  }

  const handleLanguageChange = (language: string) => {
    setSelectedLanguage(language)
  }

  return (
  <Protected>
    <div className="min-h-screen bg-background flex flex-col">
      <Header showAuthButtons={false} maxWidth={false} />

      <main className="flex-1 flex flex-col h-[calc(100vh-120px)]">
        <div className="flex-1 flex min-h-0">
          <div className="w-[42%] border-r border-border p-5 overflow-y-auto bg-muted/20">
            <ProblemViewer 
              loading={isLoading}
              problemId={problemId}
              title={data?.title}
              difficulty={data?.difficulty}
              description={data?.description}
            />
          </div>

          <div className="flex-1 flex flex-col min-h-0">
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
                    disabled={isRunning}
                    className="flex items-center gap-2 bg-primary hover:bg-primary/90 disabled:opacity-50"
                  >
                    {isRunning ? (
                      <>
                        <Spinner size="sm" className="text-white"/>
                        실행 중...
                      </>
                    ) : (
                      <>
                        <Play className="h-4 w-4" />
                        실행
                      </>
                    )}
                  </Button>
                </div>
              </div>
            </div>

            <div className={`flex-1 p-0 min-h-0 ${isTerminalOpen ? "flex-[0.6]" : "flex-1"}`}>
              <Editor
                value={code}
                onChange={(newValue) => setCode(newValue || '')}
                language={selectedLanguage}
                theme="light"
                options={{
                  selectOnLineNumbers: true,
                  automaticLayout: true,
                  scrollBeyondLastLine: false,
                  wordWrap: 'off',
                  minimap: { enabled: false },
                  fontSize: 14,
                  lineNumbers: 'on',
                  folding: true,
                  insertSpaces: true,
                  renderWhitespace: 'selection',
                  bracketPairColorization: { enabled: true },
                  guides: {
                    bracketPairs: true,
                    indentation: true
                  }
                }}
              />
            </div>

            <div className={`border-t border-border flex flex-col ${isTerminalOpen ? "flex-1" : ""}`}>
              <div
                className="flex items-center justify-between p-3 bg-muted cursor-pointer hover:bg-muted/80"
                onClick={() => setIsTerminalOpen(!isTerminalOpen)}
              >
                <h3 className="text-sm font-semibold">실행 결과</h3>
                {isTerminalOpen ? <ChevronDown className="h-4 w-4" /> : <ChevronUp className="h-4 w-4" />}
              </div>
              {isTerminalOpen && (
                <div className="h-48 p-4 bg-card border-t border-border overflow-y-auto flex-1">
                  <pre className="text-sm font-mono text-muted-foreground whitespace-pre-wrap">
                    {output || "실행 버튼을 클릭하여 코드를 실행하세요."}
                    {currentNode && `\n현재 노드: ${currentNode}`}
                    {isRunning && `\n상태: ${ReadyState[readyState]}`}
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
  </Protected>
  )
}
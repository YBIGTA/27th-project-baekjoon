import { useState, useCallback } from "react"
import { createFileRoute, redirect } from '@tanstack/react-router'
import { ChevronDown, ChevronUp, Play, RotateCcw, Square } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import Header from "@/components/organisms/header"
import { Protected } from '@/components/Protected'
import Editor from '@monaco-editor/react'
import { ProblemViewer } from '@/components/organisms/problem-viewer'
import TerminalPanel from '@/components/organisms/TerminalPanel'
import { useProblemMetadataQuery } from "@/api/problem"
import { tokenStorage } from '@/api/auth'
import useCounterexample from '@/hooks/useCounterexample'
import NodeTimeline from '@/components/organisms/NodeTimeline'


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
  const {
    history,
    currentNode,
    counterExample,
    isRunning,
    readyState,
    run: runCounterexample,
    reset: resetCounterexample,
    close: closeCounterexample,
  } = useCounterexample()
  const [selectedLanguage, setSelectedLanguage] = useState("javascript")
  const [executionResult, setExecutionResult] = useState<CodeExecutionResult | null>(null)

  const handleRunOrStop = useCallback(() => {
    // 실행 중이면 중지 (웹소켓 종료)
    if (isRunning) {
      closeCounterexample()
      return
    }
    // 새 실행
    setIsTerminalOpen(true)
    runCounterexample({ problemId: parsedProblemId, code, language: selectedLanguage })
  }, [isRunning, parsedProblemId, code, selectedLanguage, runCounterexample, closeCounterexample])

  const handleReset = () => {
    closeCounterexample()
    resetCounterexample()
    setCode("// 여기에 코드를 작성하세요")
    setExecutionResult(null)
  }

  const handleLanguageChange = (language: string) => {
    setSelectedLanguage(language)
  }

  return (
  <Protected>
    <div className="min-h-screen bg-background flex flex-col h-screen">
      <Header showAuthButtons={false} maxWidth={false} />

      <main className="flex-1 flex flex-col h-[calc(100vh-65px)]">
        <div className="flex-1 flex min-h-0">
          <div className="w-[42%] border-r border-border p-5 overflow-y-scroll bg-muted/20">
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
                    onClick={handleRunOrStop}
                    className={`flex items-center gap-2 ${isRunning ? 'bg-primary hover:bg-primary/90' : 'bg-primary hover:bg-primary/90'}`}
                  >
                    {isRunning ? (
                      <>
                        <Square className="h-4 w-4" />
                        중지
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
                <div className="flex h-full">
                  <div className="w-40 border-r border-border border-t-1 p-2 overflow-y-auto bg-muted/30">
                    <NodeTimeline history={history} currentNode={currentNode} />
                  </div>
                  <div className="flex-1 flex flex-col">
                    <TerminalPanel
                      history={history}
                      currentNode={currentNode}
                      isRunning={isRunning}
                      readyState={readyState}
                      executionResult={executionResult}
                      counterExample={counterExample}
                    />
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  </Protected>
  )
}
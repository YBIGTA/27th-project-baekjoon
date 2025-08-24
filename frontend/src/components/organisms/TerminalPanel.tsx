import React from 'react'
import { ReadyState } from 'react-use-websocket'

interface CodeExecutionResult {
  output: string
  executionTime: number
  memoryUsage: number
  status: 'accepted' | 'wrong_answer' | 'time_limit_exceeded' | 'memory_limit_exceeded' | 'runtime_error'
  counterExample?: string
}

interface TerminalPanelProps {
  output: string
  currentNode: string | null
  isRunning: boolean
  readyState: ReadyState
  executionResult: CodeExecutionResult | null
  counterExample: string | null
}

const TerminalPanel: React.FC<TerminalPanelProps> = ({
  output,
  currentNode,
  isRunning,
  readyState,
  executionResult,
  counterExample,
}) => {
  return (
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
  )
}

export default TerminalPanel

import { useCallback, useRef, useState } from 'react'
import useWebSocket, { ReadyState } from 'react-use-websocket'
import { CounterexampleEvent } from '@/api/websocket'
import { BASE_URL } from '@/api/auth'
import { NodeType } from '@/api/websocket'

export interface HistoryItemBase {
  id: string
  t: number // timestamp
  type: 'node' | 'token_stream' | 'message' | 'error' | 'finish'
}

export interface NodeHistoryItem extends HistoryItemBase {
  type: 'node'
  node: string
  data?: any
}

export interface TokenStreamHistoryItem extends HistoryItemBase {
  type: 'token_stream'
  node?: string
  content: string
}

export interface MessageHistoryItem extends HistoryItemBase {
  type: 'message'
  content: string
}

export interface ErrorHistoryItem extends HistoryItemBase {
  type: 'error'
  message: string
}

export interface FinishHistoryItem extends HistoryItemBase {
  type: 'finish'
  counterexample_found: boolean
  counterexample_input?: string
}

export type HistoryItem = NodeHistoryItem | TokenStreamHistoryItem | MessageHistoryItem | ErrorHistoryItem | FinishHistoryItem

interface UseCounterexampleReturn {
  history: HistoryItem[]
  currentNode: string | null
  counterExample: string | null
  isRunning: boolean
  readyState: ReadyState
  run: (params: { problemId: number; code: string; language: string }) => void
  reset: () => void
  close: () => void
  runSeq: number
}

function get_current_node(e: CounterexampleEvent): string | null {
  if (e.type === 'finish' || e.type === 'error')
    return null
  if (e.type === 'node_update')
    switch (e.node) {
      case NodeType.Solve:
        return NodeType.BojSubmit
      case NodeType.BojSubmit:
        if (e.data.is_solution_validated)
          return NodeType.GenerateInputs
        else
          return NodeType.Solve
      case NodeType.GenerateInputs:
        return NodeType.RunAndCompare
      case NodeType.RunAndCompare:
        if (e.data.counterexample_found)
          return null
        else
          return NodeType.GenerateInputs
      default:
        return null
    }
  return null
}

export function useCounterexample(): UseCounterexampleReturn {
  const [history, setHistory] = useState<HistoryItem[]>([])
  const [currentNode, setCurrentNode] = useState<string | null>(null)
  const [counterExample, setCounterExample] = useState<string | null>(null)
  const [isRunning, setIsRunning] = useState(false)
  const [shouldConnect, setShouldConnect] = useState(false)
  const [runSeq, setRunSeq] = useState(0)

  // Store payload for the next connection open
  const pendingPayloadRef = useRef<{ problemId: number; code: string; language: string } | null>(null)

  const wsUrl = `${BASE_URL.replace(/^http/, 'ws')}/ws/counterexample?run=${runSeq}`

  const { readyState, getWebSocket, sendJsonMessage } = useWebSocket(wsUrl, {
    share: false,
    shouldReconnect: () => false,
    onOpen: () => {
      const payload = pendingPayloadRef.current
      if (payload) {
        sendJsonMessage({
          problem_id: payload.problemId,
            user_code: payload.code,
            language: payload.language,
        })
      }
      setCurrentNode('solve')
    },
    onMessage: (e: MessageEvent) => {
      try {
        const ev = JSON.parse(e.data) as CounterexampleEvent
        console.debug(ev)
        const now = Date.now()
        switch (ev.type) {
          case 'node_update': {
            setCurrentNode(get_current_node(ev))
            setHistory(prev => [
              ...prev,
              { id: crypto.randomUUID(), t: now, type: 'node', node: ev.node, data: ev.data }
            ])
            break
          }
          case 'token': {
            setHistory(prev => {
              const last = prev[prev.length - 1]
              if (last && last.type === 'token_stream') {
                // merge
                return [
                  ...prev.slice(0, -1),
                  { ...last, content: last.content + ev.content }
                ]
              }
              return [
                ...prev,
                { id: crypto.randomUUID(), t: now, type: 'token_stream', node: ev.node, content: ev.content }
              ]
            })
            break
          }
          case 'message': {
            setHistory(prev => [
              ...prev,
              { id: crypto.randomUUID(), t: now, type: 'message', content: ev.content || '' }
            ])
            break
          }
          case 'error': {
            setHistory(prev => [
              ...prev,
              { id: crypto.randomUUID(), t: now, type: 'error', message: ev.message }
            ])
            setIsRunning(false)
            setShouldConnect(false)
            break
          }
          case 'finish': {
            if (ev.counterexample_found && ev.counterexample_input) {
              setCounterExample(`반례 발견!\n\n입력:\n${ev.counterexample_input}`)
            } else {
              setCounterExample('반례를 찾지 못했습니다.')
            }
            setHistory(prev => [
              ...prev,
              { id: crypto.randomUUID(), t: now, type: 'finish', counterexample_found: ev.counterexample_found, counterexample_input: ev.counterexample_input }
            ])
            setIsRunning(false)
            setShouldConnect(false)
            break
          }
        }
      } catch (err) {
        setHistory(prev => [
          ...prev,
          { id: crypto.randomUUID(), t: Date.now(), type: 'error', message: `[파싱오류] ${(err as Error).message}` }
        ])
      }
    },
    onClose: () => {
      setIsRunning(false)
    }
  }, shouldConnect)

  const run = useCallback(({ problemId, code, language }: { problemId: number; code: string; language: string }) => {
    setHistory([])
    setCurrentNode(null)
    setCounterExample(null)
    setIsRunning(true)
    pendingPayloadRef.current = { problemId, code, language }
    // trigger new connection
    setRunSeq(s => s + 1)
    setShouldConnect(true)
  }, [])

  const close = useCallback(() => {
    try { getWebSocket()?.close() } catch (_) {}
    setShouldConnect(false)
  }, [getWebSocket])

  const reset = useCallback(() => {
    close()
    setHistory([])
    setCurrentNode(null)
    setCounterExample(null)
    setIsRunning(false)
  }, [close])

  return { history, currentNode, counterExample, isRunning, readyState, run, reset, close, runSeq }
}

export default useCounterexample

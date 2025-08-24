import { useCallback, useRef, useState } from 'react'
import useWebSocket, { ReadyState } from 'react-use-websocket'
import { CounterexampleEvent } from '@/api/websocket'
import { BASE_URL } from '@/api/auth'

interface UseCounterexampleReturn {
  output: string
  currentNode: string | null
  counterExample: string | null
  isRunning: boolean
  readyState: ReadyState
  run: (params: { problemId: number; code: string; language: string }) => void
  reset: () => void
  close: () => void
  runSeq: number
}

export function useCounterexample(): UseCounterexampleReturn {
  const [output, setOutput] = useState('')
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
    },
    onMessage: (e: MessageEvent) => {
      try {
        const ev = JSON.parse(e.data) as CounterexampleEvent
        switch (ev.type) {
          case 'node_update':
            setCurrentNode(ev.node)
            setOutput(prev => prev + `\n[노드] ${ev.node}`)
            break
          case 'token':
            setOutput(prev => prev + ev.content)
            break
          case 'message':
            setOutput(prev => prev + `\n[메시지] ${ev.content}`)
            break
          case 'error':
            setOutput(prev => prev + `\n[에러] ${ev.message}`)
            setIsRunning(false)
            setShouldConnect(false)
            break
          case 'finish':
            if (ev.counterexample_found && ev.counterexample_input) {
              setCounterExample(`반례 발견!\n\n입력:\n${ev.counterexample_input}`)
            } else {
              setCounterExample('반례를 찾지 못했습니다.')
            }
            setIsRunning(false)
            setShouldConnect(false)
            break
        }
      } catch (err) {
        setOutput(prev => prev + `\n[파싱오류] ${(err as Error).message}`)
      }
    },
    onClose: () => {
      setIsRunning(false)
    }
  }, shouldConnect)

  const run = useCallback(({ problemId, code, language }: { problemId: number; code: string; language: string }) => {
    setOutput('')
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
    setOutput('')
    setCurrentNode(null)
    setCounterExample(null)
    setIsRunning(false)
  }, [close])

  return { output, currentNode, counterExample, isRunning, readyState, run, reset, close, runSeq }
}

export default useCounterexample

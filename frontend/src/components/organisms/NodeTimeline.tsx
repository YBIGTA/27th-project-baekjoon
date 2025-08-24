import React, { useMemo } from 'react'
import { HistoryItem, NodeHistoryItem, FinishHistoryItem } from '@/hooks/useCounterexample'
import { CheckCircle2, Loader2, Circle, XCircle } from 'lucide-react'

interface NodeTimelineProps {
  history: HistoryItem[]
  currentNode: string | null
  className?: string
}

const ORDER = ['solve', 'boj_submit', 'generate_inputs', 'run_and_compare']

export const NodeTimeline: React.FC<NodeTimelineProps> = ({ history, currentNode, className }) => {
  const statusMap = useMemo(() => {
    const map: Record<string, { started: boolean; finished: boolean; failed: boolean; counterexample?: boolean }> = {}
    for (const node of ORDER) map[node] = { started: false, finished: false, failed: false }
    for (const item of history) {
      if (item.type === 'node') {
        // mark started when first seen
        if (!map[item.node]) map[item.node] = { started: true, finished: false, failed: false }
        else map[item.node].started = true
      }
      if (item.type === 'finish') {
        // mark last node finish
        if (currentNode === null) {
          // ended
        }
      }
      if (item.type === 'error') {
        if (currentNode) {
          map[currentNode] = { ...(map[currentNode] || { started: true }), started: true, finished: true, failed: true }
        }
      }
    }
    return map
  }, [history, currentNode])

  return (
    <div className={className}>
      <ol className="flex flex-col gap-2">
        {ORDER.map(node => {
          const st = statusMap[node]
          const active = currentNode === node
          let icon: React.ReactNode = <Circle className="h-4 w-4 text-muted-foreground" />
          if (st?.failed) icon = <XCircle className="h-4 w-4 text-red-500" />
          else if (st?.finished) icon = <CheckCircle2 className="h-4 w-4 text-green-600" />
          else if (active) icon = <Loader2 className="h-4 w-4 animate-spin text-indigo-500" />
          else if (st?.started) icon = <Circle className="h-4 w-4 text-indigo-400" />
          return (
            <li key={node} className={`flex items-center gap-2 text-xs font-mono ${active ? 'text-indigo-600 font-semibold' : 'text-muted-foreground'}`}>
              {icon}
              <span>{node}</span>
            </li>
          )
        })}
      </ol>
    </div>
  )
}

export default NodeTimeline

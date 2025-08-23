import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import StyledMarkdown from '@/components/molecules/StyledMarkdown'

interface ProblemViewerProps {
  loading: boolean
  problemId: string | number
  title?: string
  difficulty?: number
  description?: string
}

export function ProblemViewer({ loading, problemId, title, difficulty, description }: ProblemViewerProps) {
  if (loading) {
    return (
      <Card>
        <CardHeader>
          <div className="flex items-start justify-between">
            <div className="space-y-3 w-full">
              <Skeleton className="h-7 w-56" />
              <div className="flex gap-2">
                <Skeleton className="h-4 w-24" />
                <Skeleton className="h-4 w-20" />
              </div>
            </div>
            <Skeleton className="h-6 w-20 rounded-full" />
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <Skeleton className="h-4 w-5/6" />
          <Skeleton className="h-4 w-4/6" />
          <Skeleton className="h-4 w-3/5" />
          <div className="space-y-2 pt-2">
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-11/12" />
            <Skeleton className="h-4 w-10/12" />
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-2xl font-bold">문제 {problemId}: {title}</CardTitle>
          {difficulty !== undefined && (
            <Badge variant="secondary" className="bg-emerald-100 text-emerald-800">
              Level {difficulty}
            </Badge>
          )}
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        <StyledMarkdown content={description || ''} />
      </CardContent>
    </Card>
  )
}

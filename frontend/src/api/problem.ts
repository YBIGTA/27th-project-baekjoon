import { useMutation, useQuery } from '@tanstack/react-query'
import { request } from './auth'

// Problem metadata response from backend (not wrapped in BaseResponse)
export type ProblemMetadata = {
  problem_id: number
  title: string
  description: string
  difficulty: number
  category: string
  created_at: string
}

// Counter example request/response types
export type CalcCounterExampleRequest = {
  user_code: string
  user_code_language: string
}

export type CalcCounterExampleResponse = {
  counter_example_input: string
}

// GET /problem/{id}
export function useProblemMetadataQuery(problemId: number | undefined, enabled = true) {
  return useQuery<ProblemMetadata, Error>({
    queryKey: ['problem', problemId],
    enabled: enabled && typeof problemId === 'number',
    queryFn: () => request<ProblemMetadata>(`/problem/${problemId}`),
    staleTime: 1000 * 60 * 5,
  })
}

// POST /problem/{id}/calc_counter_example
// Pass problemId as part of mutate arg for flexibility
export function useCalcCounterExampleMutation() {
  return useMutation<CalcCounterExampleResponse, Error, { problemId: number } & CalcCounterExampleRequest>({
    mutationFn: (vars) =>
      request<CalcCounterExampleResponse>(`/problem/${vars.problemId}/calc_counter_example`, {
        method: 'POST',
        body: JSON.stringify({
            user_code: vars.user_code,
            user_code_language: vars.user_code_language,
        }),
      }),
  })
}

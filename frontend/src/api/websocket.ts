export type CounterexampleEvent =
	| { type: 'token'; node: string; content: string }
	| { type: 'node_start'; node: string }
	| { type: 'node_end'; node: string; success?: boolean; counterexample_found?: boolean }
	| { type: 'node_update'; node: string; data?: any }
	| { type: 'message'; role?: string; content?: string }
	| { type: 'finish'; counterexample_found: boolean; counterexample_input?: string; counterexample_detail?: any; correct_solution?: string; input_generator?: string }
	| { type: 'error'; message: string; trace?: string };


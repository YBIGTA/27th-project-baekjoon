export type CounterexampleEvent =
	| { type: 'token'; node: string; content: string }
	| { type: 'node_start'; node: string }
	| { type: 'node_end'; node: string; success?: boolean; counterexample_found?: boolean }
	| { type: 'node_update'; node: string; data?: any }
	| { type: 'message'; role?: string; content?: string }
	| { type: 'finish'; counterexample_found: boolean; counterexample_input?: string; counterexample_detail?: any; correct_solution?: string; input_generator?: string }
	| { type: 'error'; message: string; trace?: string };

export function connectCounterexampleStream(
	baseUrl: string,
	params: { problemId: number; userCode: string; language: string },
	onEvent: (ev: CounterexampleEvent) => void,
): WebSocket {
	const wsUrl = baseUrl.replace(/^http/, 'ws') + '/ws/counterexample';
	const ws = new WebSocket(wsUrl);
	ws.onopen = () => {
		ws.send(
			JSON.stringify({
				problem_id: params.problemId,
				user_code: params.userCode,
				language: params.language,
			}),
		);
	};
	ws.onmessage = (e) => {
		try {
			const data = JSON.parse(e.data) as CounterexampleEvent;
			onEvent(data);
		} catch (err) {
			console.error('Invalid WS message', err, e.data);
		}
	};
	ws.onerror = (e) => {
		console.error('WS error', e);
	};
	return ws;
}

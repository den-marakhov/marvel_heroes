export const ERROR_KIND = {
	OFFLINE: 'offline',
	NETWORK: 'network',
	TIMEOUT: 'timeout',
	CLIENT: 'client',
	SERVER: 'server',
	PARSE: 'parse',
	UNKNOWN: 'unknown',
} as const;

export type ApiErrorKind = (typeof ERROR_KIND)[keyof typeof ERROR_KIND];

export const ERROR_MESSAGE: Record<ApiErrorKind, string> = {
	[ERROR_KIND.OFFLINE]: 'You are offline',
	[ERROR_KIND.NETWORK]: 'Server is unavailable',
	[ERROR_KIND.TIMEOUT]: 'Request timed out',
	[ERROR_KIND.CLIENT]: 'Something went wrong',
	[ERROR_KIND.SERVER]: 'Server error, please try later',
	[ERROR_KIND.PARSE]: 'Unexpected server response',
	[ERROR_KIND.UNKNOWN]: 'Something went wrong',
};

export const STATUS_MESSAGE: Partial<Record<number, string>> = {
	404: 'Hero not found',
	413: 'File is too large',
	422: 'Invalid request data',
};

export const TEMPORARY_ERROR_KINDS: ReadonlySet<ApiErrorKind> = new Set([
	ERROR_KIND.NETWORK,
	ERROR_KIND.SERVER,
	ERROR_KIND.TIMEOUT,
]);

export const REQUEST_TIMEOUT_MS = 15000;
export const UPLOAD_TIMEOUT_MS = 60000;

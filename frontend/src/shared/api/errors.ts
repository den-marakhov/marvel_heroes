import axios, { AxiosError } from 'axios';
import { ZodError } from 'zod';
import {
	ERROR_KIND,
	ERROR_MESSAGE,
	STATUS_MESSAGE,
	TEMPORARY_ERROR_KINDS,
	type ApiErrorKind,
} from './config';

interface IServerErrorBody {
	message?: unknown;
	detail?: unknown;
}

export class ApiError extends Error {
	readonly kind: ApiErrorKind;
	readonly status?: number;

	constructor(
		kind: ApiErrorKind,
		message: string = ERROR_MESSAGE[kind],
		status?: number,
	) {
		super(message);
		this.name = 'ApiError';
		this.kind = kind;
		this.status = status;
	}
}

const getKindByCode = (code?: string): ApiErrorKind | null => {
	switch (code) {
		case AxiosError.ECONNABORTED:
		case AxiosError.ETIMEDOUT:
			return ERROR_KIND.TIMEOUT;
		case AxiosError.ERR_NETWORK:
			return ERROR_KIND.NETWORK;
		default:
			return null;
	}
};

const getServerMessage = (data?: IServerErrorBody): string | null => {
	if (typeof data?.message === 'string') return data.message;
	if (typeof data?.detail === 'string') return data.detail;
	return null;
};

export const toApiError = (error: unknown): ApiError => {
	if (error instanceof ApiError) return error;
	if (error instanceof ZodError) return new ApiError(ERROR_KIND.PARSE);
	if (!axios.isAxiosError<IServerErrorBody>(error)) {
		return new ApiError(ERROR_KIND.UNKNOWN);
	}
	if (!navigator.onLine) return new ApiError(ERROR_KIND.OFFLINE);

	const kindByCode = getKindByCode(error.code);
	if (kindByCode) return new ApiError(kindByCode);
	if (!error.response) return new ApiError(ERROR_KIND.NETWORK);

	const { status, data } = error.response;
	const kind = status >= 500 ? ERROR_KIND.SERVER : ERROR_KIND.CLIENT;
	const message =
		getServerMessage(data) ?? STATUS_MESSAGE[status] ?? ERROR_MESSAGE[kind];

	return new ApiError(kind, message, status);
};

export const isTemporaryError = (error: unknown): boolean =>
	TEMPORARY_ERROR_KINDS.has(toApiError(error).kind);

import axios from 'axios';
import { REQUEST_TIMEOUT_MS } from './config';
import { toApiError } from './errors';

const api = axios.create({
	baseURL: '/api/v1',
	timeout: REQUEST_TIMEOUT_MS,
});

api.interceptors.response.use(
	response => response,
	error => Promise.reject(toApiError(error)),
);

export default api;

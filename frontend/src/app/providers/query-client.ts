import { isTemporaryError, toApiError } from '@/shared/api';
import { MutationCache, QueryCache, QueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';

declare module '@tanstack/react-query' {
	interface Register {
		mutationMeta: {
			silent?: boolean;
			errorMessage?: string;
		};
		queryMeta: {
			silent?: boolean;
		};
	}
}

const MAX_RETRIES = 2;

export const queryClient = new QueryClient({
	defaultOptions: {
		queries: {
			retry: (failureCount, error) =>
				isTemporaryError(error) && failureCount < MAX_RETRIES,
		},
	},
	queryCache: new QueryCache({
		onError: (error, query) => {
			if (query.meta?.silent) return;
			if (query.state.data === undefined) return;
			toast.error(`Failed to refresh data: ${toApiError(error).message}`);
		},
	}),
	mutationCache: new MutationCache({
		onError: (error, _variables, _context, mutation) => {
			if (mutation.meta?.silent) return;
			toast.error(mutation.meta?.errorMessage ?? toApiError(error).message);
		},
	}),
});

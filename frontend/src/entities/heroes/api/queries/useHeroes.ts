import { useQuery } from '@tanstack/react-query';
import { heroQueries } from './heroQueries';

export const useHeroes = () => {
	const { isLoading, isPending, isPaused, isError, data, error, refetch } =
		useQuery(heroQueries.list());

	return {
		isLoading,
		isPending,
		isPaused,
		isError,
		data,
		error,
		refetch,
	};
};

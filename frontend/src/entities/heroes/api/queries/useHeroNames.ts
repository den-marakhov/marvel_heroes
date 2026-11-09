import { useQuery } from '@tanstack/react-query';
import { heroQueries } from './heroQueries';

export const useHeroNames = () => {
	const { data, isLoading, isPending, isError, error, refetch } = useQuery(
		heroQueries.validNames(),
	);

	return {
		isLoading,
		isPending,
		isError,
		data,
		error,
		refetch,
	};
};

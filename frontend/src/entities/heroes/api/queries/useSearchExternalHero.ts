import { useQuery } from '@tanstack/react-query';
import { heroQueries } from './heroQueries';

export const useSearchExternalHeroes = (name: string) => {
	const { data, isPending, isPaused, isError, error, refetch } = useQuery(
		heroQueries.externalHeroSearch(name),
	);

	return {
		externalHeroes: data,
		isPending,
		isPaused,
		isError,
		error,
		refetch,
	};
};

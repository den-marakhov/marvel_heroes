import { useQuery } from '@tanstack/react-query';
import heroApi from '../api';

export const useHeroes = () => {
	const { isLoading, isError, data } = useQuery({
		queryKey: ['heroes'],
		queryFn: heroApi.getAll,
	});

	const hasHeroes = !!data && data.length > 0;

	return {
		hasHeroes,
		isLoading,
		isError,
		data,
	};
};

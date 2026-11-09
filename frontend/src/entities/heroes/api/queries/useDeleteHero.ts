import { useMutation, useQueryClient } from '@tanstack/react-query';

import { heroApi } from '../hero-api';
import { heroQueries } from './heroQueries';

export const useDeleteHero = () => {
	const queryClient = useQueryClient();

	const { mutate, isPending, isError, error, reset } = useMutation({
		mutationFn: (heroId: string) => heroApi.deleteHero(heroId),
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: heroQueries.all() });
		},
		meta: { silent: true },
	});

	return {
		deleteHero: mutate,
		isDeleting: isPending,
		isError,
		error,
		reset,
	};
};

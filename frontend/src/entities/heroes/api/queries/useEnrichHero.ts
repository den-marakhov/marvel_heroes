import { useMutation, useQueryClient } from '@tanstack/react-query';

import { heroApi } from '../hero-api';
import { heroQueries } from './heroQueries';

interface IEnrichHeroMutationFnProps {
	heroId: string;
	externalId: number;
}

export const useEnrichHero = () => {
	const queryClient = useQueryClient();

	const { mutate, isPending, isError, error, reset } = useMutation({
		mutationFn: ({ heroId, externalId }: IEnrichHeroMutationFnProps) =>
			heroApi.enrichHero(heroId, externalId),
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: heroQueries.all() });
		},
		meta: { silent: true },
	});

	return {
		enrichHero: mutate,
		isPending,
		isError,
		error,
		reset,
	};
};

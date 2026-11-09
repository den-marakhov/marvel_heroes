import { useMutation, useQueryClient } from '@tanstack/react-query';

import { heroApi } from '../hero-api';
import { heroQueries } from './heroQueries';

interface ICreateHeroMutationFnProps {
	name: string;
	description: string;
}

export const useCreateHero = () => {
	const queryClient = useQueryClient();

	const { mutate, isPending, isError, error, reset } = useMutation({
		mutationFn: ({ name, description }: ICreateHeroMutationFnProps) =>
			heroApi.createHero(name, description),
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: heroQueries.all() });
		},
		meta: { silent: true },
	});

	return {
		createHero: mutate,
		isCreating: isPending,
		isError,
		error,
		reset,
	};
}
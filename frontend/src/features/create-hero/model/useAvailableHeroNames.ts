import { useHeroes } from '@/entities/heroes';
import { useHeroNames } from '@/entities/heroes/api/queries/useHeroNames';

export const useAvailableHeroNames = () => {
	const {
		data: validNames,
		isPending: isPendingNames,
		isError: isErrorNames,
		error: namesError,
		refetch: refetchNames,
	} = useHeroNames();

	const {
		data: existingHeroes,
		isPending: isPendingHeroes,
		isError: isErrorHeroes,
		error: heroesError,
		refetch: refetchHeroes,
	} = useHeroes();

	const isPending = isPendingNames || isPendingHeroes;
	const isError = isErrorNames || isErrorHeroes;
	const error = namesError ?? heroesError;

	const refetch = () => {
		void refetchNames();
		void refetchHeroes();
	};

	const existingNamesList =
		existingHeroes?.map(hero => hero.name.toLowerCase()) || [];

	const availableNames =
		validNames?.filter(
			name => !existingNamesList.includes(name.toLowerCase()),
		) || [];

	const hasAvailableNames = availableNames.length > 0;

	return {
		availableNames,
		hasAvailableNames,
		isPending,
		isError,
		error,
		refetch,
	};
};

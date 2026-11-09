import { queryOptions } from '@tanstack/react-query';
import { heroApi } from '../hero-api';

export const heroQueries = {
	all: () => ['heroes'] as const,
	list: () =>
		queryOptions({
			queryKey: [...heroQueries.all(), 'list'],
			queryFn: heroApi.getAll,
		}),
	validNames: () => queryOptions({
		queryKey: [...heroQueries.all(), 'valid-names'],
		queryFn: heroApi.getHeroNames,
		staleTime: Infinity,
		meta: { silent: true },
	}),
	externalHeroSearch: (name: string) =>
		queryOptions({
			queryKey: [...heroQueries.all(), 'external-search', name],
			queryFn: () => heroApi.searchExternalHeroByName(name),
			enabled: Boolean(name),
			meta: { silent: true },
		}),
};

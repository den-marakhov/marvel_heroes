import api, { UPLOAD_TIMEOUT_MS } from '@/shared/api';
import {
	externalHeroDtoListScheme,
	heroDtoListScheme,
	heroDtoScheme,
	type ExternalHeroDTO,
	type HeroDTO,
} from './dto';
import { toExternalHero, toHero } from './mappers';

const SLUG = 'heroes';

interface IHeroValidNamesResponse {
	heroes_names: string[];
}

export const heroApi = {
	getHeroNames: async () => {
		return api
			.get<IHeroValidNamesResponse>(`/${SLUG}/valid-names`)
			.then(response => response.data.heroes_names);
	},

	getAll: async () => {
		return api
			.get<HeroDTO>(`/${SLUG}`)
			.then(response => heroDtoListScheme.parse(response.data))
			.then(dtos => dtos.map(toHero));
	},

	deleteHero: async (heroId: string) => {
		return api.delete(`/${SLUG}/${heroId}`);
	},

	uploadImage: async (
		heroId: string,
		file: File,
		onProgress?: (percent: number) => void,
	) => {
		const fromData = new FormData();
		fromData.append('file', file);

		return api
			.post<string>(`/${SLUG}/${heroId}/image-upload`, fromData, {
				timeout: UPLOAD_TIMEOUT_MS,
				onUploadProgress: event => {
					if (onProgress && event.total) {
						const currentProgress = Math.round(
							(event.loaded / event.total) * 100,
						);
						onProgress(currentProgress);
					}
				},
			})
			.then(response => response.data);
	},

	searchExternalHeroByName: async (name: string) => {
		return api
			.get<ExternalHeroDTO[]>(`/${SLUG}/search`, {
				params: { name },
			})
			.then(response => externalHeroDtoListScheme.parse(response.data))
			.then(dtos => dtos.map(toExternalHero));
	},

	enrichHero: async (heroId: string, externalId: number) => {
		return api
			.post<HeroDTO>(`/${SLUG}/${heroId}/enrich`, {
				external_id: externalId,
			})
			.then(response => heroDtoScheme.parse(response.data))
			.then(toHero);
	},

	createHero: async (name: string, description: string) => {
		return api
			.post<HeroDTO>(`/${SLUG}`, {
				name,
				description,
			})
			.then(response => heroDtoScheme.parse(response.data))
			.then(toHero);
	}
};

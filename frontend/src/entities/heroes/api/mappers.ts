import type { IExternalHero, IHero } from '../model/types';
import type { ExternalHeroDTO, HeroDTO } from './dto';

export const toHero = (dto: HeroDTO): IHero => ({
	heroId: dto.hero_id,
	name: dto.name,
	description: dto.description,
	fullName: dto.full_name ?? undefined,
	publisher: dto.publisher ?? undefined,
	uploadedImgUrl: dto.uploaded_img_url ?? undefined,
	createdAt: dto.created_at,
	updatedAt: dto.updated_at,
});

export const toExternalHero = (dto: ExternalHeroDTO): IExternalHero => ({
	externalId: dto.external_id,
	name: dto.full_name,
	fullName: dto.full_name,
	publisher: dto.publisher,
});

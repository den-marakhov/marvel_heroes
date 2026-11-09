import { z } from 'zod';

export const heroDtoScheme = z.object({
	hero_id: z.uuid(),
	name: z.string(),
	description: z.string(),
	full_name: z.string().nullable(),
	publisher: z.string().nullable(),
	uploaded_img_url: z.string().nullable(),
	created_at: z.iso.datetime({ offset: true }),
	updated_at: z.iso.datetime({ offset: true }),
});

export const heroDtoListScheme = z.array(heroDtoScheme);
export type HeroDTO = z.infer<typeof heroDtoScheme>;

export const externalDTOHeroScheme = z.object({
	external_id: z.number(),
	name: z.string(),
	full_name: z.string(),
	publisher: z.string(),
});

export const externalHeroDtoListScheme = z.array(externalDTOHeroScheme);
export type ExternalHeroDTO = z.infer<typeof externalDTOHeroScheme>;

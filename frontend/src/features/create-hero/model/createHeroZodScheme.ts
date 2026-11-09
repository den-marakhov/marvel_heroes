import z from 'zod';

export const createHeroZodScheme = z.object({
	name: z.string().min(1, 'Hero name is required'),
	description: z
		.string()
		.min(10, 'Description should be at least 10 characters')
		.max(500, 'Description must not exceed 500 characters'),
});

export type CreateHeroFormData = z.infer<typeof createHeroZodScheme>;

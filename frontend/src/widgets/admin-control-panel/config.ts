export const SCREENS = {
	TABLE: 'table',
	CREATE_HERO: 'create-hero',
	ENRICH_HERO: 'enrich',
	UPLOAD_IMG: 'upload-image',
} as const;

export const STEPS_SCREEN = {
	MANUAL: 'manual',
	ENRICH_HERO_STEP: 'enrich',
	UPLOAD_IMAGE_STEP: 'upload',
} as const;

export interface IStepsConfig {
	key: 'manual' | 'enrich' | 'upload';
	label: string;
}

export const createHeroSteps: IStepsConfig[] = [
	{
		key: 'manual',
		label: 'Create hero',
	},
	{
		key: 'enrich',
		label: 'Fetch hero additional info',
	},
	{ key: 'upload', label: 'Upload image' },
];

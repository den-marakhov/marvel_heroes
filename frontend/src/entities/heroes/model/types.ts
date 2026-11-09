export interface IHero {
	heroId: string;
	name: string;
	description: string;
	fullName?: string;
	publisher?: string;
	uploadedImgUrl?: string;
	createdAt: string;
	updatedAt: string;
}

export interface IExternalHero {
	externalId: number;
	name: string;
	fullName: string;
	publisher: string;
}

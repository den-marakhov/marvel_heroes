import type { IHero } from '@/entities/heroes';
import { create } from 'zustand';
import { SCREENS } from '../config';

export type Screen = (typeof SCREENS)[keyof typeof SCREENS];

interface IAdminControlPanelNavStore {
	screen: Screen;
	activeHero: IHero | null;
	openCreateHero: () => void;
	openUploadImage: (hero: IHero) => void;
	openEnrichHero: (hero: IHero) => void;
	backToTable: () => void;
}

export const useAdminPanelNavStore = create<IAdminControlPanelNavStore>(
	set => ({
		screen: SCREENS.TABLE,
		activeHero: null,
		openUploadImage: hero =>
			set({ screen: SCREENS.UPLOAD_IMG, activeHero: hero }),
		openEnrichHero: hero =>
			set({ screen: SCREENS.ENRICH_HERO, activeHero: hero }),
		openCreateHero: () => set({ screen: SCREENS.CREATE_HERO, activeHero: null }),
		backToTable: () => set({ screen: SCREENS.TABLE, activeHero: null }),
	}),
);

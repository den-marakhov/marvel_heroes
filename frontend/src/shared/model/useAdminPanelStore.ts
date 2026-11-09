import { create } from 'zustand';

interface AdminPanelStore {
	isOpen: boolean;
	open: () => void;
	close: () => void;
}

export const useAdminPanelStore = create<AdminPanelStore>(set => ({
	isOpen: false,
	open: () => set({ isOpen: true }),
	close: () => set({ isOpen: false }),
}));

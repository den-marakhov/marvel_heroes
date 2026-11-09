import { useAdminPanelStore } from '@/shared/model/useAdminPanelStore';
import Modal from '@/shared/ui/modal';

import { UploadImage } from '@/features/upload-image';
import CreateHeroWizard from './create-hero-wizard';
import EnrichHeroScreen from './enrich-hero-screen';

import Button from '@/shared/ui/button';
import { SCREENS } from '../config';
import { getScreenMeta } from '../lib/getScreenMeta';
import { useAdminPanelNavStore } from '../model/useAdminPanelNavStore';
import './AdminControlPanel.scss';
import { HeroViewTable } from './hero-view-table';

const AdminControlPanel = () => {
	const isOpen = useAdminPanelStore(state => state.isOpen);
	const closeModal = useAdminPanelStore(state => state.close);

	const screen = useAdminPanelNavStore(state => state.screen);
	const activeHero = useAdminPanelNavStore(state => state.activeHero);
	const openCreateHeroScreen = useAdminPanelNavStore(
		state => state.openCreateHero,
	);
	const backToTable = useAdminPanelNavStore(state => state.backToTable);

	const { title, description } = getScreenMeta(screen, activeHero);

	const handleCloseModal = () => {
		closeModal();
		backToTable();
	};

	return (
		<Modal
			isOpen={isOpen}
			onClose={handleCloseModal}
			title={title}
			description={description}
			actions={
				screen === SCREENS.TABLE && (
					<Button
						key={'create-hero-button'}
						label='Create hero'
						onClick={openCreateHeroScreen}
					/>
				)
			}
		>
			{screen === SCREENS.TABLE && (
				<HeroViewTable />
			)}
			{screen === SCREENS.UPLOAD_IMG && activeHero && (
				<UploadImage
					heroId={activeHero.heroId}
					onUploaded={backToTable}
					onCancel={backToTable}
				/>
			)}
			{screen === SCREENS.ENRICH_HERO && activeHero && (
				<EnrichHeroScreen
					hero={activeHero}
					onEnriched={backToTable}
					onNotFound={backToTable}
				/>
			)}
			{screen === SCREENS.CREATE_HERO && (
				<CreateHeroWizard onCreateHero={backToTable} />
			)}
		</Modal>
	);
};

export default AdminControlPanel;

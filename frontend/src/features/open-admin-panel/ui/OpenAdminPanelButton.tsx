import { useAdminPanelStore } from '@/shared/model/useAdminPanelStore';
import Button from '@/shared/ui/button';

const OpenAdminPanelButton = () => {
	const handleOpen = useAdminPanelStore(state => state.open);

	return <Button mode='skewed' label='Admin panel' onClick={handleOpen} />;
};

export default OpenAdminPanelButton;

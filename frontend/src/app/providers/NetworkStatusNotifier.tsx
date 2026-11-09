import { onlineManager } from '@tanstack/react-query';
import { useEffect } from 'react';
import { toast } from 'sonner';

const OFFLINE_TOAST_ID = 'network-offline';

const NetworkStatusNotifier = () => {
	useEffect(() => {
		return onlineManager.subscribe(isOnline => {
			if (isOnline) {
				toast.dismiss(OFFLINE_TOAST_ID);
				toast.success('Back online');
				return;
			}
			toast.error('You are offline', {
				id: OFFLINE_TOAST_ID,
				duration: Infinity,
			});
		});
	}, []);

	return null;
};

export default NetworkStatusNotifier;

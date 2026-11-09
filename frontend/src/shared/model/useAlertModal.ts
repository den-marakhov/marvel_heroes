import { useState } from 'react';

interface UseAlertModalOptions {
	isInProgress?: boolean;
	onClose?: () => void;
}

export const useAlertModal = (options: UseAlertModalOptions = {}) => {
	const { isInProgress = false, onClose } = options;
	const [isOpen, setIsOpen] = useState(false);

	const onOpenChange = (open: boolean) => {
		if (isInProgress) return;

		setIsOpen(open);
		if (!open) onClose?.();
	};

	const open = () => onOpenChange(true);

	const close = () => {
		setIsOpen(false);
		onClose?.();
	};

	return { isOpen, onOpenChange, open, close };
};

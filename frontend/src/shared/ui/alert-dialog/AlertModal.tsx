import * as AlertDialog from '@radix-ui/react-alert-dialog';
import type { MouseEvent, ReactNode } from 'react';
import Button from '../button';
import './AlertModal.scss';

interface IAlertModalProps {
	triggerDialogComponent: ReactNode;
	title: string;
	description?: string;
	cancelActionLabel: string;
	confirmActionLabel: string;
	onConfirm: () => void;
	isConfirming?: boolean;
	children?: ReactNode;
	isOpen?: boolean;
	onOpenChange?: (open: boolean) => void;
}

const AlertModal = (props: IAlertModalProps) => {
	const {
		triggerDialogComponent,
		title,
		description,
		cancelActionLabel,
		confirmActionLabel,
		onConfirm,
		isConfirming = false,
		children,
		isOpen,
		onOpenChange,
	} = props;

	const isControlled = isOpen !== undefined;

	const handleConfirm = (event: MouseEvent<HTMLButtonElement>) => {
		if (isControlled) event.preventDefault();
		onConfirm();
	};

	return (
		<AlertDialog.Root open={isOpen} onOpenChange={onOpenChange}>
			<AlertDialog.Trigger asChild>
				{triggerDialogComponent}
			</AlertDialog.Trigger>

			<AlertDialog.Portal>
				<AlertDialog.Content className='alert-dialog__content'>
					<div className='alert-dialog__header'>
						<AlertDialog.Title className='alert-dialog__title h2'>
							{title}
						</AlertDialog.Title>
						{description && (
							<AlertDialog.Description className='alert-dialog__description'>
								{description}
							</AlertDialog.Description>
						)}
					</div>
					{children && (
						<div className='alert-dialog__body'>{children}</div>
					)}
					<div className='alert-dialog__actions'>
						<AlertDialog.Cancel asChild>
							<Button
								mode='grey-4'
								label={cancelActionLabel}
								isDisabled={isConfirming}
							/>
						</AlertDialog.Cancel>
						<AlertDialog.Action asChild>
							<Button
								label={confirmActionLabel}
								onClick={handleConfirm}
								isDisabled={isConfirming}
							/>
						</AlertDialog.Action>
					</div>
				</AlertDialog.Content>
			</AlertDialog.Portal>
		</AlertDialog.Root>
	);
};

export default AlertModal;

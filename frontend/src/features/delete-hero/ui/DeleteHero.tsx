import { useDeleteHero } from '@/entities/heroes';
import type { IHero } from '@/entities/heroes/model/types';
import { toApiError } from '@/shared/api';
import { useAlertModal } from '@/shared/model/useAlertModal';
import AlertModal from '@/shared/ui/alert-dialog';
import Button from '@/shared/ui/button';
import Icon from '@/shared/ui/icon';
import Loader from '@/shared/ui/loader';

import { Trash2 } from 'lucide-react';

interface IDeleteHeroProps {
	hero: IHero;
}

const DeleteHero = ({ hero }: IDeleteHeroProps) => {
	const { heroId, name } = hero;
	const { deleteHero, isDeleting, isError, error, reset } = useDeleteHero();
	const { isOpen, onOpenChange, close } = useAlertModal({
		isInProgress: isDeleting,
		onClose: reset,
	});

	return (
		<AlertModal
			isOpen={isOpen}
			onOpenChange={onOpenChange}
			triggerDialogComponent={
				<Button
					isLabelHidden
					label='delete hero'
					className='button--transparent'
					isDisabled={isDeleting}
					icon={<Icon className='button__icon' icon={<Trash2 />} />}
				/>
			}
			title={isError ? 'Could not delete hero' : 'Confirm your action'}
			description={
				isError
					? toApiError(error).message
					: `Are you sure you want to delete ${name}?`
			}
			confirmActionLabel={isError ? 'Try again' : 'Delete'}
			cancelActionLabel='Cancel'
			onConfirm={() => deleteHero(heroId, { onSuccess: close })}
			isConfirming={isDeleting}
		>
			{isDeleting && <Loader label='Deleting hero' />}
		</AlertModal>
	);
};

export default DeleteHero;

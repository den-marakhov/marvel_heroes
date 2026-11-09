import { useEnrichHero, type IHero } from '@/entities/heroes';
import { toApiError } from '@/shared/api';
import { useAlertModal } from '@/shared/model/useAlertModal';
import AlertModal from '@/shared/ui/alert-dialog';
import Button from '@/shared/ui/button';
import Loader from '@/shared/ui/loader';

interface IEnrichHeroButtonProps {
	heroId: IHero['heroId'];
	externalId: number;
	onSuccess?: () => void;
}

const EnrichHeroButton = ({
	heroId,
	externalId,
	onSuccess,
}: IEnrichHeroButtonProps) => {
	const { enrichHero, isPending, isError, error, reset } = useEnrichHero();
	const { isOpen, onOpenChange, close } = useAlertModal({
		isInProgress: isPending,
		onClose: reset,
	});

	const handleConfirm = () => {
		enrichHero(
			{ heroId, externalId },
			{
				onSuccess: () => {
					close();
					onSuccess?.();
				},
			},
		);
	};

	return (
		<AlertModal
			isOpen={isOpen}
			onOpenChange={onOpenChange}
			triggerDialogComponent={<Button label='Select' isDisabled={isPending} />}
			title={isError ? 'Could not enrich hero' : 'Please confirm your choice'}
			description={
				isError
					? toApiError(error).message
					: 'Selected match data will be applied to this hero.'
			}
			confirmActionLabel={isError ? 'Try again' : 'Confirm'}
			cancelActionLabel='Cancel'
			onConfirm={handleConfirm}
			isConfirming={isPending}
		>
			{isPending && <Loader label='Enriching hero' />}
		</AlertModal>
	);
};

export default EnrichHeroButton;

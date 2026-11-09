import type { IHero } from '@/entities/heroes';
import { toApiError } from '@/shared/api';
import Button from '@/shared/ui/button';
import Loader from '@/shared/ui/loader';
import StateMessage from '@/shared/ui/state-message';
import { useAvailableHeroNames } from '../model';
import ManualCreateHeroForm from './manual-create-hero-form';
import './ManualCreate.scss';

interface IManualCreateProps {
	onCreated: (hero: IHero) => void;
}

const ManualCreate = (props: IManualCreateProps) => {
	const { onCreated } = props;

	const {
		availableNames,
		hasAvailableNames,
		isPending,
		isError,
		error,
		refetch,
	} = useAvailableHeroNames();

	const renderContent = () => {
		if (isPending) return <Loader label='Loading hero names' />;

		if (isError) {
			return (
				<StateMessage
					variant='error'
					title='Failed to load hero names'
					description={toApiError(error).message}
					action={<Button label='Try again' onClick={() => refetch()} />}
				/>
			);
		}

		if (!hasAvailableNames) {
			return <StateMessage title='All available heroes are already created' />;
		}

		return (
			<ManualCreateHeroForm
				availableNames={availableNames}
				onCreated={onCreated}
			/>
		);
	};

	return (
		<div className='manual-create'>
			<h3 className='manual-create__title'>Create Hero</h3>
			{renderContent()}
		</div>
	);
};

export default ManualCreate;

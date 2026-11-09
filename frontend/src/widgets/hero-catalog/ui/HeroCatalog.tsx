import { HeroCard, HeroCardSkeleton, useHeroes } from '@/entities/heroes';
import { OpenAdminPanelButton } from '@/features/open-admin-panel';
import { toApiError } from '@/shared/api';
import marvelLogo from '@/shared/assets/images/marvel-logo.svg';
import Button from '@/shared/ui/button';
import { Grid } from '@/shared/ui/layouts';
import StateMessage from '@/shared/ui/state-message';

const GRID_COLUMNS = 6;
const SKELETON_COUNT = GRID_COLUMNS * 2;

const HeroCatalog = () => {
	const { isPending, isPaused, isError, data, error, refetch } = useHeroes();

	if (isPending && isPaused) {
		return (
			<StateMessage
				variant='error'
				title='You are offline'
				description='Heroes will load automatically when the connection is back.'
			/>
		);
	}

	if (isPending) {
		return (
			<div aria-busy='true' aria-label='Loading heroes'>
				<Grid columns={GRID_COLUMNS}>
					{Array.from({ length: SKELETON_COUNT }, (_, index) => (
						<HeroCardSkeleton key={index} />
					))}
				</Grid>
			</div>
		);
	}

	if (isError && !data) {
		return (
			<StateMessage
				variant='error'
				title='Failed to load heroes'
				description={toApiError(error).message}
				action={<Button label='Try again' onClick={() => refetch()} />}
			/>
		);
	}

	if (!data?.length) {
		return (
			<StateMessage
				imgSrc={marvelLogo}
				title='Oops, there are no heroes yet'
				description='Open the admin panel to create the first one.'
				action={<OpenAdminPanelButton />}
			/>
		);
	}

	return (
		<Grid columns={GRID_COLUMNS}>
			{data.map(({ heroId, uploadedImgUrl, ...hero }) => (
				<HeroCard key={heroId} imgSrc={uploadedImgUrl} {...hero} />
			))}
		</Grid>
	);
};

export default HeroCatalog;

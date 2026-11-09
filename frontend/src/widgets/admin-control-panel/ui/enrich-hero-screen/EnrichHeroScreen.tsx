import {
	ExternalHeroCard,
	ExternalHeroCardSkeleton,
	useSearchExternalHeroes,
	type IHero,
} from '@/entities/heroes';
import { EnrichHeroButton } from '@/features/enrich-hero';
import { toApiError } from '@/shared/api';
import Button from '@/shared/ui/button';
import { Grid } from '@/shared/ui/layouts';
import StateMessage from '@/shared/ui/state-message';

const GRID_COLUMNS = 2;
const SKELETON_COUNT = 3;

interface IEnrichHeroScreenProps {
	hero: IHero;
	onEnriched?: () => void;
	onNotFound?: () => void;
}

const EnrichHeroScreen = ({
	hero,
	onEnriched,
	onNotFound,
}: IEnrichHeroScreenProps) => {
	const { externalHeroes, isPending, isPaused, isError, error, refetch } =
		useSearchExternalHeroes(hero.name);

	if (isPending && isPaused) {
		return (
			<StateMessage
				variant='error'
				title='You are offline'
				description='Matches will load automatically when the connection is back.'
			/>
		);
	}

	if (isPending) {
		return (
			<div aria-busy='true' aria-label='Loading matching heroes'>
				<Grid columns={GRID_COLUMNS}>
					{Array.from({ length: SKELETON_COUNT }, (_, index) => (
						<ExternalHeroCardSkeleton key={index} />
					))}
				</Grid>
			</div>
		);
	}

	if (isError && !externalHeroes) {
		return (
			<StateMessage
				variant='error'
				title='Failed to find matching heroes'
				description={toApiError(error).message}
				action={<Button label='Try again' onClick={() => refetch()} />}
			/>
		);
	}

	if (!externalHeroes?.length) {
		return (
			<StateMessage
				variant='error'
				title='No matching heroes found'
				description='There are no SuperHero API matches for this name.'
				action={
					onNotFound && (
						<Button label='Back' mode='grey-4' onClick={onNotFound} />
					)
				}
			/>
		);
	}

	return (
		<Grid columns={GRID_COLUMNS}>
			{externalHeroes.map(({ externalId, ...externalHero }) => (
				<ExternalHeroCard
					key={externalId}
					{...externalHero}
					actions={
						<EnrichHeroButton
							heroId={hero.heroId}
							externalId={externalId}
							onSuccess={onEnriched}
						/>
					}
				/>
			))}
		</Grid>
	);
};

export default EnrichHeroScreen;

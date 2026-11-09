import { useHeroes } from '@/entities/heroes';
import { DeleteHero } from '@/features/delete-hero';
import { toApiError } from '@/shared/api';
import Button from '@/shared/ui/button';
import StateMessage from '@/shared/ui/state-message';
import { AnimatePresence, motion } from 'framer-motion';
import { useAdminPanelNavStore } from '../../../model/useAdminPanelNavStore';
import AdminCellEnrich from './admin-cell-enrich';
import AdminCellImage from './admin-cell-image';
import { heroViewListColumns } from './columns';
import HeroViewTableSkeletonRow from './HeroViewTableSkeletonRow';
import './HeroViewTable.scss';

const SKELETON_ROWS = 5;

const HeroViewTable = () => {
	const openUploadImageScreen = useAdminPanelNavStore(
		state => state.openUploadImage,
	);
	const openEnrichHeroScreen = useAdminPanelNavStore(
		state => state.openEnrichHero,
	);
	const { isPending, isPaused, isError, error, data, refetch } = useHeroes();

	if (isPending && isPaused) {
		return (
			<StateMessage
				variant='error'
				title='You are offline'
				description='Heroes will load automatically when the connection is back.'
			/>
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

	if (!isPending && !data?.length) {
		return (
			<StateMessage
				title='No heroes yet'
				description='Create the first hero to see it in this table.'
			/>
		);
	}

	return (
		<div
			className='hero-admin'
			aria-busy={isPending}
			aria-label={isPending ? 'Loading heroes' : undefined}
		>
			<div className='hero-admin__wrapper'>
				<table>
					<thead>
						<tr>
							{heroViewListColumns.map(({ key, columnName }) => (
								<th key={key}>{columnName}</th>
							))}
						</tr>
					</thead>
					<tbody>
						{isPending ? (
							Array.from({ length: SKELETON_ROWS }, (_, index) => (
								<HeroViewTableSkeletonRow key={index} />
							))
						) : (
							<AnimatePresence>
								{data?.map(hero => (
									<motion.tr
										key={hero.heroId}
										layout
										initial={{ opacity: 0 }}
										animate={{ opacity: 1 }}
										exit={{ opacity: 0, height: 0 }}
										transition={{ duration: 0.25 }}
									>
										{heroViewListColumns.map(({ key, cell }) => (
											<td key={key}>
												{cell(hero, {
													uploadImage: (
														<AdminCellImage
															imgSrc={hero.uploadedImgUrl}
															onClick={() =>
																openUploadImageScreen(hero)
															}
														/>
													),
													deleteHero: <DeleteHero hero={hero} />,
													enrichHero: (
														<AdminCellEnrich
															onClick={() =>
																openEnrichHeroScreen(hero)
															}
														/>
													),
												})}
											</td>
										))}
									</motion.tr>
								))}
							</AnimatePresence>
						)}
					</tbody>
				</table>
			</div>
		</div>
	);
};

export default HeroViewTable;

import { Grid } from '@/shared/ui/layouts';
import type { IHero } from '../../types';
import HeroCard from '../HeroCard/HeroCard';

const HeroCardList = (props: { heroes: IHero[] }) => {
	const { heroes } = props;

	return (
		<Grid columns={6}>
			{heroes.map(({ hero_id, uploaded_img_url, full_name, ...hero }) => (
				<HeroCard
					key={hero_id}
					imgSrc={uploaded_img_url}
					fullName={full_name}
					{...hero}
				/>
			))}
		</Grid>
	);
};

export default HeroCardList;

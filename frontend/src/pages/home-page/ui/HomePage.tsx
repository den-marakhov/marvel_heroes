import bannerImg from '@/shared/assets/images/marvel_characters_banner.jpg';
import Banner from '@/shared/ui/banner';
import { Section } from '@/shared/ui/layouts';
import { AdminControlPanel, HeroCatalog } from '@/widgets';

const HomePage = () => {
	return (
		<>
			<Banner
				title='Marvel characters'
				titleId='marvel-characters-title'
				description='All Marvel characters'
				imgSrc={bannerImg}
			/>
			<Section titleId='featured-characters-title' title='Featured characters'>
				<HeroCatalog />
			</Section>
			<AdminControlPanel />
		</>
	);
};

export default HomePage;

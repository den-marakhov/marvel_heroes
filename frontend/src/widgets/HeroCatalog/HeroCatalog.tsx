import { HeroCardList, useHeroes } from '@/entities/heroes';

const HeroCatalog = () => {
	const { hasHeroes, isLoading, isError, data } = useHeroes();
	if (isLoading) return <p>Loading...</p>;
	if (isError) return <p>Error</p>;
	if (!hasHeroes) return <p>No heroes</p>;

	return <HeroCardList heroes={data!} />;
};

export default HeroCatalog;

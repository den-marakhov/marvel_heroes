import Skeleton from '@/shared/ui/skeleton';
import './HeroCard.scss';

const HeroCardSkeleton = () => {
	return (
		<div className='hero-card hero-card--skeleton' aria-hidden='true'>
			<Skeleton className='hero-card__img-wrapper' borderRadius={0} />
			<div className='hero-card__info'>
				<Skeleton height={24} width='70%' />
				<Skeleton count={2} />
				<Skeleton height={12} width='40%' />
			</div>
		</div>
	);
};

export default HeroCardSkeleton;

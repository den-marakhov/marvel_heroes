import Skeleton from '@/shared/ui/skeleton';
import './ExternalHeroCard.scss';

const ExternalHeroCardSkeleton = () => {
	return (
		<div
			className='external-hero-card external-hero-card--skeleton'
			aria-hidden='true'
		>
			<div className='external-hero-card__header'>
				<Skeleton height={22} width='60%' />
			</div>
			<div className='external-hero-card__body'>
				<Skeleton height={16} width='80%' />
				<Skeleton height={16} width='55%' />
			</div>
			<div className='external-hero-card__actions'>
				<Skeleton height={36} width={88} />
			</div>
		</div>
	);
};

export default ExternalHeroCardSkeleton;

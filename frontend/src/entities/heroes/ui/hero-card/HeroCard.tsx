import marvelLogo from '@/shared/assets/images/marvel-logo.svg';
import classNames from 'classnames';
import './HeroCard.scss';

interface IHeroProps {
	className?: string;
	name: string;
	fullName?: string;
	imgSrc?: string;
	description?: string;
}

const HeroCard = (props: IHeroProps) => {
	const { className, name, fullName, imgSrc, description } = props;

	return (
		<div className={classNames(className, 'hero-card')}>
			{imgSrc ? (
				<div className='hero-card__img-wrapper'>
					<img
						className='hero-card__image'
						loading='lazy'
						src={imgSrc}
						alt='hero-image'
					/>
				</div>
			) : (
				<div className='hero-card__image-placeholder-wrapper'>
					<img
						className='hero-card__image-placeholder-logo'
						src={marvelLogo}
						alt='marvel logo placeholder'
					/>
				</div>
			)}
			<div className='hero-card__body'>
				<div className='hero-card__info'>
					<h3 className='hero-card__name'>{name}</h3>
					{description && (
						<div className='hero-card__description'>
							<p>{description}</p>
						</div>
					)}
				</div>
				{fullName && <p className='hero-card__full-name'>{fullName}</p>}
			</div>
		</div>
	);
};

export default HeroCard;

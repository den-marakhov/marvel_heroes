import './ExternalHeroCard.scss';

interface IExternalHeroCardProps {
	name: string;
	fullName: string;
	publisher: string;
	actions?: React.ReactNode;
}

const ExternalHeroCard = (props: IExternalHeroCardProps) => {
	const { name, fullName, publisher, actions } = props;

	return (
		<div className='external-hero-card'>
			<div className='external-hero-card__header'>
				<h4 className='external-hero-card__title'>{name}</h4>
			</div>
			<div className='external-hero-card__body'>
				<dl className='external-hero-card__list-container'>
					<div className='external-hero-card__row'>
						<dt className='external-hero-card__label'>Full name:</dt>
						<dd className='external-hero-card__description'>{fullName}</dd>
					</div>
					<div className='external-hero-card__row'>
						<dt className='external-hero-card__label'>Publisher:</dt>
						<dd className='external-hero-card__description'>{publisher}</dd>
					</div>
				</dl>
			</div>
			{actions && (
				<div className='external-hero-card__actions'>
					{actions}
				</div>
			)}
		</div>
	);
};

export default ExternalHeroCard;

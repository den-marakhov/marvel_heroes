import './Banner.scss';

interface IBannerProps {
	imgSrc: string;
	title: string;
	titleId: string;
	description: string;
}

const Banner = (props: IBannerProps) => {
	const { imgSrc, title, titleId, description } = props;

	return (
		<section className='banner' aria-labelledby={titleId}>
			<img className='banner__image' src={imgSrc} alt='hero_banner' />
			<div className='banner__inner'>
				<div className='banner__body'>
					<h1 id={titleId} className='banner__title'>
						{title}
					</h1>
					<div className='banner__description'>
						<p>{description}</p>
					</div>
				</div>
			</div>
		</section>
	);
};

export default Banner;

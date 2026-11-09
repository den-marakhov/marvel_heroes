import Accordion from '@/shared/ui/accordion';
import './ImageTermsAccordion.scss';

const rules = [
	'Format: PNG, JPEG, WEBP',
	'Resolution: up to 900×900px (larger images are scaled down)',
	'File size: up to 5 MB',
	'Orientation: portrait works best for hero cards',
	'The image is converted to WEBP and cropped to fit the card',
];

const ImageTermsAccordion = () => {
	return (
		<Accordion
			title='What makes a good hero photo'
			value='hero photo requirements'
		>
			<ul className='image-terms__list'>
				{rules.map((rule, index) => (
					<li key={`rule-${index}`} className='image-terms__item'>
						{rule}
					</li>
				))}
			</ul>
		</Accordion>
	);
};

export default ImageTermsAccordion;

import classNames from 'classnames';
import type { ReactNode } from 'react';
import './Section.scss';

interface ISectionProps {
	className?: string;
	title: string;
	titleId: string;
	children: ReactNode;
}

const Section = (props: ISectionProps) => {
	const { className, title, titleId, children } = props;
	return (
		<section
			className={classNames(className, 'section container')}
			aria-labelledby={titleId}
		>
			<div className='section__header'>
				<h2 id={titleId} className='section__title'>
					{title}
				</h2>
			</div>
			<div className='section__body'>{children}</div>
		</section>
	);
};

export default Section;

import classNames from 'classnames';
import type { ReactNode } from 'react';
import './StateMessage.scss';

interface IStateMessageProps {
	className?: string;
	variant?: 'empty' | 'error';
	title: string;
	description?: string;
	imgSrc?: string;
	action?: ReactNode;
}

const StateMessage = (props: IStateMessageProps) => {
	const {
		className,
		variant = 'empty',
		title,
		description,
		imgSrc,
		action,
	} = props;

	const isError = variant === 'error';

	return (
		<div
			className={classNames(className, 'state-message', {
				[`state-message--${variant}`]: variant,
			})}
			role={isError ? 'alert' : 'status'}
		>
			{imgSrc && (
				<img className='state-message__image' src={imgSrc} alt='' />
			)}
			<h3 className='state-message__title h3'>{title}</h3>
			{description && (
				<p className='state-message__description'>{description}</p>
			)}
			{action && <div className='state-message__action'>{action}</div>}
		</div>
	);
};

export default StateMessage;

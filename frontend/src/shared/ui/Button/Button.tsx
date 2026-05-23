import classNames from 'classnames';
import type { MouseEvent } from 'react';
import './Button.scss';

interface IButtonProps {
	className?: string;
	type?: 'button' | 'submit';
	label: string;
	onClick: (event: MouseEvent<HTMLButtonElement>) => void;
	isDisabled?: boolean;
}

const Button = (props: IButtonProps) => {
	const {
		className,
		label,
		onClick,
		isDisabled = false,
		type = 'button',
	} = props;

	return (
		<button
			className={classNames('button', className)}
			type={type}
			onClick={onClick}
			disabled={isDisabled}
		>
			<span className='button__label'>{label}</span>
		</button>
	);
};

export default Button;

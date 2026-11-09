import classNames from 'classnames';
import type { ButtonHTMLAttributes, ReactNode, Ref } from 'react';
import './Button.scss';

interface IButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
	className?: string;
	ref?: Ref<HTMLButtonElement>;
	label: string;
	isLabelHidden?: boolean;
	icon?: ReactNode;
	mode?: '' | 'skewed' | 'grey-4';
	isDisabled?: boolean;
}

const Button = (props: IButtonProps) => {
	const {
		className,
		ref,
		label,
		isLabelHidden = false,
		icon,
		onClick,
		isDisabled = false,
		type = 'button',
		mode = '',
		...extrProps
	} = props;

	const title = isLabelHidden ? label : undefined;

	return (
		<button
			className={classNames(className, 'button', {
				[`button--${mode}`]: mode,
			})}
			ref={ref}
			type={type}
			title={title}
			aria-label={title}
			onClick={onClick}
			disabled={isDisabled}
			{...extrProps}
		>
			{icon && icon}
			{!isLabelHidden && <span className='button__label'>{label}</span>}
		</button>
	);
};

export default Button;

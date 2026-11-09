import classNames from 'classnames';
import type { ReactNode } from 'react';
import './Icon.scss';

interface IconProps {
	className?: string;
	icon: ReactNode;
	ariaLabel?: string;
}

const Icon = (props: IconProps) => {
	const { className, icon, ariaLabel } = props;

	return (
		<span className={classNames(className, 'icon')} aria-label={ariaLabel}>
			{icon}
		</span>
	);
};

export default Icon;

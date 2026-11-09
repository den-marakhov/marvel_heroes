import classNames from 'classnames';
import type { CSSProperties } from 'react';
import './Loader.scss';

interface ILoaderProps {
	className?: string;
	size?: number;
	label?: string;
}

const Loader = (props: ILoaderProps) => {
	const { className, size, label = 'Loading' } = props;

	const style = size
		? ({ '--loaderSize': `${size}px` } as CSSProperties)
		: undefined;

	return (
		<div
			className={classNames(className, 'loader')}
			style={style}
			role='status'
		>
			<span className='loader__arc loader__arc--a' aria-hidden='true' />
			<span className='loader__arc loader__arc--b' aria-hidden='true' />
			<span className='visually-hidden'>{label}</span>
		</div>
	);
};

export default Loader;

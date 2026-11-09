import classNames from 'classnames';
import { Children, type ReactNode } from 'react';
import './Grid.scss';

interface IGridProps {
	columns?: number;
	children: ReactNode;
}

const Grid = (props: IGridProps) => {
	const { columns = 1, children } = props;

	return (
		<ul
			className={classNames('grid', {
				[`grid--${columns}`]: columns > 1,
			})}
		>
			{Children.map(children, child => (
				<li className='grid__item'>{child}</li>
			))}
		</ul>
	);
};

export default Grid;

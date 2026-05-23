import classNames from 'classnames';
import type { ReactElement } from 'react';
import './Grid.scss';

interface IGridProps {
	columns?: number;
	children: ReactElement[];
}

const Grid = (props: IGridProps) => {
	const { columns = 1, children } = props;

	return (
		<ul
			className={classNames('grid', {
				[`grid--${columns}`]: columns > 1,
			})}
		>
			{children?.map((child, index) => {
				return (
					<li key={index} className='grid__item'>
						{child}
					</li>
				);
			})}
		</ul>
	);
};

export default Grid;

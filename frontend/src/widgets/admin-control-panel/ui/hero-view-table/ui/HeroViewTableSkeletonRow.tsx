import Skeleton from '@/shared/ui/skeleton';

const HeroViewTableSkeletonRow = () => {
	return (
		<tr aria-hidden='true'>
			<td>
				<Skeleton className='hero-admin__skeleton-image' borderRadius={4} />
			</td>
			<td>
				<Skeleton height={16} width='70%' />
			</td>
			<td>
				<Skeleton height={16} width='55%' />
			</td>
			<td>
				<Skeleton height={20} width={72} />
			</td>
			<td>
				<Skeleton height={16} width='80%' />
			</td>
			<td>
				<Skeleton circle height={24} width={24} />
			</td>
		</tr>
	);
};

export default HeroViewTableSkeletonRow;

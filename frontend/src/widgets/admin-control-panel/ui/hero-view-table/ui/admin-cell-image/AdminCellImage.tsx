import imgPlaceholder from '@/shared/assets/images/admin_placeholder.jpg';
import Icon from '@/shared/ui/icon';
import { Pencil } from 'lucide-react';
import './AdminCellImage.scss';

interface IAdminCellImageProps {
	imgSrc?: string;
	onClick?: () => void;
}
const AdminCellImage = (props: IAdminCellImageProps) => {
	const { imgSrc, onClick } = props;
	return (
		<button
			type='button'
			aria-label='edit hero image'
			className='admin-cell-image'
			onClick={onClick}
		>
			{imgSrc ? (
				<img
					className='admin-cell-image__image'
					src={imgSrc}
					alt='hero-cell-image'
				/>
			) : (
				<img
					className='admin-cell-image__placeholder'
					src={imgPlaceholder}
					alt='hero-cell-placeholder'
				/>
			)}
			<div className='admin-cell-image__inner'>
				<Icon className='admin-cell-image__icon' icon={<Pencil />} />
			</div>
		</button>
	);
};

export default AdminCellImage;

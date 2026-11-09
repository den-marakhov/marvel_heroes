import './AdminCellEnrich.scss';

interface IAdminCellEnrich {
	onClick?: () => void;
}

const AdminCellEnrich = ({ onClick }: IAdminCellEnrich) => {
	return (
		<button className='admin-cell-enrich' type='button' onClick={onClick}>
			<span className='admin-cell-enrich__label'>Add information</span>
		</button>
	);
};

export default AdminCellEnrich;

import { OpenAdminPanelButton } from '@/features/open-admin-panel';
import { Outlet } from 'react-router';

const MainAppLayout = () => {
	return (
		<>
			<header
				style={{
					display: 'flex',
					justifyContent: 'space-between',
					padding: '20px 15px',
				}}
			>
				<span>Header</span>
				<OpenAdminPanelButton />
			</header>
			<main className='content'>
				<Outlet />
			</main>
			<footer>Footer</footer>
		</>
	);
};

export default MainAppLayout;

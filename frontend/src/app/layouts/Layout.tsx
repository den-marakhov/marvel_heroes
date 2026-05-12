import { Outlet } from 'react-router';

const Layout = () => {
	return (
		<>
			<header>Header</header>
			<main className='content'>
				<Outlet />
			</main>
			<footer>Footer</footer>
		</>
	);
};

export default Layout;

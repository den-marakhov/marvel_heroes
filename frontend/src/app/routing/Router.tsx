import { HomePage } from '@/pages/home-page';

import { createBrowserRouter, RouterProvider } from 'react-router';
import MainAppLayout from '../layouts';

const router = createBrowserRouter([
	{
		path: '/',
		Component: MainAppLayout,
		children: [{ index: true, Component: HomePage }],
	},
]);

const Router = () => <RouterProvider router={router} />;

export default Router;

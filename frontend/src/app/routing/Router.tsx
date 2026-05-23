import HomePage from '@/pages/HomePage';
import { Layout } from '@/shared/ui/layouts';
import { createBrowserRouter, RouterProvider } from 'react-router';

const router = createBrowserRouter([
	{
		path: '/',
		Component: Layout,
		children: [{ index: true, Component: HomePage }],
	},
]);

const Router = () => <RouterProvider router={router} />;

export default Router;

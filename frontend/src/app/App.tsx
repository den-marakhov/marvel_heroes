import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Router from './routing';
import './styles';

const queryClient = new QueryClient();

const App = () => {
	return (
		<QueryClientProvider client={queryClient}>
			<Router />
		</QueryClientProvider>
	);
};

export default App;

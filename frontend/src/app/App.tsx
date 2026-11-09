import { QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'sonner';
import { NetworkStatusNotifier, queryClient } from './providers';
import Router from './routing';
import './styles';

const App = () => {
	return (
		<QueryClientProvider client={queryClient}>
			<Router />
			<NetworkStatusNotifier />
			<Toaster position='bottom-right' richColors closeButton />
		</QueryClientProvider>
	);
};

export default App;

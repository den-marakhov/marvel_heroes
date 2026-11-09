import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useState } from 'react';

import { heroApi } from '../hero-api';
import { heroQueries } from './heroQueries';

interface IMutationFnProps {
	heroId: string;
	file: File;
}

export const useUploadImage = () => {
	const queryClient = useQueryClient();
	const [progress, setProgress] = useState(0);

	const { mutate, isPending, isError, error, reset } = useMutation({
		mutationFn: ({ heroId, file }: IMutationFnProps) =>
			heroApi.uploadImage(heroId, file, setProgress),
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: heroQueries.all() });
		},
		onSettled: () => setProgress(0),
		meta: { silent: true },
	});

	return {
		uploadImage: mutate,
		isUploading: isPending,
		progress,
		isError,
		error,
		reset,
	};
};

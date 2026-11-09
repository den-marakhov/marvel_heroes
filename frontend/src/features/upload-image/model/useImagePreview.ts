import { useEffect, useState } from 'react';

const useImagePreview = (file: File | null) => {
	const [preview, setPreview] = useState<string | null>(null);

	useEffect(() => {
		if (!file) {
			setPreview(null);
			return;
		}

		const blobUrl = URL.createObjectURL(file);
		setPreview(blobUrl);

		return () => {
			URL.revokeObjectURL(blobUrl);
		};
	}, [file]);

	return preview;
};

export default useImagePreview;

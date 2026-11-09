import { useCallback, useState } from 'react';
import { useDropzone, type Accept, type FileRejection } from 'react-dropzone';

interface IUseFileDropZoneOptions {
	accept: Accept;
	maxSize: number;
	disabled?: boolean;
}

const useFileDropZone = ({
	accept,
	maxSize,
	disabled,
}: IUseFileDropZoneOptions) => {
	const [file, setFile] = useState<File | null>(null);
	const [rejectionError, setRejectionError] = useState<string | null>(null);

	const onDrop = useCallback(
		(acceptFiles: File[], rejections: FileRejection[]) => {
			setRejectionError(null);

			if (rejections.length) {
				const code = rejections[0].errors[0]?.code;

				switch (code) {
					case 'file-too-large':
						setRejectionError('File size is too large. Max: 5MB');
						break;
					case 'file-invalid-type':
						setRejectionError('Only PNG, JPEG or WebP allowed.');
						break;
					default:
						setRejectionError('Invalid file.');
						break;
				}
				return;
			}

			if (acceptFiles[0]) setFile(acceptFiles[0]);
		},
		[],
	);

	const { getRootProps, getInputProps, isDragActive, open } = useDropzone({
		onDrop,
		accept,
		maxSize,
		disabled,
		multiple: false,
	});

	const reset = useCallback(() => {
		setFile(null);
		setRejectionError(null);
	}, []);

	return {
		file,
		getRootProps,
		getInputProps,
		isDragActive,
		rejectionError,
		reset,
		open,
	};
};

export default useFileDropZone;

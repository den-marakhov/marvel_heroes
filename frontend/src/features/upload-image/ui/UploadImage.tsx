import { useUploadImage } from '@/entities/heroes';
import { toApiError } from '@/shared/api';
import { useAlertModal } from '@/shared/model/useAlertModal';
import AlertModal from '@/shared/ui/alert-dialog';
import Button from '@/shared/ui/button';
import { ACCEPTED_IMAGE_TYPES, MAX_FILE_SIZE } from '../config';
import useFileDropZone from '../model/useFileDropZone';
import useImagePreview from '../model/useImagePreview';
import Dropzone from './dropzone';
import ImageTermsAccordion from './image-terms-accordion';
import PreviewImage from './preview-image';
import './UploadImage.scss';

interface IUploadImageProps {
	heroId: string;
	onUploaded?: () => void;
	onCancel?: () => void;
}

const UploadImage = ({ heroId, onUploaded, onCancel }: IUploadImageProps) => {
	const {
		uploadImage,
		isUploading,
		isError,
		error,
		progress,
		reset: resetUpload,
	} = useUploadImage();
	const {
		isOpen,
		onOpenChange,
		open: openAlert,
		close: closeAlert,
	} = useAlertModal({
		isInProgress: isUploading,
		onClose: resetUpload,
	});

	const { file, reset, getRootProps, getInputProps, open, rejectionError } =
		useFileDropZone({
			accept: ACCEPTED_IMAGE_TYPES,
			maxSize: MAX_FILE_SIZE,
			disabled: isUploading,
		});

	const previewSrc = useImagePreview(file);

	const handleConfirm = () => {
		if (!file) return;

		closeAlert();
		uploadImage(
			{ heroId, file },
			{
				onSuccess: () => {
					reset();
					onUploaded?.();
				},
				onError: openAlert,
			},
		);
	};

	return (
		<div className='upload-hero-image'>
			<div className='upload-hero-image__recommendations-banner'>
				<p>
					For best results, upload a portrait image. Photos are resized to fit
					900×900px and converted to WEBP. Wide images will be cropped to fit
					the card.
				</p>
			</div>
			<div className='upload-hero-image__body'>
				<div className='upload-hero-image__left-col'>
					<Dropzone
						rootProps={getRootProps}
						inputProps={getInputProps}
						isUploading={isUploading}
						open={open}
					/>
					<ImageTermsAccordion />
					{rejectionError && (
						<div className='upload-hero-image__error-block'>
							<p role='alert' className='upload-hero-image__error-text'>
								{rejectionError}
							</p>
						</div>
					)}
					<div className='upload-hero-image__actions'>
						{file && (
							<AlertModal
								isOpen={isOpen}
								onOpenChange={onOpenChange}
								triggerDialogComponent={
									<Button
										className='upload-hero-image__button'
										label='Upload'
										isDisabled={isUploading}
									/>
								}
								title={
									isError
										? 'Could not upload image'
										: 'Please confirm media uploading'
								}
								description={
									isError
										? toApiError(error).message
										: 'By pressing confirm button you will start uploading process for current media file. Are you sure about that?'
								}
								confirmActionLabel={isError ? 'Try again' : 'Confirm'}
								cancelActionLabel='Cancel'
								onConfirm={handleConfirm}
							/>
						)}
						{onCancel && (
							<Button
								className='upload-hero-image__button'
								mode='grey-4'
								label='Back'
								onClick={onCancel}
							/>
						)}
					</div>
				</div>
				<div className='upload-hero-image__right-col'>
					<PreviewImage
						progress={progress}
						isUploading={isUploading}
						previewSrc={previewSrc}
						reset={reset}
					/>
				</div>
			</div>
		</div>
	);
};

export default UploadImage;

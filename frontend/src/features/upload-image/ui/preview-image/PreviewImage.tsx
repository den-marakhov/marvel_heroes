import Button from '@/shared/ui/button';
import Icon from '@/shared/ui/icon';
import Loader from '@/shared/ui/loader';
import { Trash2 } from 'lucide-react';
import './PreviewImage.scss';

interface IPreviewImageProps {
	reset: () => void;
	previewSrc: string | null;
	progress: number;
	isUploading: boolean;
}

const PreviewImage = (props: IPreviewImageProps) => {
	const { reset, previewSrc, progress, isUploading } = props;

	return (
		<div className='preview-image'>
			<div className='preview-image__header'>
				<h3 className='preview-image__title'>Hero card picture preview</h3>
			</div>
			<div className='preview-image__body'>
				<div className='preview-image__preview-wrapper'>
					{previewSrc && (
						<>
							<img
								className='preview-image__image'
								src={previewSrc}
								alt='hero image preview'
							/>
							<Button
								className='preview-image__delete-button'
								label='delete preview image'
								isLabelHidden
								icon={<Icon icon={<Trash2 />} />}
								onClick={reset}
								isDisabled={isUploading}
							/>
							{isUploading && (
								<div className='preview-image__loader-overlay'>
									<Loader label='Uploading image' />
									{progress > 0 && (
										<p className='preview-image__loader-progress'>{progress}%</p>
									)}
								</div>
							)}
						</>
					)}
				</div>
			</div>
		</div>
	);
};
export default PreviewImage;

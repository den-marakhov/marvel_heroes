import Button from '@/shared/ui/button';
import Icon from '@/shared/ui/icon';
import { Paperclip } from 'lucide-react';
import type { DropzoneInputProps, DropzoneRootProps } from 'react-dropzone';
import './Dropzone.scss';

interface IDropzoneProps {
	inputProps: <T extends DropzoneInputProps>(props?: T) => T;
	rootProps: <T extends DropzoneRootProps>(props?: T) => T;
	isUploading: boolean;
	open: () => void;
}

const Dropzone = (props: IDropzoneProps) => {
	const { inputProps, rootProps, isUploading, open } = props;

	return (
		<div className='dropzone' {...rootProps()}>
			<input {...inputProps()} />
			<div className='dropzone__body'>
				<Button
					className='dropzone__choose-btn'
					onClick={event => {
						event.stopPropagation();
						open();
					}}
					mode='grey-4'
					label='choose image for uploading'
					isLabelHidden
					icon={<Icon icon={<Paperclip />} />}
					disabled={isUploading}
				/>
				<div className='dropzone__info'>
					<p className='dropzone__title'>Drag and drop or choose a file</p>
					<p className='dropzone__hint'>
						Supported formats: JPG, JPEG, PNG, WEBP (Max size: 5MB)
					</p>
				</div>
			</div>
		</div>
	);
};

export default Dropzone;

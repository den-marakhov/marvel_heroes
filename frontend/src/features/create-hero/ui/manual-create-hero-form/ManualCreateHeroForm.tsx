import type { IHero } from '@/entities/heroes';
import { useCreateHero } from '@/entities/heroes';
import { toApiError } from '@/shared/api';
import { useAlertModal } from '@/shared/model/useAlertModal';
import AlertModal from '@/shared/ui/alert-dialog';
import Button from '@/shared/ui/button';
import Field from '@/shared/ui/field';
import Loader from '@/shared/ui/loader';
import Select from '@/shared/ui/select';
import { zodResolver } from '@hookform/resolvers/zod';
import { Controller, useForm } from 'react-hook-form';
import {
	createHeroZodScheme,
	type CreateHeroFormData,
} from '../../model/createHeroZodScheme';
import './ManualCreateHeroForm.scss';

interface IManualCreateHeroFormProps {
	availableNames: string[];
	onCreated: (hero: IHero) => void;
}

const ManualCreateHeroForm = (props: IManualCreateHeroFormProps) => {
	const { availableNames, onCreated } = props;
	const { createHero, isCreating, isError, error, reset } = useCreateHero();
	const { isOpen, onOpenChange, open, close } = useAlertModal({
		isInProgress: isCreating,
		onClose: reset,
	});

	const {
		control,
		handleSubmit,
		getValues,
		watch,
		formState: { errors, isValid },
	} = useForm<CreateHeroFormData>({
		resolver: zodResolver(createHeroZodScheme),
		mode: 'onChange',
		defaultValues: {
			name: availableNames[0],
			description: '',
		},
	});

	const heroName = watch('name');

	const handleConfirm = () => {
		createHero(getValues(), {
			onSuccess: hero => {
				close();
				onCreated(hero);
			},
		});
	};

	const errorMessages = [
		errors.name?.message,
		errors.description?.message,
	].filter((message): message is string => Boolean(message));

	return (
		<form
			className='manual-create-hero-form'
			onSubmit={handleSubmit(open)}
		>
			<Controller
				name='name'
				control={control}
				render={({ field }) => (
					<Select
						options={availableNames}
						value={field.value}
						onChange={field.onChange}
						placeholder='Choose a hero to create'
					/>
				)}
			/>
			<Controller
				name='description'
				control={control}
				render={({ field, fieldState }) => (
					<Field
						isInvalid={fieldState.invalid}
						label='Description'
						type='textarea'
						isRequired
						placeholder=' '
						{...field}
					/>
				)}
			/>
			{errorMessages.length > 0 && (
				<div className='manual-create-hero-form__error'>
					{errorMessages.map((message, index) => (
						<p
							className='manual-create-hero-form__error-message'
							key={`error-${index}`}
						>
							{message}
						</p>
					))}
				</div>
			)}
			<div className='manual-create-hero-form__actions'>
				<AlertModal
					isOpen={isOpen}
					onOpenChange={onOpenChange}
					triggerDialogComponent={
						<Button
							label='Create Hero'
							type='button'
							isDisabled={isCreating || !isValid}
						/>
					}
					title={isError ? 'Could not create hero' : 'Confirm your action'}
					description={
						isError
							? toApiError(error).message
							: `Are you sure you want to create ${heroName}?`
					}
					confirmActionLabel={isError ? 'Try again' : 'Create'}
					cancelActionLabel='Cancel'
					onConfirm={handleConfirm}
					isConfirming={isCreating}
				>
					{isCreating && <Loader label='Creating hero' />}
				</AlertModal>
			</div>
		</form>
	);
};

export default ManualCreateHeroForm;

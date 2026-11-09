import getIdFromLabel from '@/shared/utils/getIdFromTitle';
import classNames from 'classnames';
import type { InputHTMLAttributes, Ref } from 'react';
import './Field.scss';

interface IFieldProps {
	id?: string;
	className?: string;
	label: string;
	type?: 'textarea' | InputHTMLAttributes<HTMLInputElement>['type'];
	isRequired?: boolean;
	placeholder?: string;
	inputMode?: InputHTMLAttributes<HTMLInputElement>['inputMode'];
	name?: string;
	value?: string;
	isInvalid?: boolean;
	onChange?: React.ChangeEventHandler<HTMLInputElement | HTMLTextAreaElement>;
	onBlur?: React.FocusEventHandler<HTMLInputElement | HTMLTextAreaElement>;
	ref?: Ref<HTMLInputElement | HTMLTextAreaElement>;
}

const Field = (props: IFieldProps) => {
	const {
		id = getIdFromLabel(props.label),
		className,
		label,
		type,
		isRequired,
		ref,
		isInvalid,
		...rest
	} = props;

	const isTextarea = type === 'textarea';
	const Component = isTextarea ? 'textarea' : 'input';
	const inputType = isTextarea ? undefined : type;

	return (
		<div className={classNames(className, 'field')}>
			<Component
				className={classNames('field__control', { 'is-invalid': isInvalid })}
				id={id}
				type={inputType}
				ref={ref as any}
				{...rest}
			/>
			<label className="field__label" htmlFor={id}>
				{label}{' '}
				{isRequired && (
					<span className="field__required-star" aria-hidden="true">
						*
					</span>
				)}
			</label>
		</div>
	);
};

export default Field;

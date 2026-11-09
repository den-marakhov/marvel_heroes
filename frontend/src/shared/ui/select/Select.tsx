import * as CustomSelect from '@radix-ui/react-select';
import classNames from 'classnames';
import './Select.scss';

interface ISelectProps {
	className?: string;
	options: string[];
	value?: string;
	onChange: (value: string) => void;
	placeholder?: string;
}

const Select = (props: ISelectProps) => {
	const {className, value, options, onChange, placeholder = 'Select an option' } = props;

	return (
		<div className='select'>
			<CustomSelect.Root value={value} onValueChange={onChange}>
				<CustomSelect.Trigger className='select__trigger'>
					<CustomSelect.Value
						className='select__value'
						placeholder={placeholder}
					/>
				</CustomSelect.Trigger>

				<CustomSelect.Content position='popper' className='select__content'>
					<CustomSelect.Viewport className='select__viewport'>
						{options.map((option, index) => (
							<CustomSelect.Item
								className={classNames('select__item', {
									'is-selected': value === option,
								})}
								key={`key-${option}-${index}`}
								value={option}
							>
								<CustomSelect.ItemText>{option}</CustomSelect.ItemText>
							</CustomSelect.Item>
						))}
					</CustomSelect.Viewport>
				</CustomSelect.Content>
			</CustomSelect.Root>
		</div>
	);
};

export default Select;

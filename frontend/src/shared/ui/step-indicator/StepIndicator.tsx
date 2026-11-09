import classNames from 'classnames';
import './StepIndicator.scss';

interface IStepIndicatorProps<K extends string> {
	steps: { key: K; label: string }[];
	currentStep: number;
}

const StepIndicator = <K extends string>(props: IStepIndicatorProps<K>) => {
	const { steps = [], currentStep = 0 } = props;
	return (
		<ol className='step-indicator'>
			{steps.map(({ key, label }, index) => (
				<li
					key={key}
					className={classNames('step-indicator__item', {
						'is-active': index === currentStep || index < currentStep,
					})}
				>
					{label}
				</li>
			))}
		</ol>
	);
};

export default StepIndicator;

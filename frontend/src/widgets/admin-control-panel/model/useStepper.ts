import { useCallback, useState } from 'react';

export const useStepper = (totalSteps: number) => {
	const [currentStep, setCurrentStep] = useState(0);

	const safeCurrentStep = Math.min(Math.max(currentStep, 0), totalSteps - 1);

	const handleNextStep = useCallback(() => {
		setCurrentStep(prev => Math.min(totalSteps - 1, prev + 1));
	}, [totalSteps]);

	const handlePreviousStep = useCallback(() => {
		setCurrentStep(prev => Math.max(0, prev - 1));
	}, []);

	const isFirst = safeCurrentStep === 0;
	const isLast = safeCurrentStep === totalSteps - 1;

	return {
		safeCurrentStep,
		handleNextStep,
		handlePreviousStep,
		isFirst,
		isLast,
	};
};

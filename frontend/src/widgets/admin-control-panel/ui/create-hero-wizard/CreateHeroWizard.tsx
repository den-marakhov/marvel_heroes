import type { IHero } from '@/entities/heroes';
import { ManualCreate } from '@/features/create-hero';
import { UploadImage } from '@/features/upload-image';
import StepIndicator from '@/shared/ui/step-indicator';
import { useState } from 'react';
import { createHeroSteps, STEPS_SCREEN } from '../../config';
import { useStepper } from '../../model/useStepper';
import EnrichHeroScreen from '../enrich-hero-screen';
import './CreateHeroWizard.scss';

interface ICreateHeroWizardProps {
	onCreateHero: () => void;
}

const CreateHeroWizard = (props: ICreateHeroWizardProps) => {
	const { onCreateHero } = props;

	const { safeCurrentStep, handleNextStep } = useStepper(createHeroSteps.length);

	const [hero, setHero] = useState<IHero | null>(null);

	const handleCreatedHero = (createdHero: IHero) => {
		setHero(createdHero);
		handleNextStep();
	};

	const currentScreen = createHeroSteps[safeCurrentStep].key;

	return (
		<div className='create-hero-wizard'>
			<StepIndicator
				currentStep={safeCurrentStep}
				steps={createHeroSteps.map(({ key, label }) => ({ key, label }))}
			/>
			<div className='create-hero-wizard__body'>
				{currentScreen === STEPS_SCREEN.MANUAL && (
					<ManualCreate onCreated={handleCreatedHero} />
				)}
				{currentScreen === STEPS_SCREEN.ENRICH_HERO_STEP && hero && (
					<EnrichHeroScreen
						hero={hero}
						onEnriched={handleNextStep}
						onNotFound={onCreateHero}
					/>
				)}
				{currentScreen === STEPS_SCREEN.UPLOAD_IMAGE_STEP && hero && (
					<UploadImage heroId={hero.heroId} onUploaded={onCreateHero} />
				)}
			</div>
		</div>
	);
};

export default CreateHeroWizard;

import * as RadixAccordion from '@radix-ui/react-accordion';
import classNames from 'classnames';
import { ChevronDown } from 'lucide-react';
import type { ReactNode } from 'react';
import './Accordion.scss';

interface IAccordionProps {
	className?: string;
	value: string;
	children: ReactNode;
	title: string;
}

const Accordion = (props: IAccordionProps) => {
	const { className, value, children, title } = props;

	return (
		<RadixAccordion.Root
			type='single'
			className={classNames(className, 'accordion')}
			collapsible
		>
			<RadixAccordion.Item className='accordion__item' value={value}>
				<RadixAccordion.Header className='accordion__header'>
					<RadixAccordion.Trigger className='accordion__trigger'>
						<span className='accordion__title'>{title}</span>
						<ChevronDown className='accordion__arrow' />
					</RadixAccordion.Trigger>
				</RadixAccordion.Header>

				<RadixAccordion.Content className='accordion__content'>
					<div className='accordion__content-inner'>{children}</div>
				</RadixAccordion.Content>
			</RadixAccordion.Item>
		</RadixAccordion.Root>
	);
};

export default Accordion;

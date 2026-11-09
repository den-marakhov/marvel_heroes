import type { IHero } from '@/entities/heroes/model/types';
import marvelLogo from '@/shared/assets/images/marvel-logo.svg';
import { formatInTimeZone } from 'date-fns-tz';
import type { ReactNode } from 'react';

interface ICellActions {
	uploadImage?: ReactNode;
	deleteHero?: ReactNode;
	enrichHero?: ReactNode;
}

interface IHeroColumns {
	key: string;
	columnName: string;
	cell: (hero: IHero, actions: ICellActions) => ReactNode;
}

export const heroViewListColumns: IHeroColumns[] = [
	{
		key: 'image',
		columnName: 'Image',
		cell: (_hero, actions) => actions.uploadImage,
	},
	{
		key: 'name',
		columnName: 'Name',
		cell: hero => <span>{hero.name}</span>,
	},
	{
		key: 'full_name',
		columnName: 'Full name',
		cell: (hero, actions) =>
			hero.fullName ? <span>{hero.fullName}</span> : actions.enrichHero,
	},
	{
		key: 'publisher',
		columnName: 'Publisher',
		cell: (hero, actions) =>
			hero.publisher ? (
				<img src={marvelLogo} alt='marvel logo' />
			) : (
				actions.enrichHero
			),
	},
	{
		key: 'created_at',
		columnName: 'Hero creation date',
		cell: hero => (
			<span>
				{formatInTimeZone(hero.createdAt, 'UTC', 'dd.MM.yyyy, HH:mm:ss')}
			</span>
		),
	},
	{
		key: 'actions',
		columnName: '',
		cell: (_hero, actions) => actions.deleteHero,
	},
];

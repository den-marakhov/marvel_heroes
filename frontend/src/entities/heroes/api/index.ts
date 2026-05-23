import type { IHero } from '../types';
import api from './http-client';

const SLUG = 'heroes';

const heroApi = {
	getAll: () => {
		return api.get<IHero[]>(`/${SLUG}`).then(response => response.data);
	},
};

export default heroApi;

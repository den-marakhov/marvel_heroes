const getIdFromTitle = (title: string): string => {
	return title.toLowerCase().replace(' ', '-');
};

export default getIdFromTitle;

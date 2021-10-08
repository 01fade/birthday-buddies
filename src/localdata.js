import { csv } from 'd3-fetch';
import { readable } from 'svelte/store';

export const localdata = readable({}, function start(set) {
	csv('./data/Combined40.csv').then(data => {
		set(data)
	});	

	return function stop() {
		console.log("last unsubscribe");
	};
});


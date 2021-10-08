<script>
	import MovableImage from './MovableImage.svelte';
	import { fade, fly } from 'svelte/transition';
	import { screenshot } from './screenshotClipboard.js';

	export let date = "";
	export let options = [];

	let showSelect = false;

	function sortAlphabetically(a, b, prop) {
		var textA = a[prop].toUpperCase();
		var textB = b[prop].toUpperCase();
		return (textA < textB) ? -1 : (textA > textB) ? 1 : 0;
	}

	if (options.length > 0) {
		options = options
			.filter((d) => d.image.length > 0)
			.sort((a, b) => sortAlphabetically(a, b, "label"));
	}

	const randomBetweenRange = (num, range) => {
		const res = [];
		let i = 0;
		while(i < num) {
			const random = Math.floor((Math.random() * (range[1] - range[0])) + range[0]);
			console.log(random);
			if(res.filter((d) => d.qid === options[random].qid).length === 0) {
				res.push(options[random]);
				i++;
			};
		};
		return res;
	};

	let bigImages = randomBetweenRange(5, [0, options.length]);

	const pos = [
		[3, 15],
		[42, 32],
		[69, 25],
		[15, 40],
		[48, 65]
	]

	let startScreenshot = false;

	console.log(options);

</script>

<div id="share-container" use:screenshot={startScreenshot}>
	<div class="heading">
		<h2>
			<span class="date">{date}</span><br>
			<span style="font-style: italic;">It's our birthday!</span>
		</h2>
	</div>
	<div class="info">
		<div class="logos">
			<img src="./assets/Wikidata-logo.svg" alt="Wikidata logo" style="width: 20%;">
			<img src="./assets/Wikipedia-logo-v2.svg" alt="Wikipedia logo" style="width: 20%;">
		</div>
		<span style="font-size: 1rem; padding: 0.25rem; font-weight: bold;">birthday-experiment.wiki.org</span>
	</div>
	<ul class="big-images">
		{#each bigImages as b, i }
			<li class="big-img">
				<MovableImage data={b} imgSize={400} position={pos[i]} options={options}/>
			</li>
		{/each}
	</ul>
</div>
<button class="save-image-btn" on:click={() => startScreenshot = true}>Save a screenshot</button>

<style>
	.save-image-btn {
		position: fixed;
		right: 0;
		top: 0;
		margin: 1rem;
		z-index: 5000;
	}

	#share-container {
		width: 100%;
		height: 100%;
		top: 0;
		left: 0;
		position: fixed;
	}

	.heading {
		display: flex;
		justify-content: flex-start;
	    align-items: center;
		margin: 2rem;
		flex-direction: column;
		height: 100%;
	}

	h2 {
		text-align: center;
		position: relative;
		z-index: 1000;
		display: inline-block;
		margin: 0 auto;
	    padding: 0.5rem 1rem 1rem;
	    text-shadow: 0px 0px 10px rgba(255, 255, 255, 0.9);
	}

	h2 .date {
		font-size: 0.7em; 
		text-transform: uppercase;
		position: relative;
	}

	h2 .date:after {
		content: "";
		width: 100%;
		position: absolute;
		height: 3px;
		background-color: #000;
		margin: 0;
		top: 100%;
		left: 0;
	}

	ul {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
	}

	ul, li {
		padding: 0;
		background-color: transparent;
		-webkit-user-select: none;
		-moz-user-select: none;
		-ms-user-select: none;
		user-select: none;
	}

	.info {
		position: fixed;
		bottom: 0;
		left: 0;
		margin: 1rem;
		z-index: 1000;
	}

	.logos {
		z-index: 2000;
		flex-grow: 0;
		margin: 0.5rem 0;
		justify-content: flex-start;
		align-items: center;
		flex-direction: row;
	}

</style>
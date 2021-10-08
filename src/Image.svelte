<script>
	import { onMount } from 'svelte';
	export let src = "";
	export let alt = "";

	let loaded = false;
	let thisImage;

	onMount(() => {
		thisImage.onload = () => {
			loaded = true;
		}
	}) 

	// source: https://css-tricks.com/lazy-loading-images-in-svelte/

</script>

<img {src} {alt} class:loaded bind:this={thisImage}/>

<style>
	img {
		opacity: 0;
		transform: translateY(-5px);
		transition: all 0.3s ease-out;
	}

	img.loaded {
		transform: translateY(0px);
		opacity: 1;
	}
</style>
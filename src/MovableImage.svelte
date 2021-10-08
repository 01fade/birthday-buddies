<script>
	import { onMount } from 'svelte';
	import { pannable } from './pannable.js';
	import { spring } from 'svelte/motion';
	import { createEventDispatcher } from 'svelte';

	export let data = {};
	export let imgSize = 100;
	export let position = [0, 0];
	export let options = [];
	let width;
	let height;
	const dispatch = createEventDispatcher();

	onMount(() => {
		console.log(width, height);
		relativeCoords();
	});	

	const coords = spring({ x: position[0], y: position[1] }, {
		stiffness: 0.1,
		damping: 0.5
	});

	function handlePanStart(event) {
		coords.stiffness = coords.damping = 1;
	}

	function handlePanMove(event) {
		coords.update($coords => ({
			x: $coords.x + event.detail.dx,
			y: $coords.y + event.detail.dy
		}));
	}

	function handlePanEnd(event) {
		coords.stiffness = 0.2;
		coords.damping = 0.4;
	}

	function relativeCoords() {
		coords.update($coords => ({
			x: width * position[0]/100,
			y: height * position[1]/100,
		}));	
	}

</script>

<svelte:window bind:innerWidth={width} bind:innerHeight={height} />

<div use:pannable on:panstart={handlePanStart} on:panmove={handlePanMove} on:panend={handlePanEnd} style="transform: translate({$coords.x}px,{$coords.y}px)">
	<img src="{data.image}?width={imgSize}px" alt={data.label} />
	{#if options.length > 0}
		<div class="change-options">
			<select bind:value={data}>
				{#each options as o}
					<option value={o}>{o.label}</option>
				{/each}
			</select>
		</div>
	{/if}
</div>

<style>
	div {
		position: fixed;
		top: 0;
		left: 0;
		width: 25%;
		cursor: move;
	}

	img {
		pointer-events: none;
		box-shadow: 0px 0px 0px rgba(0,0,0, 0.1);
		transition: 0.2s box-shadow;
		padding: 0.3rem;
		box-sizing: border-box;
	}

	.change-options {
		display: block;
		position: absolute;
		width: 100%;
		margin: 0.5rem;
		top: 0;
		right: 0;
		opacity: 0;
		transition: 0.2s;
		visibility: hidden;
	}

	select {
		width: 80%;
	    max-width: 160px;
	    min-width: 80px;
	}

	div:hover .change-options {
		opacity: 1;
		visibility: visible;
	}

	div:hover img {
		animation: shake 0.4s cubic-bezier(.36,.07,.19,.97) both;
		transform-origin: center;
		transform: translateX(0px) rotate(0deg);
		box-shadow: 0px 0px 10px rgba(0,0,0, 0.1);
	}

	@keyframes shake {
		33%{
		transform: translateX(-2px) rotate(-0.5deg);
		}
		66% {
		transform: translateX(2px) rotate(0.5deg);
		}
	}
	</style>
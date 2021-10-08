<script>
	export let showItem = false;
	import { fade, fly } from 'svelte/transition';
	import { createEventDispatcher } from 'svelte';

	document.addEventListener('keydown', (e) => {
		if (e.code === "Escape") { 
			showItem = false;
			modalChange();
		}
	});

	const dispatch = createEventDispatcher();

	function modalChange() {
		dispatch('modalChange', {
			modal: showItem
		});
	}

</script>


<div class="item" on:click="{() => {showItem = true; modalChange();} }">
	<slot name="label">?</slot>
</div>
{#if showItem}
	<div class="item-container" in:fly="{{y: 10}}" out:fly="{{y: -10}}">
		<div class="item-wrapper">
			<slot name="content">
				<h2>Content</h2>
			</slot>
		</div>
		<div class="back" on:click="{() => {showItem = false; modalChange();} }"><button class="secondary">← back</button></div>
	</div>
{/if}

<style>
	.item {
		padding: 0.25rem;
		font-size: 1.5rem;
		font-weight: bold;
		width: 2.5rem;
		height: 2.5rem;
		display: flex;
		justify-content: center;
		align-items: center;
		border-radius: 50%;
		background-color: #000;
		color: #fff;
		margin-top: 0.5rem;
		transform-origin: bottom center;
		transition: 0.2s;
	}

	.item:hover {
		cursor: pointer;
		transform: scale(1.1);
	}

	.item-container {
		position: fixed;
		top: 0;
		left: 0;
		background-color: rgba(255, 255, 255, 1);
		width: 100vw;
		height: 100vh;
		box-sizing: border-box;
		overflow: scroll;
		padding: 4rem 2rem 2rem;
		z-index: 9000;
	}

	.item-container .back {
		position: fixed;
		margin: 1rem;
		top: 0;
		left: 0;
	}
</style>
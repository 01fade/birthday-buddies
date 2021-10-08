<script>
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();
	export let selectedDay = 15;
	export let selectedMonth = 0;
	export let bigText = false;

	const days = [];
	for (var i = 0; i < 31; i++) {
		days[i] = { id: i+1, text: i+1 }
	}
	const monthsLabels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
	const months = [];
	for (var i = 0; i < 12; i++) {
		months[i] = { id: i, text: monthsLabels[i] }
	}

	// $: {console.log(selectedDay, selectedMonth)}

	function handleSubmit() {
		dispatch('datechange', {
			day: selectedDay,
			month: selectedMonth,
		});
	}

	// document.addEventListener('keydown', (e) => {
	// 	if (e.code === "Enter") { 
	// 		// handleSubmit();
	// 		document.theForm.addEventListener("submit", (e) => {
	// 			e.preventDefault();
	// 			console.log(e);
	// 			handleSubmit(); 
	// 		});
	// 		document.theForm.submit();
	// 	}
	// });

</script>

<form on:submit|preventDefault={handleSubmit} class:big-text="{bigText}" name="theForm">
	<div class="select-wrapper">
		<select bind:value={selectedDay}>
			{#each days as day}
				<option value={day.id}>
					{day.text}
				</option>
			{/each}
		</select>
	</div>
	<div class="select-wrapper" class:wrapped="{bigText}">
		<select bind:value={selectedMonth}>
			{#each months as month}
				<option value={month.id}>
					{month.text}
				</option>
			{/each}
		</select>
	</div>

	<button disabled={!selectedDay && !selectedMonth} type=submit>
		Search
	</button>
</form>

<style>
	form {
		text-align: center;
		position: relative;
		padding: 0.5rem;
	}

	.big-text {
		font-size: 2rem;
	}

	select {
	    -webkit-appearance: none;
	    -moz-appearance: none;
	    -ms-appearance: none;
	    -o-appearance: none;
	    appearance: none;
		padding: 6px;
		background-color: transparent;
		border: none;
		border-radius: 0;
		font-weight: bold;
		margin-bottom: 0;
		padding-right: 1.5em;
		width: 100%;
	}

	.select-wrapper {
		display: inline-block;
		position: relative;
		border-bottom: 2px solid black;
		margin: 0.25rem 1rem 0.25rem 0;
	}

	.select-wrapper:after {
		content: "";
		background-image: url("./css-assets/arrow.svg");
		background-repeat: no-repeat;
		background-position: right center;
		background-size: contain;
		right: 0;
		top: 0;
		bottom: 0;
		margin: auto 0;
		height: 100%;
		width: 0.75em;
		position: absolute;
		z-index: -1;
		font-size: 1em;
	}

	.select-wrapper.wrapped {
		margin: 0 1rem 1rem 0;	
	}
</style>
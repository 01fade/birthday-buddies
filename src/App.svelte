<script>
	import Input from "./Input.svelte";
	import Image from "./Image.svelte";
	import Map from "./Map.svelte";
	import MenuOverlay from "./MenuOverlay.svelte";
	import Share from "./Share.svelte";

	import Headroom from "headroom.js";

	import { localdata } from './localdata.js';
	import { fade, fly } from 'svelte/transition';

	let results = [];
	let shownResults = [];
	let show = true;
	let initpos = true;
	let index;
	let width;
	let height;
	let scrollY;
	let headroom;

	let sDay;
	let sMonth;

	const monthsLabels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
	const breakpoint = 600;

	function split2Int(s) {
		// year-month-day
		return s.split("-").map(x=>parseInt(x));
	}
	
	function handleDate(e) {
		const {day, month} = e.detail;
		setTimeout(() => {
			shownResults = [];
			show = false;

			setTimeout(() => {

				sDay = day;
				sMonth = month;
				results = $localdata
					.filter(d=>{
						const darr = split2Int(d.date);
						return darr[2] === day && darr[1] === month + 1;
					})
					.sort((a, b)=>b.sitelinks - a.sitelinks);
				index = 10;

				shownResults = results.slice(0, index);

				const header = document.getElementById("header");
				headroom = new Headroom(header);
				headroom.init();

			}, 400);
		}, 200);
	}

	function processDate(d) {
		const darr = split2Int(d);
		return {
			d: darr[2],
			m: monthsLabels[darr[1]-1],
			y: darr[0]
		}
	}

	async function getWikipedia(id) {
		const res = await fetch(`https://www.wikidata.org/w/api.php?format=json&formatversion=2&origin=*&action=wbgetentities&sites=enwiki&ids=${id}&languages=en&sitefilter=enwiki&props=info|sitelinks`);
		const json = await res.json();
		return json.entities[id].sitelinks.enwiki ? json.entities[id].sitelinks.enwiki.title : false;
	}

	function modal(e) {
		if (e.detail.modal) {
			document.body.classList.add('no-scroll');
		} else {
			document.body.classList.remove('no-scroll');
		}
	}

	// $: console.log(width, height, scrollY);

	$: { 
		if (scrollY/height > 0.75 && index < results.length - 1) {
			index++;
			shownResults = results.slice(0, index);
			// console.log(index, shownResults);
		}
	};
	$: screenL = width > breakpoint;
	$: mapWidth = screenL ? width*0.4 : width - 40;
	$: mapHeight = mapWidth * 0.66;

</script>

<svelte:window bind:innerWidth={width} bind:scrollY={scrollY} />

<main class:initpos>
	<header id="header" class:initpos class:big-text="{initpos}">
		<h1>When is your birthday?</h1>
		<Input bind:selectedDay={sDay} bind:selectedMonth={sMonth} on:datechange={handleDate} bigText={initpos}/>

		{#if initpos}
			<div class="logos"><div>
				<p class="small" style="width: 100%">Powered by</p>
				<img src="./assets/Wikidata-logo.svg" alt="Wikidata logo" style="width: 40%;">
				<img src="./assets/Wikipedia-logo-v2.svg" alt="Wikipedia logo" style="width: 40%;">
			</div></div>
		{/if}
	</header>

	<section bind:clientHeight={height}>
		<ul>
		{#each shownResults as res, i}
			<li class:visible="{i <= index}" class:hidden="{i > index}" class="{i % 2 === 0 ? 'result-layout-left' : 'result-layout-right'}">
				<div class="result" data-date="{res.date}" in:fade="{{duration: 100, delay: 400 }}" out:fade="{{duration: 100}}" on:introend="{() => {show = true; initpos = false; }}">

					<div class="result-context">
						<div class="result-details">
							<div class="date non-select" data-date="{results[i].date}">
								<span class="day" in:fly="{{y: -25, delay: 100, duration: 300}}">
									{processDate(results[i].date).d}
								</span>
								<span class="month" in:fly="{{y: -20, delay: 100, duration: 200}}">
									{processDate(results[i].date).m}
								</span>
								<span class="year" in:fly="{{y: -10, delay: 100, duration: 100}}">
									{processDate(results[i].date).y}
								</span>
							</div>
							
							<div class="label">
								<h2 in:fly="{{y: -10, delay: 300}}" >
									{res.label}
								</h2>
								<p class="serif" in:fly="{{y: -5, delay: 350}}">
									{res.desc}
								</p>
								<p class="small top-separator" in:fly="{{y: -5, delay: 450}}" style="opacity: 0.8">
									More on <a href="https://www.wikidata.org/wiki/{res.qid}" target="_blank">Wikidata</a>
									{#await getWikipedia(res.qid) then wikipedia}
										 | <a href="https://en.wikipedia.org/wiki/{wikipedia}" target="_blank">Wikipedia</a>
									{/await} 
								</p>
							</div>
						</div>
						
						<div class="svg-wrapper" style="width: {mapWidth}px; height: {mapHeight}px;">
							<Map latlong={res.coordinates} country={res.country}/>
						</div>

						<div class="location"><p class="serif" in:fly="{{y: -5, delay: 400}}">
							{res.place.split("|").join(", ")}{res.place && res.country ? `, ` : ``}{res.country.split("|").join(", ")}
						</p></div>
					</div>
					<div class="result-image">
						<div class="{res.image ? `img-wrapper` : `img-wrapper empty`}">
							{#if res.image}
							<Image src="{res.image}?width={screenL ? 500 : 250}px" alt={res.label} />
							{/if}
						</div>
					</div>

				</div>
			</li>
		{/each}
		</ul>
	</section>

	<div style="position: fixed; right: 0; bottom: 0; padding: 1rem; z-index: 8000;">
		{#if !initpos}
			<MenuOverlay on:modalChange={modal}>
				<svg slot="label" width="25" height="25" viewBox="0 0 25 25" fill="none" xmlns="http://www.w3.org/2000/svg" style="transform: scale(0.85); transform-origin: center;">
					<path fill-rule="evenodd" clip-rule="evenodd" d="M1.47059 0H0V1.47059V23.5294V25H1.47059H23.5294H25V23.5294V14.5H22.0588V22.0588H2.94118V2.94118H10.5V0H1.47059ZM23.5294 0H16.5441V2.94118H19.9791L7.78367 15.1366L9.86339 17.2163L22.0588 5.0209V8.45588H25V1.47059V0H23.5294Z" fill="white"/>
				</svg>
				<div slot="content" style="max-width: 1000px; margin: auto;">
					<Share date="{`${sDay} ${monthsLabels[sMonth]}`}" options="{results}"/>
				</div>
			</MenuOverlay>
		{/if}

		<MenuOverlay on:modalChange={modal}>
			<span slot="label">?</span>
			<div slot="content" style="max-width: 700px; margin: auto;">
				<h2>About</h2>
			</div>
		</MenuOverlay>
	</div>

</main>

<style>
</style>
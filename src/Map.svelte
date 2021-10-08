<script>
	import { fade } from 'svelte/transition';
	import { geoPath, geoEquirectangular, geoMercator } from "d3-geo";
	import { onMount } from "svelte";
	import { feature } from "topojson-client";
    import world from './world-countries-sans-antarctica.json';
    // https://github.com/topojson/topojson

    export let latlong = null;
    export let country = null;
	let pathD;
	let pathCountry = [];

	const projection = geoMercator().center([0, 56]).scale(150).rotate([0, 0])
	const path = geoPath(geoEquirectangular()).projection(projection);

	onMount(() => {
		const land = feature(world, world.objects.countries1);
		pathD = path(land);

		const countries = country.split("|");
		const f = world.objects.countries1.geometries.filter(d=>countries.indexOf(d.properties.name) !== -1);
		if (f.length > 0) {
			for (var i = 0; i < f.length; i++) {
				pathCountry[i] = path(feature(world, f[i]));
			}
		}
	});	

	function getLatLong(str) {
		// example: Point(-84.390277777 33.756944444)
		const split = str.split("Point(")[1].split(" ");
		const ll = [split[0], split[1].split(")")[0]];
		return projection(ll);
	}
	
</script>

<svg width="100%" height="100%" viewBox="0 0 960 600" in:fade="{{delay: 500}}">
	<path d={pathD} class="border" />
	{#if latlong.length > 0}
		<circle transform="{`translate( ${getLatLong(latlong)} )`}" cx=0 cy=0 r="5" />
		<path style="stroke-width: 2px" class="border" d="{`M${getLatLong(latlong).join(',')} C480,300 480,550 480,700`}" />
	{:else}
		{#each pathCountry as countryPath}
			<path d={countryPath} class="fill"/>
		{/each}
	{/if}
</svg>

<style>

	circle {
		fill: #f00;
		stroke-width: 1;
		stroke: #000;
		opacity: 0.9;
	}

	.fill {
		fill: #54595D;
	}

	.border {
		stroke: #54595D;
		fill: transparent;
	}
</style>
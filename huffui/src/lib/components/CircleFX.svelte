<script lang="ts">
	import { ProgressRadial } from '@skeletonlabs/skeleton';
	import { onMount } from 'svelte';

	let direction = 1;
	let value: number | undefined = undefined;
	let random = '0.00';
	export let width = 'w-16';
	export let meter = 'stroke-orange-400';
	export let track = 'stroke-orange-400/30';
	export let squareClass = 'text-orange-400';
	export let textClass = 'text-blue-500';

	onMount(() => {
		direction = Math.random() > 0.5 ? 1 : -1;
		const delay = Math.random() * 10000;

		setTimeout(() => {
			value = 1;
			setTimeout(() => {
				value = undefined;
			}, 10); // Immediately set to undefined
		}, delay);

		setInterval(() => {
			random = (Math.random() * 10).toFixed(2);
		}, 1000);
	});
</script>

<div class="relative flex items-center justify-center">
	<ProgressRadial {value} {width} {meter} {track}></ProgressRadial>
	<span
		class={`absolute rotate text-3xl font-bold text-center ${squareClass}`}
		class:reverse={direction === -1}>◆</span
	>
</div>
<div class={`text-center ${textClass}`}>{random}</div>

<style>
	@keyframes rotate {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}
	.rotate {
		display: inline-block;
		animation: rotate 2s linear infinite;
	}
	.rotate.reverse {
		animation-direction: reverse;
	}
</style>

<script lang="ts">
	import { LoadingBox } from '@flexilte/skeleton';
	import { stateStore } from '$lib/stores';
	import { ProgressBar } from '@skeletonlabs/skeleton';

	export let title: string = '';
	export let currentState: string;
	export let avgState: string;
	export let max: number;
	let currentV: number;
	let maxV: number = 100;
	function constrain(value: number, min: number, max: number): number {
		return Math.min(Math.max(value, min), max);
	}

	const calc = (v: number, avg: number) => {
		const diff = v - avg;
		if (diff >= 0) {
			return constrain(diff, 0, 100);
		}
		return 0;
	};
	stateStore.subscribe((states: Record<string, any>) => {
		if (!states[currentState]) {
			return;
		}
		if (avgState) {
			currentV = calc(states[currentState], states[avgState]);
		} else if (max) {
			maxV = max;
			currentV = states[currentState];
		}
	});
</script>

<div class="h1 mr-12">{title}</div>
{#if currentV !== undefined && maxV !== undefined}
	<ProgressBar value={currentV} max={maxV} />
{:else}
	<LoadingBox />
{/if}

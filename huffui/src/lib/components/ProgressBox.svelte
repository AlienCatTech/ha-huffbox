<script lang="ts">
	import { LoadingBox } from '@flexilte/skeleton';
	import { stateStore } from '$lib/stores';
	import { ProgressBar } from '@skeletonlabs/skeleton';

	export let name: string = '';
	export let currentState: string;
	export let maxState: string;
	let currentV: number;
	let maxV: number;
	stateStore.subscribe((states: Record<string, any>) => {
		if (!states[currentState] || !states[maxState]) {
			return;
		}

		currentV = Number(states[currentState]);
		maxV = Number(states[maxState]);
	});
</script>

{#if currentV !== null && maxV !== undefined}
	<ProgressBar value={currentV} max={maxV} />
{:else}
	<LoadingBox />
{/if}

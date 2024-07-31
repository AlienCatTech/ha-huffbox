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

		const n1 = Number(states[currentState]);
		const n2 = Number(states[maxState]);

		currentV = Math.min(n1, n2);
		maxV = Math.max(n1, n2);
	});
</script>

{#if currentV !== undefined && maxV !== undefined}
	<ProgressBar value={currentV} max={maxV} />
{:else}
	<LoadingBox />
{/if}

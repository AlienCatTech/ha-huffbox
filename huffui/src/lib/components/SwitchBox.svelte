<script lang="ts">
	import { LoadingBox } from '@flexilte/skeleton';
	import { stateStore } from '$lib/stores';
	import { callHass } from '$lib/common';
	import { ProgressRadial } from '@skeletonlabs/skeleton';

	export let name: string = '';
	export let state: string;
	let data: boolean;
	stateStore.subscribe((states: Record<string, any>) => {
		if (!states[state]) {
			return;
		}
		if (states[state] === 'on' || states[state] === 'locked') {
			data = true;
		} else {
			data = false;
		}
	});
	const handleClick = () => {
		const [domain, entity] = state.split('.');
		callHass('service', {
			domain,
			service: 'toggle',
			data: {
				entity_id: state
			}
		});
	};
</script>

{#if data !== null && data !== undefined}
	<div on:click={handleClick}>
		<ProgressRadial
			value={data ? 100 : 0}
			stroke={70}
			meter="stroke-success-500"
			track="stroke-error-500"
			class={`${data ? 'glow-icon-success' : 'glow-icon-error'}`}
		>
			{name}
		</ProgressRadial>
	</div>
{:else}
	<LoadingBox />
{/if}

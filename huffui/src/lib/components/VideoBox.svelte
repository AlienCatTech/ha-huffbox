<script lang="ts">
	import { stateStore } from '$lib/stores';

	export let state: string;
	let url: string;
	stateStore.subscribe((states: Record<string, any>) => {
		url = states[state] ?? '';
	});
</script>

<div class="flex items-center justify-center h-screen">
	<!-- svelte-ignore a11y-media-has-caption -->
	<video class="max-w mx-auto" controls autoplay muted loop width="1900">
		<source src={url} type="video/mp4" />
		<!-- Fallback for browsers that don't support the video element -->
		Your browser does not support the video tag.
	</video>
</div>

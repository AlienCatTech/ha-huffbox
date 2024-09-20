<script lang="ts">
	import { stateStore } from '$lib/stores';

	export let state;
	let text = '';
	stateStore.subscribe((states: Record<string, any>) => {
		text = states[state] ?? '';
	});
	$: warningScroll = () => {
		return Array(7).fill(text);
	};
</script>

<div class="animated-stripes flex justify-center items-center scrolling-text-container">
	{#each warningScroll() as e}
		<div class="text-black font-bold text-6xl scrolling-text pr-5 top-1/2">
			{e}
		</div>
	{/each}
</div>

<style>
	.animated-stripes {
		@apply overflow-hidden relative;
		background-image: linear-gradient(
			45deg,
			#000 25%,
			theme('colors.yellow.500') 25%,
			theme('colors.yellow.500') 50%,
			#000 50%,
			#000 75%,
			theme('colors.yellow.500') 75%,
			theme('colors.yellow.500') 100%
		);
		background-size: 56.57px 56.57px; /* 40px * sqrt(2) to account for the 45 degree angle */
		animation: move-stripes 2s linear infinite;
	}

	@keyframes move-stripes {
		0% {
			background-position: 56.57px 0;
		}
		100% {
			background-position: 0 0;
		}
	}
	.scrolling-text-container {
		@apply relative overflow-hidden w-full h-full;
		white-space: nowrap;
	}

	.scrolling-text {
		animation: scroll-text 5s linear infinite;
		background: theme('colors.yellow.500');
		/* display: inline-block; */
		/* margin-left: 100%;  */
	}

	@keyframes scroll-text {
		from {
			transform: translateX(100%);
		}
		to {
			transform: translateX(-100%);
		}
	}
</style>

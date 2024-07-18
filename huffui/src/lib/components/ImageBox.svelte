<script lang="ts">
	import { callHass } from '$lib/common';
	import { stateStore } from '$lib/stores';

	export let state = '';
	export let alt = '';
	let url = '';
	let inputRef: HTMLInputElement;
	stateStore.subscribe((states: Record<string, any>) => {
		url = states[state];
	});
	const handleClick = () => {
		inputRef.click();
	};
	const handleFileChange = (event: Event) => {
		const target = event.target as HTMLInputElement;
		const file = target.files?.[0];
		if (file) {
			const reader = new FileReader();
			reader.onload = (e) => {
				const fileBytes = e.target?.result as ArrayBuffer;

				callHass('uploadImage', {
					bytes: fileBytes,
					name: file.name,
					type: file.type
				});
			};
			reader.readAsArrayBuffer(file);
		}
	};
</script>

<div class="w-full overflow-hidden flex items-center justify-center">
	<img src={url} {alt} class="h-full w-auto object-cover" on:click={handleClick} />
	<input
		type="file"
		accept="image/*"
		class={url ? 'hidden' : ''}
		bind:this={inputRef}
		on:change={handleFileChange}
	/>
</div>

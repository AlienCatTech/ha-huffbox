<script lang="ts">
	import QRCode from 'qrcode';
	import { onMount } from 'svelte';
	export let type: string = 'text';
	export let title: string = '';
	export let light: string = 'ffffff00';
	export let dark: string = '0d3d56ff';
	export let data: string;

	let dataUrl = '';
	onMount(() => {
		if (type === 'wifi') {
			const parts = data.split('||');
			data = `WIFI:T:WPA;S:${parts[0]};P:${parts[1]};;`;
		}

		QRCode.toDataURL(data, { color: { light, dark } }).then((url) => {
			dataUrl = url;
		});
	});
</script>

<div class="flex">
	<div class="w-full h-full">
		<div class="text-center text-2xl">
			<div>{title}</div>
		</div>
		<img src={dataUrl} alt="qrcode" class="mx-auto object-contain" />
	</div>
</div>

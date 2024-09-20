<script lang="ts">
	import { modeCurrent } from '@skeletonlabs/skeleton';
	import QRCode from 'qrcode';
	import { onMount } from 'svelte';
	export let type: string = 'text';
	export let title: string = '';
	export let subtitle: string = '';
	export let light: string = 'ffffffff';
	export let dark: string = '0d3d56ff';
	export let data: string;

	const transparent = '00000000';

	let dataUrl = '';
	onMount(async () => {
		if (type === 'wifi') {
			const parts = data.split('||');
			data = `WIFI:T:WPA;S:${parts[0]};P:${parts[1]};;`;
		}

		await adaptColor($modeCurrent);
	});

	const adaptColor = async (isLight: boolean) => {
		const colorOpt = isLight ? { light: transparent, dark } : { light: transparent, dark: light };
		dataUrl = await QRCode.toDataURL(data, { color: colorOpt });
	};

	modeCurrent.subscribe(async (isLight) => {
		await adaptColor(isLight);
	});
</script>

<div class="flex">
	<div class="w-full h-full">
		<div class="text-center">
			<div class="text-2xl">{title}</div>
		</div>
		<img src={dataUrl} alt="qrcode" class="mx-auto object-contain" />
		<div class="text-center">
			<div class="text-lg">{subtitle}</div>
		</div>
	</div>
</div>

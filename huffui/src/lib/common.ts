export const fancyLogging = (msg: string, obj?: any) =>
	console.log(
		`%c${msg}`,
		'font-family: "Courier New", monospace; color: #ecf5f9; text-shadow: 0 0 5px #ecf5f9; background-color: #061e2a; padding: 10px; border: 1px solid #ecf5f9; border-radius: 5px; font-size: 16px; font-weight: bold;',
		obj
	);

type CallService = {
	domain: string;
	service: string;
	data: any;
};

type CallApi = {
	method: string;
	path: string;
	data?: any;
	headers?: any;
};

type UploadImage = {
	bytes: ArrayBuffer;
	name: string;
	type: string;
};

type CallWs = {
	message: any;
};

export const callHass = (
	eventType: 'ws' | 'api' | 'service' | 'uploadImage',
	data: UploadImage | CallApi | CallService | CallWs
) => {
	console.log('hass', eventType, data);
	window.parent.postMessage(
		{
			type: eventType,
			data
		},
		'*'
	);
};

export function populate(template: string, ctx: any): string {
	return template.replace(/\{\{([^}]+)\}\}/g, (match, key) => {
		const [prefix, ...parts] = key.trim().split('.');
		const rest = parts.join('.');
		if (prefix === 'ctx') {
			return ctx[rest];
		} else if (prefix === 'img') {
			return `<img src="${rest}" width="30"/>`;
		}
		return '';
	});
}

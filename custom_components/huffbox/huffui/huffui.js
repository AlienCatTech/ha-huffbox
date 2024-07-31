// Simplest possible custom card
// Does nothing. Doesn't look like anything
// let LitElement = Object.getPrototypeOf(customElements.get('ha-panel-lovelace'));
// const html = LitElement?.prototype.html;
class HuffboxUI extends HTMLElement {
	setConfig(config) {
		this._config = config;
	}

	static getConfigElement() {
		return document.createElement('huffbox-ui-editor');
	}

	static getStubConfig() {
		return { token: '', config_json: '{}' };
	}

	set hass(hass) {
		this._hass = hass;
		if (!this.card) {
			this.initIframe();
		} else {
			this.updateIframeState();
		}
	}

	hideSidebarsIfKiosk() {
		const urlParams = new URLSearchParams(window.location.search);
		if (urlParams.has('kiosk')) {
			const homeAssistant = document.querySelector('home-assistant');
			if (homeAssistant && homeAssistant.shadowRoot) {
				const main = homeAssistant.shadowRoot.querySelector('home-assistant-main');
				if (main && main.shadowRoot) {
					const drawer = main.shadowRoot.querySelector('ha-drawer');
					if (drawer && drawer.shadowRoot) {
						const content = drawer.shadowRoot.querySelector('.mdc-drawer-app-content');
						if (content) {
							content.setAttribute('style', 'padding: 0');
						}
						const aside = drawer.shadowRoot.querySelector('aside');
						if (aside) {
							aside.setAttribute('style', 'display: none');
						}
					}
				}
			}
		}
	}

	initIframe() {
		this.hideSidebarsIfKiosk();
		const shadow = this.shadowRoot || this.attachShadow({ mode: 'open' });
		const card = document.createElement('ha-card');
		card.style.cssText = `overflow: auto; width: 100%; height: 100%; display: flex; flex-direction: column;`;

		const iframe = document.createElement('iframe');
		iframe.src = '/huffbox/huffui/index.html';
		iframe.style.cssText = 'width: 100%; height: 100%; border: none; overflow: auto;';
		iframe.sandbox =
			'allow-forms allow-popups allow-pointer-lock allow-same-origin allow-scripts allow-modals allow-downloads';

		iframe.onload = () => {
			iframe.contentWindow.postMessage(
				{
					msg: 'init',
					data: this._hass.states
				},
				'*'
			);
			window.addEventListener('message', this.handleIframeMessage.bind(this));
		};

		this._hass.connection.subscribeEvents(() => {
			location.href = '/huffbox-dashboard?kiosk';
		}, 'huffbox_refresh_event');

		card.appendChild(iframe);
		shadow.appendChild(card);
		this.card = card;
		this.iframe = iframe;
		console.log('hass', this._hass);
	}

	updateIframeState() {
		if (this.iframe) {
			this.iframe.contentWindow.postMessage({ msg: 'stateUpdate', data: this._hass.states }, '*');
		}
	}

	handleIframeMessage(event) {
		console.log(event.data);
		if (event.data.type === 'service') {
			this._hass.callService(event.data.data.domain, event.data.data.service, event.data.data.data);
		} else if (event.data.type === 'api') {
			this._hass.callApi(
				event.data.data.method,
				event.data.data.path,
				event.data.data.data,
				event.data.data.headers
			);
		} else if (event.data.type === 'uploadImage') {
			const formData = new FormData();
			const blob = new Blob([event.data.data.bytes], { type: event.data.data.type }); // Adjust type if necessary
			formData.append('file', blob, event.data.data.name);

			fetch('/api/image/upload', {
				method: 'post',
				headers: {
					Authorization: 'Bearer ' + this._hass.auth.data.access_token
				},
				body: formData
			})
				.then((res) => res.json())
				.then((j) =>
					this._hass.callService('text', 'set_value', {
						entity_id: 'text.huffbox_subject_picture',
						value: `/api/image/serve/${j.id}/original`
					})
				);
		}
	}

	getCardSize() {
		return 5;
	}
}

customElements.define('ha-panel-huffbox-ui', HuffboxUI);

// const LitElement = Object.getPrototypeOf(customElements.get("ha-panel-lovelace"));
// class HuffboxUIEditor extends LitElement {
// 	setConfig(config) {
// 		this._config = {
// 			...config
// 		};
// 	}
// 	_valueChanged(e) {
// 		this._config = { ...e.detail.value };
// 		this.dispatchEvent(new CustomEvent('config-changed', { detail: { config: this._config } }));
// 	}

// 	render() {
// 		if (!this.hass) {
// 			return html``;
// 		}
// 		const schema = [
// 			// {
// 			//   name: "token",
// 			//   required: true,
// 			//   selector: { text: { type: "password" } },
// 			// },
// 			{ name: 'layout_config', required: true, selector: { template: {} } }
// 		];

// 		return html`<ha-form
// 			.data=${this._config}
// 			.schema=${schema}
// 			.computeLabel=${(schema) => schema.name}
// 			@value-changed=${this._valueChanged}
// 		></ha-form>`;
// 	}
// }

// This registers the card class as a custom element that can be included in lovelace by
// type: custom:huffbox-ui
// if (!customElements.get('huffbox-ui-editor'))
// 	customElements.define('huffbox-ui-editor', HuffboxUIEditor);
// if (!customElements.get('huffbox-ui')) customElements.define('huffbox-ui', HuffboxUI);

/* To use this card:
  - Put this file in <config>/www/huffbox-ui.js
  - Add "/local/huffbox-ui.js" to your lovelace resources
  - Refresh your browser
  - Add a new lovelace card and set its configuration to:
  type: custom:huffbox-ui

  */
// window.customCards = window.customCards || [];
// window.customCards.push({
// 	type: 'huffbox-ui',
// 	name: 'huffbox-ui',
// 	preview: false,
// 	description: 'Meow Meow'
// });

let initMsg = 'HuffUI Loaded';

console.log(
	`%c${initMsg}`,
	'font-family: "Courier New", monospace; color: #ecf5f9; text-shadow: 0 0 5px #ecf5f9; background-color: #061e2a; padding: 10px; border: 1px solid #ecf5f9; border-radius: 5px; font-size: 16px; font-weight: bold;'
);

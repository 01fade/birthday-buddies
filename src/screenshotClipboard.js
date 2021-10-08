import html2canvas from 'html2canvas';

export function screenshot(node, start) {

	function clipboardSuccess() {
		alert("Image was saved to your clipboard.");
	}

	function clipboardError() {
		alert("Couldn't save image to your clipboard. Please take a screenshot");
	}

	function saveImage(s) {
		console.log(s);
		if (s) {
		    html2canvas(document.querySelector("#share-container"), { logging: true, letterRendering: 1, allowTaint: true, useCORS: true})
		    	.then(canvas => canvas
		    		.toBlob(blob => navigator.clipboard
			    		.write([new ClipboardItem({'image/png': blob})])
			    		.then(clipboardSuccess, clipboardError)
			    		)
		    		);
		}
	}

	saveImage(start);

	return {
		update(start) {
			saveImage(start);
		},
		destroy() {
			
		}
	};
}
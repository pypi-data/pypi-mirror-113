(self.webpackChunkjupyterlab_jupytext=self.webpackChunkjupyterlab_jupytext||[]).push([[568],{568:(t,e,a)=>{"use strict";Object.defineProperty(e,"__esModule",{value:!0});const o=a(138),r=a(611),n=[{format:"ipynb",label:"Pair Notebook with ipynb document"},{format:"auto:light",label:"Pair Notebook with light Script"},{format:"auto:percent",label:"Pair Notebook with percent Script"},{format:"auto:hydrogen",label:"Pair Notebook with Hydrogen Script"},{format:"auto:nomarker",label:"Pair Notebook with nomarker Script"},{format:"md",label:"Pair Notebook with Markdown"},{format:"md:myst",label:"Pair Notebook with MyST Markdown"},{format:"Rmd",label:"Pair Notebook with R Markdown"},{format:"custom",label:"Custom pairing"},{format:"none",label:"Unpair Notebook"}];function i(t){if(!t.currentWidget)return[];let e=function(t){if(!t.currentWidget)return[];if(!t.currentWidget.context.model.metadata.has("jupytext"))return[];const e=t.currentWidget.context.model.metadata.get("jupytext");return(e&&e.formats?e.formats.split(","):[]).filter((function(t){return""!==t}))}(t);const a=t.currentWidget.context.model.metadata.get("language_info");if(a&&a.file_extension){const t=a.file_extension.substring(1);e=e.map((function(e){return e===t?"auto:light":e.replace(t+":","auto:")}))}let o=t.currentWidget.context.path.split(".").pop();if(!o)return e;o=-1==["ipynb","md","Rmd"].indexOf(o)?"auto":o;for(const t in e)if(e[t].split(":")[0]==o)return e;if(-1!=["ipynb","md","Rmd"].indexOf(o))e.push(o);else{let a="light";if(t.currentWidget.context.model.metadata.has("jupytext")){const e=t.currentWidget.context.model.metadata.get("jupytext");e&&e.text_representation&&e.text_representation.format_name&&(a=e.text_representation.format_name)}e.push("auto:"+a)}return e}const d={id:"jupyterlab-jupytext",autoStart:!0,requires:[o.ICommandPalette,r.INotebookTracker],activate:(t,e,a)=>{console.log("JupyterLab extension jupyterlab-jupytext is activated"),n.forEach(((o,r)=>{const n=o.format,d="jupytext:"+n;t.commands.addCommand(d,{label:o.label,isToggled:()=>{if(!a.currentWidget)return!1;const t=i(a);if("custom"==n){for(const e in t){const a=t[e];if(-1==["ipynb","auto:light","auto:percent","auto:hydrogen","auto:nomarker","md","Rmd","md:myst"].indexOf(a))return!0}return!1}return-1!=t.indexOf(n)},isEnabled:()=>{if(!a.currentWidget)return!1;const t=a.currentWidget.context.path.split(".").pop();return n!==t&&("none"!==n||i(a).length>1)},execute:()=>{const t=a.currentWidget.context.model.metadata.get("jupytext");let e=i(a);if(console.log("Jupytext: executing command="+d),"custom"==n)return void alert("Please edit the notebook metadata directly if you wish a custom configuration.");let o=a.currentWidget.context.path.split(".").pop();o=-1==["ipynb","md","Rmd"].indexOf(o)?"auto":o;const r=e.indexOf(n);if("none"===n)for(const t in e){const a=e[t];if(a.split(":")[0]===o){e=[a];break}}else if(-1!=r){e.splice(r,1);let t=!1;for(const a in e)if(e[a].split(":")[0]===o){t=!0;break}if(!t)return}else{const t=[];for(const a in e){const o=e[a];o.split(":")[0]!==n.split(":")[0]&&t.push(o)}e=t,e.push(n)}if(1===e.length)if("auto"!==o)e=[];else if(t&&t.text_representation){const a=e[0].split(":")[1];t.text_representation.format_name=a,e=[]}if(0===e.length){if(!a.currentWidget.context.model.metadata.has("jupytext"))return;return t.formats&&delete t.formats,void(0==Object.keys(t).length&&a.currentWidget.context.model.metadata.delete("jupytext"))}t?t.formats=e.join():a.currentWidget.context.model.metadata.set("jupytext",{formats:e.join()})}}),console.log("Jupytext: adding command="+d+" with rank="+(r+1)),e.addItem({command:d,rank:r+2,category:"Jupytext"})})),e.addItem({args:{text:"Jupytext Reference",url:"https://jupytext.readthedocs.io/en/latest/"},command:"help:open",category:"Jupytext",rank:0}),e.addItem({args:{text:"Jupytext FAQ",url:"https://jupytext.readthedocs.io/en/latest/faq.html"},command:"help:open",category:"Jupytext",rank:1}),t.commands.addCommand("jupytext_metadata",{label:"Include Metadata",isToggled:()=>!!a.currentWidget&&(!!a.currentWidget.context.model.metadata.has("jupytext")&&"-all"!==a.currentWidget.context.model.metadata.get("jupytext").notebook_metadata_filter),isEnabled:()=>{if(!a.currentWidget)return!1;if(!a.currentWidget.context.model.metadata.has("jupytext"))return!1;const t=a.currentWidget.context.model.metadata.get("jupytext");return void 0===t.notebook_metadata_filter||"-all"===t.notebook_metadata_filter},execute:()=>{if(console.log("Jupytext: toggling YAML header"),!a.currentWidget)return;if(!a.currentWidget.context.model.metadata.has("jupytext"))return;const t=a.currentWidget.context.model.metadata.get("jupytext");if(t.notebook_metadata_filter)return delete t.notebook_metadata_filter,void("-all"===t.cell_metadata_filter&&delete t.cell_metadata_filter);t.notebook_metadata_filter="-all",void 0===t.cell_metadata_filter&&(t.cell_metadata_filter="-all")}}),e.addItem({command:"jupytext_metadata",rank:n.length+3,category:"Jupytext"})}};e.default=d}}]);
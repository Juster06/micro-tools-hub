import {convert} from './engine.mjs';
self.onmessage=({data})=>{try{self.postMessage({ok:true,...convert(data.input)});}catch(e){self.postMessage({ok:false,error:e instanceof Error?e.message:'Unable to convert Markdown.'});}};

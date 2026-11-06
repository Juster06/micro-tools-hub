import {convert,sanitize} from './engine.mjs';
self.onmessage=({data})=>{try{self.postMessage({ok:true,...(data.testRawHTML?sanitize(data.input):convert(data.input))});}catch(e){self.postMessage({ok:false,error:e instanceof Error?e.message:'Unable to convert Markdown.'});}};

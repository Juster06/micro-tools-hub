import { Marked } from './packages/marked-18.1.3/lib/marked.esm.js';
import { boundedParse, CSP } from '../task22/scripts/vendor/task21/markup-core.mjs';
export const LIMITS = Object.freeze({input:32768,output:131072,nodes:4096,depth:64,deadline:2000});
const utf8=new TextEncoder();
const escape=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const allowed=new Set('p h1 h2 h3 h4 h5 h6 ul ol li blockquote pre code em strong del br hr table thead tbody tr td th'.split(' '));
export function guard(s,maximum=LIMITS.input){if(typeof s!=='string'||!s.trim())throw Error('Enter Markdown.');if(s.length>maximum||utf8.encode(s).length>maximum)throw Error('Text exceeds '+maximum/1024+' KiB UTF-8.');if(/[\uD800-\uDFFF]/u.test(s.replace(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g,'')))throw Error('Unpaired Unicode surrogate.');return s;}
function safeLink(value){if(/[\u0000-\u0020\u007f-\u009f]/u.test(value)||!/^https?:\/\//i.test(value))return null;try{const url=new URL(value);return ['http:','https:'].includes(url.protocol)&&!url.username&&!url.password?url.href:null;}catch{return null;}}
export function sanitize(html){
 const tree=boundedParse(guard(html,LIMITS.output),false,LIMITS.output);let exported=[],inert=[],bytes=0,omissions=0;
 function add(a,b=a){bytes+=utf8.encode(a).length+utf8.encode(b).length;if(bytes>2*LIMITS.output)throw Error('Output exceeds 128 KiB.');exported.push(a);inert.push(b);}
 function walk(n){if(n.nodeName==='#text'){add(escape(n.value));return;}if(!n.tagName){for(const c of n.childNodes??[])walk(c);return;}if(n.namespaceURI!=='http://www.w3.org/1999/xhtml'){omissions++;return;}
  if(n.tagName==='a'){const link=safeLink(n.attrs.find(x=>x.name==='href')?.value??'');if(link)add('<a href="'+escape(link)+'" rel="noopener noreferrer">','');else omissions++;for(const c of n.childNodes??[])walk(c);if(link)add('</a>','');return;}
  if(!allowed.has(n.tagName)){omissions++;return;}
  if(n.attrs.length)omissions++;add('<'+n.tagName+'>');for(const c of n.childNodes??[])walk(c);if(!['br','hr'].includes(n.tagName))add('</'+n.tagName+'>');
 }walk(tree);
 const text=exported.join(''),preview=documentFor(inert.join('')),download=documentFor(text);for(const s of [text,preview,download])guard(s,LIMITS.output);
 return {text,preview,download,omissions};
}
export function documentFor(fragment){return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="'+CSP+'"><title>Converted Markdown</title></head><body>'+fragment+'</body></html>';}
export function convert(input){guard(input);const parser=new Marked({gfm:true,breaks:false,async:false,renderer:{html({text}){return escape(text);},image({text}){return escape(text);}}});
 const tokens=parser.lexer(input);let count=0,stack=[[tokens,0]];
 while(stack.length){const [value,depth]=stack.pop();if(depth>LIMITS.depth)throw Error('Markdown exceeds 64 nesting levels.');if(Array.isArray(value)){for(const v of value)stack.push([v,depth]);}else if(value&&typeof value==='object'){if(++count>LIMITS.nodes)throw Error('Markdown exceeds 4,096 tokens.');for(const [key,v]of Object.entries(value)){if(key!=='links'&&v&&typeof v==='object')stack.push([v,depth+1]);}}}
 const raw=parser.parser(tokens);guard(raw,LIMITS.output);const result=sanitize(raw);return {...result,warning:'Raw HTML is escaped; images become text. Preview links are inert. Export links allow only explicit HTTP(S) URLs without credentials. Styling, task checkboxes, IDs and other attributes are omitted. No extensions, math, diagrams or syntax highlighting.'};
}

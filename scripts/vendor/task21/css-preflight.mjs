import { tokenize, tokenTypes as T } from "css-tree";
export function preflight(input) {
  const stack = [];
  let tokens = 0;
  tokenize(input, (type, start, end) => {
    if (++tokens > 8192) throw Error("CSS exceeds 8,192 tokens.");
    const raw = input.slice(start, end);
    if ([T.BadString, T.BadUrl].includes(type))
      throw Error("Malformed CSS string or URL.");
    if (type === T.String) {
      let escapes = 0;
      for (let i = raw.length - 2; i >= 0 && raw[i] === "\\"; i--) escapes++;
      if (raw.length < 2 || raw.at(-1) !== raw[0] || escapes % 2)
        throw Error("Unclosed CSS string.");
    }
    if (type === T.Comment && !raw.endsWith("*/"))
      throw Error("Unclosed CSS comment.");
    if (type === T.Url && !raw.endsWith(")")) throw Error("Unclosed CSS URL.");
    if (type === T.Function || type === T.LeftParenthesis)
      stack.push(T.RightParenthesis);
    if (type === T.LeftCurlyBracket) stack.push(T.RightCurlyBracket);
    if (type === T.LeftSquareBracket) stack.push(T.RightSquareBracket);
    if (stack.length > 64) throw Error("CSS exceeds 64 nesting levels.");
    if (
      [T.RightCurlyBracket, T.RightParenthesis, T.RightSquareBracket].includes(
        type,
      ) &&
      stack.pop() !== type
    )
      throw Error("Unbalanced CSS brackets.");
  });
  if (stack.length) throw Error("Unclosed CSS block or function.");
}

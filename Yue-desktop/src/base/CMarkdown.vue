<script setup>
// 轻量 Markdown 渲染：安全转义 + 块级/行内解析，不引第三方库
import { computed } from "vue";

const props = defineProps({
  content: { type: String, default: "" },
});

function escapeHtml(s) {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function inline(s) {
  let t = escapeHtml(s);
  // 行内代码（先保护，避免被后续规则破坏）
  const codes = [];
  t = t.replace(/`([^`]+)`/g, (_, c) => {
    codes.push(c);
    return `\u0000${codes.length - 1}\u0000`;
  });
  // 粗体
  t = t.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  // 斜体
  t = t.replace(/(^|[^*])\*([^*]+)\*(?!\*)/g, "$1<em>$2</em>");
  // 链接
  t = t.replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
  // 恢复行内代码
  t = t.replace(/\u0000(\d+)\u0000/g, (_, i) => `<code>${codes[+i]}</code>`);
  return t;
}

const html = computed(() => {
  const src = props.content.replace(/\r\n/g, "\n");
  const lines = src.split("\n");
  const out = [];
  let i = 0;
  let listType = null;

  while (i < lines.length) {
    const line = lines[i];

    // 代码块
    if (/^```/.test(line)) {
      const lang = line.slice(3).trim();
      const buf = [];
      i++;
      while (i < lines.length && !/^```/.test(lines[i])) {
        buf.push(lines[i]);
        i++;
      }
      i++; // 跳过 ``` 结束
      const code = escapeHtml(buf.join("\n"));
      out.push(lang ? `<pre><code class="lang-${escapeHtml(lang)}">${code}</code></pre>` : `<pre><code>${code}</code></pre>`);
      listType = null;
      continue;
    }

    // 标题
    const h = line.match(/^(#{1,6})\s+(.*)$/);
    if (h) {
      out.push(`<h${h[1].length}>${inline(h[2])}</h${h[1].length}>`);
      listType = null;
      i++;
      continue;
    }

    // 引用
    if (/^>\s?/.test(line)) {
      const buf = [];
      while (i < lines.length && /^>\s?/.test(lines[i])) {
        buf.push(lines[i].replace(/^>\s?/, ""));
        i++;
      }
      out.push(`<blockquote>${buf.map((b) => inline(b)).join("<br>")}</blockquote>`);
      listType = null;
      continue;
    }

    // 无序列表
    const ul = line.match(/^[-*+]\s+(.*)$/);
    if (ul) {
      if (listType !== "ul") { if (listType) out.push(`</${listType}>`); out.push("<ul>"); listType = "ul"; }
      out.push(`<li>${inline(ul[1])}</li>`);
      i++;
      continue;
    }

    // 有序列表
    const ol = line.match(/^\d+[.)]\s+(.*)$/);
    if (ol) {
      if (listType !== "ol") { if (listType) out.push(`</${listType}>`); out.push("<ol>"); listType = "ol"; }
      out.push(`<li>${inline(ol[1])}</li>`);
      i++;
      continue;
    }

    // 表格
    if (line.includes("|") && lines[i + 1] && /^\s*\|?[\s:-|]+\|?\s*$/.test(lines[i + 1]) && lines[i + 1].includes("-")) {
      const head = line.split("|").map((c) => c.trim()).filter((c, idx, arr) => !(idx === 0 && c === "") && !(idx === arr.length - 1 && c === ""));
      i += 2;
      const rows = [];
      while (i < lines.length && lines[i].includes("|")) {
        const cells = lines[i].split("|").map((c) => c.trim()).filter((c, idx, arr) => !(idx === 0 && c === "") && !(idx === arr.length - 1 && c === ""));
        rows.push(`<tr>${cells.map((c) => `<td>${inline(c)}</td>`).join("")}</tr>`);
        i++;
      }
      out.push(`<table><thead><tr>${head.map((c) => `<th>${inline(c)}</th>`).join("")}</tr></thead><tbody>${rows.join("")}</tbody></table>`);
      listType = null;
      continue;
    }

    // 分割线
    if (/^\s*(---+|\*\*\*+|___+)\s*$/.test(line)) {
      out.push("<hr>");
      listType = null;
      i++;
      continue;
    }

    // 空行
    if (!line.trim()) {
      if (listType) { out.push(`</${listType}>`); listType = null; }
      i++;
      continue;
    }

    // 段落
    const para = [line];
    i++;
    while (i < lines.length && lines[i].trim() && !/^```/.test(lines[i]) && !/^#{1,6}\s/.test(lines[i]) && !/^>\s?/.test(lines[i]) && !/^[-*+]\s+/.test(lines[i]) && !/^\d+[.)]\s+/.test(lines[i]) && !/^\s*---+\s*$/.test(lines[i])) {
      para.push(lines[i]);
      i++;
    }
    if (listType) { out.push(`</${listType}>`); listType = null; }
    out.push(`<p>${para.map((l) => inline(l)).join("<br>")}</p>`);
  }
  if (listType) out.push(`</${listType}>`);
  return out.join("\n");
});
</script>

<template>
  <div class="markdown-body" v-html="html"></div>
</template>

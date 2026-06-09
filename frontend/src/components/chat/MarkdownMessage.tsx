"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function MarkdownMessage({ content }: { content: string }) {
  return (
    <div className="prose prose-invert prose-sm max-w-none prose-p:my-2 prose-ul:my-2 prose-li:my-0.5 prose-headings:my-2 prose-strong:text-emerald-300">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          a: ({ href, children }) => (
            <a href={href} target="_blank" rel="noopener noreferrer" className="text-emerald-400 underline">
              {children}
            </a>
          ),
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}

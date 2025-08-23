import React from 'react'
import Markdown from 'react-markdown'

interface StyledMarkdownProps {
  content?: string
  children?: string
  className?: string
  hideTopHeading?: boolean // option to hide h1 if present
}

// Centralized styled markdown component
export const StyledMarkdown: React.FC<StyledMarkdownProps> = ({ content, children, className = '', hideTopHeading = true }) => {
  const source = content ?? children ?? ''
  return (
    <div className={className}>
      <Markdown
        components={{
          // 제목 두번 출력 방지 
          h1: ({ node, ...props }) => hideTopHeading ? <></> : <h1 className="text-3xl font-bold mt-6 mb-4 leading-snug" {...props} />,
          h2: ({ node, ...props }) => <h2 className="text-2xl font-semibold mt-5 mb-3 leading-snug" {...props} />,
          h3: ({ node, ...props }) => <h3 className="text-xl font-semibold mt-4 mb-2 leading-snug" {...props} />,
          h4: ({ node, ...props }) => <h4 className="text-lg font-semibold mt-4 mb-2" {...props} />,
          p: ({ node, ...props }) => <p className="mb-4 leading-relaxed" {...props} />,
          ul: ({ node, ...props }) => <ul className="list-disc ml-6 mb-4 space-y-1" {...props} />,
          ol: ({ node, ...props }) => <ol className="list-decimal ml-6 mb-4 space-y-1" {...props} />,
          li: ({ node, ...props }) => <li className="marker:text-muted-foreground" {...props} />,
          code: ({ node, className, children, ...props }) => {
            return (
              <code className={"block w-full p-3 rounded bg-muted font-mono text-sm overflow-x-auto mb-4" + (className ? ` ${className}` : '')} {...props}>
                {children}
              </code>
            )
          },
          blockquote: ({ node, ...props }) => <blockquote className="border-l-4 border-muted-foreground/30 pl-4 italic text-muted-foreground mb-4" {...props} />,
          hr: ({ node, ...props }) => <hr className="my-8 border-border" {...props} />
        }}
      >
        {source}
      </Markdown>
    </div>
  )
}

export default StyledMarkdown

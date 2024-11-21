'use client'
// InitializedMDXEditor.tsx
import type { ForwardedRef } from 'react'
import {
  headingsPlugin,
  listsPlugin,
  quotePlugin,
  thematicBreakPlugin,
  markdownShortcutPlugin,
  MDXEditor,
  toolbarPlugin,
  UndoRedo,
  BoldItalicUnderlineToggles,
  BlockTypeSelect,
  CodeToggle,
  Separator,
  type MDXEditorMethods,
  type MDXEditorProps,
  diffSourcePlugin,
  ListsToggle,
  InsertImage,
  imagePlugin,
  CreateLink,
  linkDialogPlugin,
  InsertThematicBreak,
  tablePlugin,
  InsertTable,
  DiffSourceToggleWrapper,
} from '@mdxeditor/editor'
import '@mdxeditor/editor/style.css'

export default function InitializedMDXEditor({
  editorRef,
  sourceMarkdown,
  ...props
}: { editorRef: ForwardedRef<MDXEditorMethods> | null } & MDXEditorProps & { sourceMarkdown: string }) {
  return (
    <MDXEditor
      plugins={[
        headingsPlugin(),
        listsPlugin(),
        quotePlugin(),
        thematicBreakPlugin(),
        markdownShortcutPlugin(),
        diffSourcePlugin({ diffMarkdown: sourceMarkdown, viewMode: 'rich-text' }),
        imagePlugin(),
        linkDialogPlugin(),
        tablePlugin(),
        toolbarPlugin({
          toolbarContents: () => (
          <>
              {' '}
              <UndoRedo />
              <Separator />
              <BoldItalicUnderlineToggles />
              <CodeToggle />
              <Separator />
              <ListsToggle />
              <Separator />
              <BlockTypeSelect />
              <Separator />
              <CreateLink />
              <InsertImage />
              <Separator />
              <InsertTable />
              <InsertThematicBreak />
              <Separator />
              <DiffSourceToggleWrapper>
                <UndoRedo />
              </DiffSourceToggleWrapper>

          </>
          )
        })
      ]}
      contentEditableClassName='prose min-w-full bg-white rounded-md min-h-[93vh] h-full whitespace-pre-wrap'
      {...props}
      ref={editorRef}
    />
  )
}
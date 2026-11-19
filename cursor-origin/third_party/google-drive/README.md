# Google Drive

Cursor plugin that connects agents to [Google Drive](https://drive.google.com) through Cursor's remote [Model Context Protocol](https://modelcontextprotocol.io/) server.

Search Drive, read file metadata and contents, create or update files, and manage sharing.

## Use the skill

Load [`google-drive`](skills/google-drive/SKILL.md) and connect the corresponding MCP service in your agent.

## MCP

```json
{
  "mcpServers": {
    "google-drive": {
      "type": "http",
      "url": "https://api.cursor.com/rest-mcp/google-drive/mcp"
    }
  }
}
```

Auth is OAuth 2.0 against Google. Cursor prompts for Google sign-in when the plugin connects.

## Docs

- Google Drive API: https://developers.google.com/workspace/drive/api/reference/rest/v3
- Google Drive overview: https://developers.google.com/workspace/drive

Logo is the official Google Drive product icon, placed on a white tile with padding so it reads well in the Cursor UI:
https://www.gstatic.com/images/branding/productlogos/drive_2026/v1/192px.svg

## License

MIT

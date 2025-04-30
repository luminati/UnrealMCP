"""Asset tools-related commands for Unreal Engine.

This module contains all asset tools-related commands for the UnrealMCP bridge,
including creation, modification, and querying of assets.
"""

import sys
import os
from mcp.server.fastmcp import Context

# Import send_command from the parent module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from unreal_mcp_bridge import send_command

def register_all(mcp):
    """Register all asset tools-related commands with the MCP server."""
    
    @mcp.tool()
    def create_asset(ctx: Context, package_path: str, name: str, asset_type: str, properties: dict = None) -> str:
        """Create a new asset in the Unreal project.
        
        Args:
            package_path: The path where the asset should be created (e.g., '/Game/Assets')
            name: The name of the asset
            asset_type: The type of asset to create (e.g., 'StaticMesh', 'Texture', etc.)
            properties: Optional dictionary of asset properties to set.
        """
        try:
            params = {
                "package_path": package_path,
                "name": name,
                "asset_type": asset_type
            }
            if properties:
                params["properties"] = properties
            response = send_command("create_asset", params)
            if response["status"] == "success":
                return f"Created asset: {response['result']['name']} at path: {response['result']['path']}"
            else:
                return f"Error: {response['message']}"
        except Exception as e:
            return f"Error creating asset: {str(e)}"

    @mcp.tool()
    def modify_asset(ctx: Context, path: str, properties: dict) -> str:
        """Modify an existing asset's properties.
        
        Args:
            path: The full path to the asset (e.g., '/Game/Assets/MyAsset')
            properties: Dictionary of asset properties to set.
        """
        try:
            params = {
                "path": path,
                "properties": properties
            }
            response = send_command("modify_asset", params)
            if response["status"] == "success":
                return f"Modified asset: {response['result']['name']} at path: {response['result']['path']}"
            else:
                return f"Error: {response['message']}"
        except Exception as e:
            return f"Error modifying asset: {str(e)}"

    @mcp.tool()
    def get_asset_info(ctx: Context, path: str) -> dict:
        """Get information about an asset.
        
        Args:
            path: The full path to the asset (e.g., '/Game/Assets/MyAsset')
            
        Returns:
            Dictionary containing asset information.
        """
        try:
            params = {"path": path}
            response = send_command("get_asset_info", params)
            if response["status"] == "success":
                return response["result"]
            else:
                return {"error": response["message"]}
        except Exception as e:
            return {"error": str(e)}
